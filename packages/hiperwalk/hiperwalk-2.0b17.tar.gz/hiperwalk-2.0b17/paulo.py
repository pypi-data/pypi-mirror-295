import numpy as np
import hiperwalk as hpw

def hpw_calls(hpc):
    hpw.set_hpc(hpc)

    N = 101
    cycle = hpw.Cycle(N)
    ctqw = hpw.ContinuousTime(cycle, gamma=0.35)
    psi0 = ctqw.ket(N // 2)
    states = ctqw.simulate(range=(N // 2 + 1), state=psi0)
    prob = ctqw.probability_distribution(states)

    print('hpc ' + str(hpc) + ' states are unitary? '
          + str(np.allclose([psi@psi.conj() for psi in states],
                        np.ones(len(states)))))
    print('hpc ' + str(hpc) + ' probabilities sum up to one? '
          + str(np.allclose(prob.sum(axis=1), np.ones(len(prob)))))

    return states, prob

states, prob = hpw_calls(None)
print()
hpc_states, hpc_prob = hpw_calls('cpu')

print('Distance between states')
print(np.abs(states - hpc_states).sum(axis=1))
print()
print('Distance between probabilities')
print(np.abs(prob - hpc_prob).sum(axis=1))
