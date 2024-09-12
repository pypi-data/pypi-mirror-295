"""Homogeneously mixing continuous-time SIR model"""

import numpy as np
import tensorflow as tf

from gemlib.distributions import ContinuousTimeStateTransitionModel

incidence_matrix = np.array([[-1, 0], [1, -1], [0, 1]], np.float32)
initial_conditions = np.array([[99, 1, 0]], np.float32)


def make_rate_fn(beta, gamma):
    def rate_fn(t, state):
        si_rate = beta * state[:, 1] / tf.reduce_sum(state, axis=-1)
        ir_rate = tf.broadcast_to([gamma], si_rate.shape)
        return si_rate, ir_rate

    return rate_fn


model = ContinuousTimeStateTransitionModel(
    transition_rate_fn=make_rate_fn(0.2, 0.14),
    incidence_matrix=incidence_matrix,
    initial_state=initial_conditions,
    num_steps=80,
)
