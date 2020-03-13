from game import GameEnv
import random

env = GameEnv()
actions = [i for i in range(4)]
done = False

while not done:
    state, reward, done = env.step(random.sample(actions, 1)[0])
