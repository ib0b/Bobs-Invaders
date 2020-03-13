from game import GameEnv
import random

env = GameEnv(1/60)
actions = [i for i in range(4)]
done = False

print(env.reset())
# env.loop()


def randMove():
    while not done:
        state, reward, done = env.step(random.sample(actions, 1)[0])
