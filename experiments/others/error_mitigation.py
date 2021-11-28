# The function we changed in qiskit-ignis

# from line 378, changed the function fun(x) to fun2(x)

            elif method == 'least_squares':

                def fun(x):
                    mat_dot_x = np.zeros([num_of_states], dtype=float)
                    for state1_idx, state1 in enumerate(all_states):
                        mat_dot_x[state1_idx] = 0.
                        for state2_idx, state2 in enumerate(all_states):
                            if x[state2_idx] != 0:
                                product = 1.
                                end_index = self.nqubits
                                for c_ind, cal_mat in \
                                        enumerate(self._cal_matrices):

                                    start_index = end_index - \
                                        self._qubit_list_sizes[c_ind]

                                    state1_as_int = \
                                        self._indices_list[c_ind][
                                            state1[start_index:end_index]]

                                    state2_as_int = \
                                        self._indices_list[c_ind][
                                            state2[start_index:end_index]]

                                    end_index = start_index
                                    product *= \
                                        cal_mat[state1_as_int][state2_as_int]
                                    if product == 0:
                                        break
                                mat_dot_x[state1_idx] += \
                                    (product * x[state2_idx])
                    return sum(
                        (raw_data2[data_idx] - mat_dot_x)**2)
                
                def fun2(x):
                    mat_dot_x = deepcopy(x)
                    for i, cal_mat in enumerate(self._cal_matrices):
                        res_mat_dot_x = np.zeros([num_of_states], dtype=float)
                        for state_idx, state in enumerate(all_states):
                            res_mat_dot_x[state_idx] += cal_mat[int(state[i]), int(state[i])] * mat_dot_x[state_idx]
                            flip_state = state[:i] + str(int(state[i]) ^ 1) + state[i+1:]
                            res_mat_dot_x[int(flip_state, 2)] += cal_mat[int(state[i]) ^ 1, int(state[i])] * mat_dot_x[state_idx]
                        mat_dot_x = res_mat_dot_x
                    return sum( (raw_data2[data_idx] - mat_dot_x) ** 2)

                x0 = np.random.rand(num_of_states)
                x0 = x0 / sum(x0)
                nshots = sum(raw_data2[data_idx])
                cons = ({'type': 'eq', 'fun': lambda x: nshots - sum(x)})
                bnds = tuple((0, nshots) for x in x0)
                # res = minimize(fun, x0, method='SLSQP', constraints=cons, bounds=bnds, tol=1e-6)
                res = minimize(fun2, x0, method='SLSQP', constraints=cons, bounds=bnds, tol=tol)
                raw_data2[data_idx] = res.x