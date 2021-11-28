#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pprint
# import multiprocessing as multi
# from multiprocessing import Pool
import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit import IBMQ
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from qiskit.compiler import transpile
from qiskit.providers.aer.noise import NoiseModel
import qiskit.providers.aer.noise as noise
from qiskit.ignis.mitigation.measurement import complete_meas_cal, tensored_meas_cal, CompleteMeasFitter, TensoredMeasFitter


# ## Prepare Graph States

# In[ ]:


def general_graph_state(graph, barrier=False):
    """
    Input
        graph       : 2d array of graph representation by adjacency matrix
    Output 
        graph_state : qiskit.QuantumCircuit of graph state
    """
    
    graph_size = len(graph) # == len(graph) == len(graph[0])
    graph_state = QuantumCircuit(graph_size)

    ## start all qubits in |+> state
    graph_state.h(range(graph_size))
    if barrier:
        graph_state.barrier()
    
    ## make a CZ between the control qubit and target qubits
    for j in range(graph_size):
        for k in range(j):
            if graph[j][k] == 1: # operate cz = h * cx * h
                graph_state.cz(j, k)

    return graph_state


# In[ ]:


def path_graph_state(size, barrier=False):
    if size <= 1:
        return None
    graph_state = QuantumCircuit(size)
    graph_state.h(range(size))
    if barrier:
        graph_state.barrier()
    for i in [i for i in range(size) if i % 2 == 0][:-1]:
        graph_state.cz(i, i + 1)
    if size % 2 == 0:
        graph_state.cz(size - 2, size - 1)
    for i in [i for i in range(size) if i % 2 == 1][:-1]:
        graph_state.cz(i, i + 1)
    if size % 2 == 1:
        graph_state.cz(size - 2, size - 1)
    return graph_state


# In[ ]:


def ring_graph_state(size, barrier=False):
    if size <= 2:
        return None
    graph_state = QuantumCircuit(size)
    graph_state.h(range(size))
    if barrier:
        graph_state.barrier()
    for i in [i for i in range(size) if i % 2 == 0][:-1]:
        graph_state.cz(i, i + 1)
    if size % 2 == 0:
        graph_state.cz(size - 2, size - 1)
    for i in [i for i in range(size) if i % 2 == 1][:-1]:
        graph_state.cz(i, i + 1)
    if size % 2 == 1:
        graph_state.cz(size - 2, size - 1)
    graph_state.cz(size - 1, 0)
    return graph_state


# #### GHZ States

# In[ ]:


def ghz_state(size, barrier=False):
    if size <= 1:
        return None
    graph_state = QuantumCircuit(size)
    graph_state.h(0)
    for i in range(1, size):
        graph_state.cx(i - 1, i)
    if barrier:
        graph_state.barrier()
    return graph_state


# In[ ]:


def better_ghz_state(size, order, barrier=False):
    if size <= 1:
        return None
    graph_state = QuantumCircuit(size)
    graph_state.h(0)
    for i, j in order:
        graph_state.cx(i, j)
    if barrier:
        graph_state.barrier()
    return graph_state


# #### Star Graph States

# In[ ]:


def star_graph_state(size, barrier=False):
    if size <= 1:
        return None
    graph_state = QuantumCircuit(size)
    graph_state.h(range(size))
    if barrier:
        graph_state.barrier()
    for i in range(1, size):
        graph_state.cz(0, i)
    return graph_state


# In[ ]:


def star_graph_state_by_path(size, barrier=False):
    if size <= 1:
        return None
    graph_state = QuantumCircuit(size)
    graph_state.h(0)
    for i in range(1, size):
        graph_state.cx(i - 1, i)
    if barrier:
        graph_state.barrier()
    graph_state.h(range(1,size))
    return graph_state


# In[ ]:


def better_star_graph_state(size, order, barrier=False):
    if size <= 1:
        return None
    graph_state = QuantumCircuit(size)
    graph_state.h(0)
    for i, j in order:
        graph_state.cx(i, j)
    if barrier:
        graph_state.barrier()
    graph_state.h(range(1,size))
    return graph_state


# In[ ]:


def barrier_star_graph_state(size, order, barrier_poses, pi_rot=False):
    if size <= 1:
        return None
    iter_barrier_poses = iter(barrier_poses)
    pos = 0
    
    graph_state = QuantumCircuit(size)
    graph_state.h(0)
    for k, (i, j) in enumerate(order):
        if pos == k:
            graph_state.barrier()
            pos = next(iter_barrier_poses)
        graph_state.cx(i, j)
    graph_state.barrier()
    if pi_rot:
        graph_state.x(range(size))
        graph_state.barrier()
    graph_state.h(range(1,size))
    return graph_state


# In[ ]:


def refocusing_outer_star_graph_state(size, order, qubit_depths, system_size):
    if size <= 1:
        return None
    qc = QuantumCircuit(system_size)
    qc.h(0)
    if size < system_size:
        qc.h(range(size,system_size))
    depth = 0
    for i, j in order:
        if depth != qubit_depths[j]:
            qc.barrier()
            depth += 1
            if depth == (qubit_depths[-1] + 1) // 2:
                if size < system_size:
                    qc.x(range(size,system_size))
        qc.cx(i, j)
    qc.barrier()
    qc.h(range(1,system_size))
    return qc


# In[ ]:


def refocusing_last_star_graph_state(size, order, qubit_depths, system_size):
    if size <= 1:
        return None
    qc = QuantumCircuit(system_size)
    qc.h(0)
    if size < system_size:
        qc.h(range(size,system_size))
    depth = 0
    for i, j in order:
        if depth != qubit_depths[j]:
            qc.barrier()
            depth += 1
            if depth ==(qubit_depths[-1] + 1) // 2:
                if size < system_size:
                    qc.x(range(size,system_size))
        qc.cx(i, j)
    qc.barrier()
    qc.x(range(size))
    qc.h(range(1,system_size))
    return qc


# In[ ]:


def tree_graph_state(tree):
    # to be specified
    return


# ## Convert Adjacency Matrix <==> Ajacency List

# In[ ]:


def matrix_to_list(graph): # OK
    """
    Input
        graph : 2d matrix (n * n)
    Output
        adj_list : list of list (adjacency matrix)
        
    -> time complexity : O(n^2)
    """
    n = len(graph)
    adj_list = []
    for i in range(n):
        adj = []
        for j in range(n):
            if graph[i][j] == 1:
                adj.append(j)
        adj_list.append(adj)
    return adj_list


# In[ ]:


def list_to_matrix(graph):
    """
    Input
        graph : list of list (adjacency matrix)
    Output
        adj_matrix : 2d matrix (n * n)
        
    -> time complexity : O(n^2)
    """
    n = len(graph)
    adj_mat = []
    for i in range(n):
        row = [0] * n
        for j in graph[i]:
            row[j] = 1
        adj_mat.append(row)
    return adj_mat


# In[ ]:


import subprocess
subprocess.run(['jupyter', 'nbconvert', '--to', 'python', 'graph_state_lib.ipynb'])


# In[ ]:




