---
title: Graph Neural Networks in Computer Networks: A Survey on Optimization and Prediction of Network Performance
date: 2024-10-03 16:00:00 +09:00
# categories: []
tags: [gnn, computer network, survey]     # TAG names should always be lowercase
author: "Chi Yeong Heo"
# description: Introduction to the course
---


## 1. Abstract

Graph Neural Networks (GNNs) have been widely used in various fields. As Computer Networks are essentially graphs, we can represent the network as a graph and apply GNNs to analyze and optimize the network. Our project on this topic would help us deepen our knowledge about GNNs and Computer Networks. Therefore, we decided to conduct a survey to find whether this project is feasible.

## 2. Introduction

### 2.1 Background

    pass

### 2.2 Motivation

- Queuing Theory imposes strong assumptions on the packet arrival process (Poisson traffic generation), which often is not sufficient to model real-world networks.
- packet-level simulators can accurately model networks. However, they are computationally expensive and time-consuming. The cost of a simulator depends linearly on the number of packets forwarded.
- Classical Deep Learning techniques(MLPS, RNNs) fail to provide accurate estimates when the network scenario differs from teh examples seen during trainig.

## 3. GNNs in Computer Networks

### 3.1 BNN-UPC

The [Barcelona Neural Networking Center (BNN-UPC)](https://bnn.upc.edu/) is a research center that focuses on the application of Graph Neural Networks (GNNs) in Computer Networks. They provide datasets and tools about this topic and have published many papers.

Graph Neural Networking Challenge

- 2020
  - Build a model that estimates performance metrics given a network snapshot.
- 2021
  - Bulid a model that scales to larger networks than those seen during training.
- 2022
  - Produce a training dataset that results in better performance for the target GNN model.
- 2023
  - Build a model with datasets from real-world networks.

#### RouteNet-Fermi

Queuing Theory
packet-level simulator
NEtwork Digital Twin

a GNN-based model that provides performance estimates (delay, jitter, and packet loss) on given network scenarios.

Traffic models: Networks carry different types of traffic,
so, supporting arbitrary stochastic traffic models is crucial.
Experimental observations show that traffic on the Internet has
strong autocorrelation and heavy-tails [13]. In this context, it is
well-known that the main limitation of Queuing Theory is that
it fails to provide accurate estimates on realistic Markovian
models with continuous state space, or non-Markovian traffic
models. The challenge for DL-based modeling is: How can
we design a neural network architecture that can accurately
model realistic traffic models?

Training and Generalization:
the DL model can predict only scenarios it has previously seen.
Note that this is a common property of all neural network
architectures.
the generalization to larger
networks. Real-world networks include hundreds or thousands
of nodes, and building a network testbed at this scale is
typically unfeasible.

- Netowrk Simulator:
  - OMNET++
  - ns3
- unrivaled accuracy
- can simulate virtually any network scenario
- high computational cost

metric: Mean Absolute Percentage Error (MAPE)

Message-Passing Neural Network (MPNN): not good

- not take into account the paths traversed by different traffic flows (i.e., the routing
configuration), which is a fundamental property to understand inter-dependencies between flows and links.
- learned the relationships between flows and links no loner valid when the routing configuration changes.

there is a circular dependency
between the flows and links found in the network. At the same
time, the state of a flow depends on the state of the links they
traverse, and the state of the links depends on the state of the
flows passing through them.

If we apply a standard GNN over this example, the state of
each flow is not updated at each hop. Therefore, the GNN does not have a structure that represents how the delay depends on
both the links (topology) and the flows that go through each
specific router.

Model:

input:

- network topology
- routing scheme (flow level)
- queuing configuration (interface level)
- a set of traffic flows characterized by some parameters.

output:

- eestimates of relevant performance metrics (delay, jitter, packet loss)

description:

- finding a good representation of the network components
supported by the model (e.g., traffic models, routing, queue
scheduling)
- exploit scale-independent features of
networks to accurately scale to larger networks unseen during
training

Representing network components and their relationships:

Define a network as:

- a set of source-destination flows

$$
\mathcal{F} = \{f_i : i \in (1, ..., n_f)\}
$$

- a set of queues

$$
\mathcal{Q} = \{q_j : j \in (1, ..., n_q)\}
$$

- a set of links

$$
\mathcal{L} = \{l_k : k \in (1, ..., n_l)\}
$$

According to the routing configuration,
flows follow a source-destination path.

Define flows as sequences of tuples with the queues and links they traverse:

$$
f_i = \{(q^{i,1}, l^{i,1}), ..., (q^{i,M}, l^{i,M})\}
$$

where M is the path length of the flow (number of links).

$Q_f(q_j)$: a function that returns all the flows passing through a queue $q_j$.

$L_f(l_k)$: a function that returns all the flows passing through a link $l_k$.

$L_q(l_k)$: a function that returns the queues $q_{l_k} \in \mathcal{Q}$ injecting traffic into link $l_k$ (i.e., the queues at the output port to which the link is connected).

three basic principles:

1) The state of flows (e.g., delay, throughput, packet loss) is
affected by the state of the queues and links they traverse
(e.g., queue/link utilization).
2) The state of queues (e.g., occupation) depends on the state
of the flows passing through them (e.g., traffic volume,
burstiness).
3) The state of links (e.g., utilization) depends on the states
of the queues that can potentially inject traffic into the
link, and the queue scheduling policy applied over these
queues (e.g., Strict Priority, Weighted Fair Queuing).
Formally, these principles can be formulated as follows:

$$
\begin{align*}
h_{f_i} = G_f(h_{q^{i,1}}, h_{l^{i,1}}, ..., h_{q^{i,M}}, h_{l^{i,M}}) \\
h_{q_j} = G_q(h_{f_1}, ..., h_{f_I}), f_i \in Q_f(q_j) \\
h_{l_k} = G_l(h_{q_1}, ..., h_{q_J}), q_j \in L_q(l_k)
\end{align*}
$$

Where $G_f$, $G_q$ and $G_l$ are some unknown functions, and $h_f$, $h_q$ and $h_l$ are latent variables that encode information about the state of the flows $\mathcal{F}$, queues $\mathcal{Q}$ and links $\mathcal{L}$, respectively. Note that these principles define a circular dependency
between the three network components (F, Q, and L) that
must be solved to find latent representations satisfying the
equations above.

RouteNet-F implements a three-stage message
passing algorithm that combines the states of flows F, queues
Q, and links L, and updates them iteratively. Finally, it
combines these states to estimate flow-level delays, jitters,
and packet loss.
