"""Mechanism for proposing event times to move"""

from warnings import warn

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.mcmc.internal import util as mcmc_util

from gemlib.distributions import (
    Categorical2,
    UniformInteger,
    UniformKCategorical,
)

tfd = tfp.distributions


def _events_or_inf(events, transition_id):
    if transition_id is None:
        return tf.fill(
            events.shape[:-1], tf.constant(np.inf, dtype=events.dtype)
        )
    return tf.gather(events, transition_id, axis=-1)


def _abscumdiff(
    events, initial_state, topology, t, delta_t, bound_times, int_dtype=tf.int32
):
    """Returns the number of free events to move in target_events
       bounded by max([N_{target_id}(t)-N_{bound_id}(t)]_{bound_t}).

    :param events: a [T, M, X] tensor of transition events
    :param initial_state: a [M, X] tensor of the constraining initial state
    :param target_id: the Xth index of the target event
    :param bound_t: the times to compute the constraints
    :param bound_id: the Xth index of the bounding event, -1 implies no bound

    :returns: a tensor of shape [M] + bound_t.shape[0] +  of max free events,
              dtype=target_events.dtype
    """
    with tf.name_scope("_abscumdiff"):
        # This line prevents negative indices.  However, we must have
        # a contract that the output of the algorithm is invalid!
        bound_times = tf.clip_by_value(
            bound_times, clip_value_min=0, clip_value_max=events.shape[-3] - 1
        )

        # Maybe replace with pad to avoid unstack/stack
        prev_events = _events_or_inf(events, topology.prev)
        target_events = tf.gather(events, topology.target, axis=-1)
        next_events = _events_or_inf(events, topology.next)
        event_tensor = tf.stack(
            [prev_events, target_events, next_events], axis=-1
        )

        # Compute the absolute cumulative difference between event times
        diff = event_tensor[..., 1:] - event_tensor[..., :-1]  # [T, m, 2]
        cumdiff = tf.abs(tf.cumsum(diff, axis=-3))  # cumsum along time axis

        # Create indices into cumdiff [d_max, m, 2].  Last dimension selects
        # the bound for either the previous or next event.
        elems = [
            tf.reshape(bound_times, [-1]),
            tf.repeat(
                tf.range(events.shape[1], dtype=int_dtype),
                [bound_times.shape[1]],
            ),
            tf.repeat(tf.where(delta_t < 0, 0, 1), [bound_times.shape[1]]),
        ]
        indices = tf.stack(elems, axis=-1)
        indices = tf.reshape(
            indices, [events.shape[-2], bound_times.shape[1], 3]
        )
        free_events = tf.gather_nd(cumdiff, indices)

        # Add on initial state
        indices = tf.stack(
            [
                tf.range(events.shape[-2]),
                tf.where(
                    delta_t[:, 0] < 0, topology.target, topology.target + 1
                ),
            ],
            axis=-1,
        )
        bound_init_state = tf.gather_nd(initial_state, indices)
        free_events += bound_init_state[..., tf.newaxis]

        return free_events


class Deterministic2(tfd.Deterministic):
    def __init__(
        self,
        loc,
        atol=None,
        rtol=None,
        validate_args=False,
        allow_nan_stats=True,
        log_prob_dtype=tf.float32,
        name="Deterministic",
    ):
        parameters = dict(locals())
        super().__init__(
            loc,
            atol=atol,
            rtol=rtol,
            validate_args=validate_args,
            allow_nan_stats=allow_nan_stats,
            name=name,
        )
        self.log_prob_dtype = log_prob_dtype

    def _prob(self, x):
        return tf.constant(1, dtype=self.log_prob_dtype)


def event_time_proposal(
    events, initial_state, topology, d_max, n_max, dtype=tf.int32, name=None
):
    """Draws an event time move proposal.
    :param events: a [T, M, K] tensor of event times (M number of
                   metapopulations, T number of full_timepoints, K number of
                   transitions)
    :param initial_state: a [M, S] tensor of initial metapopulation x state
                          counts
    :param topology: a 3-element tuple of (previous_transition,
                     target_transition, next_transition), eg "(s->e, e->i,
                     i->r)" (assuming we are interested presently in e->i,
                     `None` for boundaries)
    :param d_max: the maximum distance over which to move (in time)
    :param n_max: the maximum number of events to move
    """
    target_events = tf.gather(events, topology.target, axis=-1)
    time_interval = tf.range(d_max, dtype=dtype)

    def t():
        with tf.name_scope("t"):
            # Waiting for fixed tf.nn.sparse_softmax_cross_entropy_with_logits
            x = tf.cast(target_events > 0, dtype=events.dtype)  # [T, M]
            return Categorical2(
                logits=tf.transpose(tf.math.log(x)), name="event_coords"
            )

    def delta_t(t):
        with tf.name_scope("delta_t"):
            d_max_bcast = tf.broadcast_to(d_max, [events.shape[-2]])
            low = -tf.clip_by_value(
                d_max_bcast, clip_value_min=0, clip_value_max=t
            )
            high = tf.clip_by_value(
                d_max_bcast,
                clip_value_min=0,
                clip_value_max=events.shape[-3] - t - 1,
            )
            return UniformInteger(
                low=low, high=high + 1, float_dtype=events.dtype
            )

    def x_star(t, delta_t):
        with tf.name_scope("x_star"):
            # Compute bounds
            # The limitations of XLA mean that we must calculate bounds for
            # intervals [t, t+delta_t) if delta_t > 0, and [t+delta_t, t) if
            # delta_t is < 0.
            t = t[..., tf.newaxis]
            delta_t = delta_t[..., tf.newaxis]
            bound_times = tf.where(
                delta_t < 0,
                t - time_interval - 1,
                t + time_interval,  # [t+delta_t, t)
            )  # [t, t+delta_t)

            free_events = _abscumdiff(
                events=events,
                initial_state=initial_state,
                topology=topology,
                t=t,
                delta_t=delta_t,
                bound_times=bound_times,
                int_dtype=dtype,
            )

            # Mask out bits of the interval we don't need for our delta_t
            inf_mask = tf.cumsum(
                tf.one_hot(
                    tf.math.abs(delta_t[:, 0]),
                    d_max,
                    on_value=tf.constant(np.inf, events.dtype),
                    dtype=events.dtype,
                )
            )
            free_events = tf.maximum(inf_mask, free_events)
            free_events = tf.reduce_min(free_events, axis=-1)

            indices = tf.stack(
                [t[:, 0], tf.range(events.shape[-2], dtype=dtype)], axis=-1
            )
            available_events = tf.gather_nd(target_events, indices)
            max_events = tf.minimum(free_events, available_events)
            max_events = tf.clip_by_value(
                max_events, clip_value_min=0, clip_value_max=n_max
            )
            # Draw x_star
            return UniformInteger(
                low=1, high=max_events + 1, float_dtype=events.dtype
            )

    return tfd.JointDistributionNamed(
        {"t": t, "delta_t": delta_t, "x_star": x_star}, name=name
    )


def filtered_event_time_proposal(  # pylint: disable-invalid-name
    events,
    initial_state,
    topology,
    m_max,
    d_max,
    n_max,
    dtype=tf.int32,
    name=None,
):
    """FilteredEventTimeProposal allows us to choose a subset of indices
    in `range(events.shape[0])` for which to propose an update.  The
    results are then broadcast back to `events.shape[0]`.

    :param events: a [T, M, R] event tensor
    :param initial_state: a [M, S] initial state tensor
    :param topology: a TransitionTopology named tuple describing the ordering
                     of events
    :param m: the number of metapopulations to move
    :param d_max: maximum distance in time to move
    :param n_max: maximum number of events to move (user defined)
    :return: an instance of a JointDistributionNamed
    """
    if mcmc_util.is_list_like(events):
        warn(
            "Batched FilteredEventTimeProposals are not yet supported",
            stacklevel=1,
        )
        events = events[0]

    target_events = tf.gather(events, topology.target, axis=-1)

    def m():
        with tf.name_scope("m"):
            hot_meta = tf.math.count_nonzero(target_events, axis=-1) > 0
            X = UniformKCategorical(
                m_max, hot_meta, float_dtype=events.dtype, name="m"
            )
            return X

    def move(m):
        """We select out meta-population `m` from the first
        dimension of `events`.
        :param m: a 1-D tensor of indices of meta-populations
        :return: a random variable of type `EventTimeProposal`
        """
        with tf.name_scope("move"):
            select_meta = tf.gather(events, m, axis=-2)
            select_init = tf.gather(initial_state, m, axis=-2)
            return event_time_proposal(
                select_meta,
                select_init,
                topology,
                d_max,
                n_max,
                dtype=dtype,
                name=name,
            )

    return tfd.JointDistributionNamed(
        {"m": m, "move": move}, name="FilteredEventTimeProposal"
    )
