"""DiscreteTimeStateTransitionModel examples"""

import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.lines import Line2D

from gemlib.distributions.discrete_time_state_transition_model import (
    DiscreteTimeStateTransitionModel,
)
from gemlib.util import compute_state

# Example 1: SIR model for a single population

dtype = tf.float32

# Initial state, counts per compartment (S, I, R), for one population
initial_state = tf.constant([[99, 1, 0]], dtype)

# Stoichiometry matrix
stoichiometry = tf.constant(
    [  #  S  I  R
        [-1, 1, 0],  # S->I
        [0, -1, 1],  # I->R
    ],
    dtype,
)

# time parameters
initial_step, time_delta, num_steps = 0.0, 1.0, 100


def txrates(t, state):
    """Transition rate per individual corresponding to each row of the
    stoichiometry matrix.

    Args:
    ----
        state: `Tensor` representing the current state (count of individuals in
               each compartment).
        t: Python float representing the current time. For example seasonality
           in the S->I transition could be driven by tensors of the following
           form:
                seasonality = tf.math.sin(2 * 3.14159 * t / 20) + 1
                si = seasonality * beta * state[:, 1] / tf.reduce_sum(state)

    Returns:
    -------
        List of `Tensor`(s) each of which corresponds to a transition.

    """
    beta, gamma = 0.28, 0.14  # note R0=beta/gamma
    si = beta * state[:, 1] / tf.reduce_sum(state)  # S->I transition rate
    ir = tf.constant([gamma], dtype)  # I->R transition rate
    return [si, ir]


# Instantiate model
sir = DiscreteTimeStateTransitionModel(
    transition_rate_fn=txrates,
    stoichiometry=stoichiometry,
    initial_state=initial_state,
    initial_step=initial_step,
    time_delta=time_delta,
    num_steps=num_steps,
)


@tf.function
def simulate_one(elems):
    """One realisation of the epidemic process."""
    return sir.sample()


nsim = 15  # Number of realisations of the epidemic process
eventlist = tf.map_fn(
    simulate_one,
    tf.ones([nsim, stoichiometry.shape[0]]),
    fn_output_signature=dtype,
)

# Events for each transition with shape (simulation, population, time,
#   transition)
print("I->R events:", eventlist[0, 0, :, 1])

# Log prob of observing the eventlist, of first simulation, given the model
print("Log prob:", sir.log_prob(eventlist[0, ...]))
print(
    "log prob of each simulation:",
    tf.vectorized_map(
        fn=lambda i: sir.log_prob(eventlist[i, ...]), elems=tf.range(nsim)
    ),
)


# Plot timeseries of counts in each compartment from eventlist
def plot_timeseries(
    initial_state,
    eventlist,
    stoichiometry,
    initial_step,
    time_delta,
    num_steps,
    nsim,
    col,
    legend,
):
    """Plot timeseries of counts in each compartment."""
    state_timeseries = compute_state(initial_state, eventlist, stoichiometry)
    x = tf.range(
        initial_step, initial_step + time_delta * num_steps, delta=time_delta
    )
    for i in range(0, initial_state.shape[0]):  # populations
        plt.subplots_adjust(hspace=0.8)
        plt.subplot(initial_state.shape[0], 1, i + 1)
        for j in range(0, nsim):  # simulations
            for k in range(0, initial_state.shape[1]):  # compartments
                plt.step(x, state_timeseries[j, i, :, k], col[k], lw=0.5)
        lines = [Line2D([0], [0], color=c, lw=0.5) for c in col]
        plt.legend(lines, legend)
        plt.title(str(nsim) + " simulations of population " + str(i))
        plt.xlabel("time")
        plt.ylabel("count")


plot_timeseries(
    initial_state,
    eventlist,
    stoichiometry,
    initial_step,
    time_delta,
    num_steps,
    nsim,
    ["k", "r", "b"],
    ["S", "I", "R"],
)
plt.show()

# Example 2: SIR feedback model where recovered become susceptible

dtype = tf.float32

# Initial state, counts per compartment (S, I, R), for one population
initial_state = tf.constant([[999, 1, 0]], dtype)

# Stoichiometry matrix      #  S, I, R
stoichiometry = tf.constant(
    [
        [-1, 1, 0],  # S->I
        [0, -1, 1],  # I->R
        [1, 0, -1],
    ],  # R->S
    dtype,
)
# time parameters
initial_step, time_delta, num_steps = 0.0, 1.0, 200


def txrates(t, state):
    """Transition rate per individual with feedback from R to S."""
    beta, gamma, eta = 0.6, 0.4, 0.05
    si = beta * state[:, 1] / tf.reduce_sum(state)  # S->I transition rate
    ir = tf.constant([gamma], dtype)  # I->R transition rate
    rs = tf.constant([eta], dtype)  # R->S transition rate
    return [si, ir, rs]


# Instantiate model
sirs = DiscreteTimeStateTransitionModel(
    transition_rate_fn=txrates,
    stoichiometry=stoichiometry,
    initial_state=initial_state,
    initial_step=initial_step,
    time_delta=time_delta,
    num_steps=num_steps,
)


@tf.function
def simulate_one(elems):
    """One realisation of the epidemic process."""
    return sirs.sample()


nsim = 12
eventlist = tf.map_fn(
    simulate_one,
    tf.ones([nsim, stoichiometry.shape[0]]),
    fn_output_signature=dtype,
)

# Second simulation eventlist for transition I->R
print("I->R events:", eventlist[1, 0, :, 1])

# Log prob of observing the eventlist, of second simulation, given the model
print("Log prob:", sirs.log_prob(eventlist[1, ...]))

# Plot timeseries using plot_timeseries() from first example
plot_timeseries(
    initial_state,
    eventlist,
    stoichiometry,
    initial_step,
    time_delta,
    num_steps,
    nsim,
    ["k", "r", "b"],
    ["S", "I", "R"],
)
plt.show()

# Example 3: SEIR model for two populations

dtype = tf.float32

# Initial state, counts per compartment (S, E, I, R), for two populations
initial_state = tf.constant(
    [
        [450, 5, 5, 0],  # first population
        [990, 10, 0, 0],
    ],  # second population
    dtype,
)

# Stoichiometry matrix      #  S, E, I, R
stoichiometry = tf.constant(
    [
        [-1, 1, 0, 0],  # S->E
        [0, -1, 1, 0],  # E->I
        [0, 0, -1, 1],
    ],  # I->R
    dtype,
)
# time parameters
initial_step, time_delta, num_steps = 0.0, 1.0, 150


def txrates(t, state):
    """Transition rate per individual for 2 populations [population_0,
    population_1].
    """
    beta, delta, gamma = 0.25, 0.15, 0.05
    se = tf.stack(
        [
            beta * state[0, 1] / tf.reduce_sum(state[0, :]),
            beta * state[1, 1] / tf.reduce_sum(state[1, :]),
        ]
    )  # S->E transition rate
    ei = tf.constant([delta, delta], dtype)  # E->I transition rate
    ir = tf.constant([gamma, gamma], dtype)  # I->R transition rate
    return [se, ei, ir]


# Instantiate model
seir = DiscreteTimeStateTransitionModel(
    transition_rate_fn=txrates,
    stoichiometry=stoichiometry,
    initial_state=initial_state,
    initial_step=initial_step,
    time_delta=time_delta,
    num_steps=num_steps,
)


@tf.function
def simulate_one(elems):
    """One realisation of the epidemic process."""
    return seir.sample()


nsim = 10
eventlist = tf.map_fn(
    simulate_one,
    tf.ones([nsim, stoichiometry.shape[0]]),
    fn_output_signature=dtype,
)

# Sixth simulation, second population, transition E->I
print("E->I events:", eventlist[5, 1, :, 1].numpy())

# Log prob of observing the eventlist, of sixth simulation, given the model
print("Log prob:", seir.log_prob(eventlist[5, ...]))

# Plot timeseries using plot_timeseries() from first example
plot_timeseries(
    initial_state,
    eventlist,
    stoichiometry,
    initial_step,
    time_delta,
    num_steps,
    nsim,
    ["k", "g", "r", "b"],
    ["S", "E", "I", "R"],
)
plt.show()


# Example 4: SIR model with mixing between the two populations

dtype = tf.float32

# Initial state (counts). Infections in population 1 will be driven by
#   population 0
initial_state = tf.constant(
    [
        [700, 300, 0],  # population 0
        [1000, 0, 0],
    ],  # population 1
    dtype,
)

# Stoichiometry matrix      #  S, I, R
stoichiometry = tf.constant(
    [
        [-1, 1, 0],  # S->I
        [0, -1, 1],
    ],  # I->R
    dtype,
)

# Mixing matrix describes 25% mixing between 2 populations
C = tf.constant([[0.75, 0.25], [0.25, 0.75]], dtype)


def txrates(t, state):
    """Transition rate per individual with mixing between populations."""
    beta, gamma = 0.4, 0.1
    si = (
        beta * tf.linalg.matvec(C, state[:, 1]) / tf.reduce_sum(state)
    )  # S->I transition
    ir = tf.constant([gamma, gamma], dtype)  # I->R transition rate
    return [si, ir]


# time parameters
initial_step, time_delta, num_steps = 0.0, 1.0, 100

sirc = DiscreteTimeStateTransitionModel(
    transition_rate_fn=txrates,
    stoichiometry=stoichiometry,
    initial_state=initial_state,
    initial_step=initial_step,
    time_delta=time_delta,
    num_steps=num_steps,
)


@tf.function
def simulate_one(elems):
    """One realisation of the epidemic process."""
    return sirc.sample()


nsim = 15
eventlist = tf.map_fn(
    simulate_one,
    tf.ones([nsim, stoichiometry.shape[0]]),
    fn_output_signature=dtype,
)

# Log prob of observing the eventlist, of second simulation, given the model
print("Log prob:", sirc.log_prob(eventlist[1, ...]))

# Plot timeseries using plot_timeseries() from first example
plot_timeseries(
    initial_state,
    eventlist,
    stoichiometry,
    initial_step,
    time_delta,
    num_steps,
    nsim,
    ["k", "r", "b"],
    ["S", "I", "R"],
)
plt.show()

# Example 5: SIVR model for a single population (V=vaccinated)
dtype = tf.float32

# Initial state, counts per compartment (S, I, V, R), for one population
initial_state = tf.constant([[998, 1, 1, 0]], dtype)

# Stoichiometry matrix      #  S, I, V, R
stoichiometry = tf.constant(
    [
        [-1, 1, 0, 0],  # S->I
        [0, -1, 0, 1],  # I->R
        [-1, 0, 1, 0],  # S->V
        [0, 0, -1, 1],
    ],  # V->R
    dtype,
)

# time parameters
initial_step, time_delta, num_steps = 0.0, 1.0, 100


def txrates(t, state):
    """Transition rate per individual"""
    beta, gamma = 0.3, 0.2
    xi, eta = 0.6, 0.1
    si = beta * state[:, 1] / tf.reduce_sum(state)  # S->I transition rate
    ir = tf.constant([gamma], dtype)  # I->R transition rate
    sv = xi * state[:, 1] / tf.reduce_sum(state)  # S->V transition rate
    vr = tf.constant([eta], dtype)  # V->R transition rate
    return [si, ir, sv, vr]


# Instantiate model
sivr = DiscreteTimeStateTransitionModel(
    transition_rate_fn=txrates,
    stoichiometry=stoichiometry,
    initial_state=initial_state,
    initial_step=initial_step,
    time_delta=time_delta,
    num_steps=num_steps,
)


@tf.function
def simulate_one(elems):
    """One realisation of the epidemic process."""
    return sivr.sample()


nsim = 30  # Number of realisations of the epidemic process
eventlist = tf.map_fn(
    simulate_one,
    tf.ones([nsim, stoichiometry.shape[0]]),
    fn_output_signature=dtype,
)

# Events for each transition with shape (simulation, population, time,
#   transition)
print("S->V events:", eventlist[0, 0, :, 2])

# Log prob of observing the eventlist, of third simulation, given the model
print("Log prob:", sivr.log_prob(eventlist[2, ...]))

# Plot timeseries using plot_timeseries() from first example
plot_timeseries(
    initial_state,
    eventlist,
    stoichiometry,
    initial_step,
    time_delta,
    num_steps,
    nsim,
    ["k", "r", "g", "b"],
    ["S", "I", "V", "R"],
)
plt.show()
