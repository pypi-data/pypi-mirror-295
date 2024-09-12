"""Tests for HMC sampler"""

import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.mcmc.hmc import hmc
from gemlib.mcmc.mcmc_sampler import mcmc

tfd = tfp.distributions

NUM_SAMPLES = 100000


@pytest.fixture
def simple_model():
    @tfp.distributions.JointDistributionCoroutine
    def model():
        yield tfp.distributions.Normal(loc=0.0, scale=1.0, name="foo")
        yield tfp.distributions.Normal(loc=1.0, scale=1.0, name="bar")
        yield tfp.distributions.Normal(loc=2.0, scale=1.0, name="baz")

    return model


def test_hmc(simple_model):
    mcmc_init_state = simple_model.sample(seed=[0, 0])
    algorithm = hmc(step_size=0.1, num_leapfrog_steps=16)

    state = algorithm.init(simple_model.log_prob, mcmc_init_state)
    new_state, info = algorithm.step(simple_model.log_prob, state, [0, 0])

    tf.nest.assert_same_structure(state, new_state)


def test_many_hmc(simple_model):
    mcmc_init_state = simple_model.sample(seed=[0, 0])
    algorithm = hmc(step_size=1.2, num_leapfrog_steps=16)

    samples, info = tf.function(
        lambda: mcmc(
            NUM_SAMPLES,
            sampling_algorithm=algorithm,
            target_density_fn=simple_model.log_prob,
            initial_position=mcmc_init_state,
            seed=[0, 0],
        ),
        jit_compile=True,
    )()

    np.testing.assert_allclose(
        np.array([np.mean(x) for x in samples]),
        np.array([0.0, 1.0, 2.0]),
        atol=1e-2,
    )
    np.testing.assert_allclose(
        np.array([np.var(x) for x in samples]),
        np.array([1.0, 1.0, 1.0]),
        atol=1e-2,
    )
