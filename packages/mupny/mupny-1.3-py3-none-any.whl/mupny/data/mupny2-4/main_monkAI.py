import random

class Environment:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.initial_state = {
            'monk_pos': (random.randint(0, self.m), random.randint(0, self.n)),
            'key': False
        }
        self.key_pos = (random.choice([i for i in range(0, self.m) if i != state['monk_pos'][0]]),
                        random.choice([j for j in range(0, self.n) if j != state['monk_pos'][1]]))
        self.chest_pos = (random.choice([i for i in range(0, self.m)
                                         if i != self.initial_state['monk_pos'][0]
                                         and i != self.initial_state['key_pos'][0]
                                         ]),
                          random.choice([j for j in range(0, self.n)
                                         if j != self.initial_state['monk_pos'][1]
                                         and j != self.initial_state['key_pos'][1]
                                         ]))


environment = Environment(5, 4)

