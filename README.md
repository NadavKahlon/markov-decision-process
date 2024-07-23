# Markov Decision Process (MDP)

This package provides an API for describing and solving Markov Decision
Processes, using the Value Iteration algorithm.

This project was developed in 2022, and uploaded to GitHub in 2024.

## Background

An MDP is the problem of choosing the correct action to transition between
states in a discrete state space. An available action's outcome is random,
distributed uniquely. Each state is associated with a reward metric, and the
goal is to maximize the agent's _utility_: the expected weighted-sum of the
agent's future rewards, with exponentially decaying weights.

An MDP's solution is a _policy_: a mapping between every state, and the ideal
action to take in it.

## Grid-MDP

We further implement a specific class of MDPs, I named "grid MDPs". These MDPs
consist of a grid-like state space, where:

* Each slot is a state.
* The states' rewards are specified by a _reward matrix_.
* The agent may choose to move one slot to up, down, left, or right, with a
random chance to land in either sides of the target slot.

Under `examples/grid_map_3x3.py` you can find a small script to solve a grid-MDP
with a 3x3 reward matrix, parameterized by the script's command-line argument.
