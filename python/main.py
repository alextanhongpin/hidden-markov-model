import math

obs = y = ('normal', 'cold', 'dizzy')
states = ('healthy', 'fever')
init_prob = {'healthy': 0.6, 'fever': 0.4}
tran_prob = {
  'healthy': {'healthy': 0.7, 'fever': 0.3},
  'fever': {'healthy': 0.4, 'fever': 0.6}
}
emit_prob = {
  'healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
  'fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
}


def viterbi(obs, states, init_prob, tran_prob, emit_prob):
  K, T = len(states), len(obs)
  # t1 and t2 is of size K x T
  t1 = [[0] * T for _ in range(0, K)]
  t2 = [[0] * T for _ in range(0, K)]
  # t1[state][obs]

  # For each initial state, compute the initial probability
  for i, s in enumerate(states):
    # The initial observation from the initial state
    t1[i][0] = init_prob[s] * emit_prob[s][obs[0]]
    t2[i][0] = 0
  
  # For the following observations (we exclude the first one)
  for i in range(1, T):
    prev_max = -math.inf
    prev_st = 0
    # For each state
    for j, jj in enumerate(states):
      p = [t1[k][i - 1] * tran_prob[kk][jj] * emit_prob[jj][obs[i]] 
           for k, kk in enumerate(states)]
      t1[j][i] = max(p)
      if max(p) > prev_max:
        prev_max = max(p)
        prev_st = p.index(max(p))
      t2[j][i] = prev_st if prev_max == max(p) else 0

  print('[t1]', t1)
  print('[t2]', t2)

  # Take the maximum value of the last item in t1
  z = [0 for i in range(0, T)]
  x = [0 for i in range(0, T)]

  # The highest probabilities
  p = [t1[s][-1] for s in range(len(states))]
  z[-1] = p.index(max(p))
  x[-1] = states[z[-1]]

  print('BREAKPOINT', x)

  # 3, 2, 1
  # 2, 1, 0
  for i in range(T-1, T-3, -1):
    n = t2[z[i]][i]
    s = t1[z[i]][i]
    print('[i]', i, ' n: {} state: {}'.format(n, s))
    z[i - 1] = n
    x[i - 1] = states[n]
  print('[z]', z)
  print('[x]', x)

viterbi(obs, states, init_prob, tran_prob, emit_prob)

# [T] 1
# PREV {'prob': 0.01512, 'prev': 'Healthy'}
# [T] 0
# PREV {'prob': 0.084, 'prev': 'Healthy'}