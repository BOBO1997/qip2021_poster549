#!/usr/bin/env python
# coding: utf-8

# In[1]:


def adjacency_list_for_path_graph(n):
    """
    Input
        n : int, size of the path graph
    Output
        graph : list of list, adjacency list of the path graph
    """
    graph = []
    if n == 1:
        graph.append([])
    else:
        graph.append([1])
        for j in range(1, n - 1):
            graph.append([j - 1, j + 1])
        graph.append([n - 2])
    return graph


# In[2]:


def adjacency_list_for_star_graph(n):
    """
    Input
        n : int, size of the star graph
    Output
        graph : list of list, adjacency list of the star graph
    """
    graph = []
    if n == 1:
        graph.append([])
    else:
        graph.append(list(range(1,n)))
        for j in range(1, n):
            graph.append([0])
    return graph


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


# In[3]:


import subprocess
subprocess.run(['jupyter', 'nbconvert', '--to', 'python', 'graph_lib.ipynb'])

