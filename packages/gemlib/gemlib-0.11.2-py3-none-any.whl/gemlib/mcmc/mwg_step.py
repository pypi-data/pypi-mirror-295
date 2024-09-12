"""Implementation of Metropolis-within-Gibbs framework"""

from __future__ import annotations

from collections import ChainMap, namedtuple
from typing import AnyStr, Callable

import tensorflow as tf
import tensorflow_probability as tfp

from .sampling_algorithm import (
    ChainAndKernelState,
    ChainState,
    KernelInfo,
    LogProbFnType,
    Position,
    SamplingAlgorithm,
    SeedType,
)

split_seed = tfp.random.split_seed

__all__ = ["MwgStep"]


def _project_position(
    position: Position, varnames: list[AnyStr]
) -> tuple[Position, Position]:
    """Splits `position` into `position[varnames]` and
    `position[~varnames]`
    """
    if varnames is None:
        return position, ()

    for name in varnames:
        if name not in position._asdict():
            raise ValueError(f"`{name}` is not present in `position`")

    target = {k: v for k, v in position._asdict().items() if k in varnames}
    target_compl = {
        k: v for k, v in position._asdict().items() if k not in varnames
    }

    return (
        namedtuple("Target", target.keys())(**target),
        namedtuple("TargetCompl", target_compl.keys())(**target_compl),
    )


def _join_dicts(a: dict, b: dict):
    """Joins two dictionaries `a` and `b`"""
    return dict(ChainMap(a, b))


class MwgStep:  # pylint: disable=too-few-public-methods
    """A Metropolis-within-Gibbs step.
    Transforms a base kernel to operate on a substate of a Markov chain.

    Args
    ----
    sampling_algorithm: a named tuple containing the generic kernel `init`
                        and `step` function.
    target_names: a list of variable names on which the
                        Metropolis-within-Gibbs step is to operate
    kernel_kwargs_fn: a callable taking the chain position as an argument,
                    and returning a dictionary of extra kwargs to
                    `sampling_algorithm.step`.

    Returns
    -------
    An instance of SamplingAlgorithm.

    """

    def __new__(
        cls,
        sampling_algorithm: SamplingAlgorithm,
        target_names: list[str] | None = None,
        kernel_kwargs_fn: Callable[[Position], dict] = lambda _: {},
    ):
        def init(
            target_log_prob_fn: LogProbFnType,
            initial_position: Position,
        ):
            target, target_compl = _project_position(
                initial_position, target_names
            )

            def conditional_tlp(*args):
                if target_names is None:
                    return target_log_prob_fn(*args)

                state = _join_dicts(
                    dict(zip(target._fields, args)),
                    target_compl._asdict(),
                )
                return target_log_prob_fn(**state)

            kernel_state = sampling_algorithm.init(
                conditional_tlp, target, **kernel_kwargs_fn(initial_position)
            )

            chain_state = ChainState(
                position=initial_position,
                log_density=kernel_state[0].log_density,
                log_density_grad=kernel_state[0].log_density_grad,
            )

            return chain_state, kernel_state[1]

        def step(
            target_log_prob_fn: LogProbFnType,
            chain_and_kernel_state: ChainAndKernelState,
            seed: SeedType,
        ) -> tuple[ChainAndKernelState, KernelInfo]:
            chain_state, kernel_state = chain_and_kernel_state

            # Split global state and generate conditional density
            target, target_compl = _project_position(
                chain_state.position, target_names
            )

            # Calculate the conditional log density
            def conditional_tlp(*args):
                if target_names is None:
                    return target_log_prob_fn(*args)

                state = _join_dicts(
                    dict(zip(target._fields, args)),
                    target_compl._asdict(),
                )
                return target_log_prob_fn(**state)

            chain_substate = chain_state._replace(
                position=target[0] if len(target) == 1 else target
            )

            # Invoke the kernel on the target state
            (new_chain_substate, new_kernel_state), info = (
                sampling_algorithm.step(
                    conditional_tlp,
                    (chain_substate, kernel_state),
                    seed,
                    **kernel_kwargs_fn(chain_state.position),
                )
            )

            if len(target) == 1:
                new_chain_substate = new_chain_substate._replace(
                    position=tf.nest.pack_sequence_as(
                        target, [new_chain_substate.position]
                    )
                )

            # Stitch the global position back together
            if target_names is None:
                new_global_state = new_chain_substate
            else:
                new_global_position = chain_state.position.__class__(
                    **new_chain_substate.position._asdict(),
                    **target_compl._asdict(),
                )
                new_global_state = new_chain_substate._replace(
                    position=new_global_position,
                )

            return (new_global_state, new_kernel_state), info

        return SamplingAlgorithm(init, step)
