import os
import random
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import cv2
from game2 import GameEnv
import time
import skimage
import skimage.io
import pylab as pl
os.environ["SDL_VIDEODRIVER"] = "dummy"

env = GameEnv(0)
actions = [i for i in range(4)]
done = False
state = env.reset()

# fig = plt.figure()
# im = plt.imshow(state)
# images = []
# env.loop()
# pl.ion()
start = time.time()
while not done:
    state, reward, done, win = env.step(random.sample(actions, 1)[0])
    # image = np.rot90(state, axes=(1, 0))
    # im = plt.imshow(image, animated=True)
    # images.append([im])
    # img = pl.imshow(image)
    # pl.draw()
    # pl.pause(.05)
# ani = animation.ArtistAnimation(
#     fig, images, interval=50, blit=False,                          repeat_delay=1000)
# ani.save('dynamic_images.mp4')
# plt.show()


dur = time.time()-start
print(f"dur={dur} steps={env.steps} avg={env.steps/dur}")


def randMove():
    done = False
    while not done:
        state, reward, done, win = env.step(random.sample(actions, 1)[0])

# for i in range(4):
#     env.reset()
#     randMove()
