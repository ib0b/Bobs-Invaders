import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2
from game2 import GameEnv
import random
import os

env = GameEnv(1/60, graphics=False)
actions = [i for i in range(4)]
done = False
state = env.reset()
env.bullets = 200
print("state", len(state))

env.loop()


def randMove():
    done = False
    while not done:
        state, reward, done, win = env.step(random.sample(actions, 1)[0])

# for i in range(4):
#     env.reset()
#     randMove()
