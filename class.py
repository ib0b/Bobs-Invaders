from game import GameEnv
import random
import os
# learn
import math
import random
import pygame
from game import GameEnv
from time import sleep
import numpy as np
import os
import time
# os.environ["SDL_VIDEODRIVER"] = "dummy"
from collections import deque
from keras.models import Model, load_model, Sequential, load_model
from keras.layers import Input, Dense, Conv2D, Flatten
from keras.optimizers import Adam, RMSprop
import time
import keras
import matplotlib.pyplot as plt

from skimage.transform import resize
from skimage.color import rgb2gray
env = GameEnv()
stateSize = len(env.reset())
fakeState = env.reset()
print(stateSize)
env.getGameState()
# PREPROCESSING HYPERPARAMETERS
stack_size = 8                 # Number of frames stacked
# MODEL HYPERPARAMETERS
action_size = 4  # 4 possible actions

# Initialize deque with zero-images one array for each image
stacked_frames = deque([np.zeros((stateSize), dtype=np.int)
                        for i in range(stack_size)], maxlen=stack_size)


def stack_frames(stacked_frames, state, is_new_episode):
    # Preprocess frame
    small = resize(state, (80, 60), anti_aliasing=False)
    gray = rgb2gray(small)
    frame = gray

    if is_new_episode:
        # Clear our stacked_frames
        stacked_frames = deque([np.zeros((80, 60), dtype=np.int)
                                for i in range(stack_size)], maxlen=stack_size)

        # Because we're in a new episode, copy the same frame 4x
        for i in range(stack_size):
            stacked_frames.append(frame)

        # Stack the frames
        stacked_state = np.stack(stacked_frames, axis=0)

    else:
        # Append frame to deque, automatically removes the oldest frame
        stacked_frames.append(frame)

        # Build the stacked state (first dimension specifies different frames)
        stacked_state = np.stack(stacked_frames, axis=0)
    # stacked_state = stacked_state.reshape(-1)
    return stacked_state, stacked_frames


lastState, stacked_frames = stack_frames(stacked_frames, fakeState, True)
lastState, stacked_frames = stack_frames(stacked_frames, lastState, True)
print("stateShape", lastState.shape)
print("stacked", len(stacked_frames))


classifier = load_model("class.h5")
env = GameEnv(1/12)
actions = [i for i in range(4)]
done = False
state = env.reset()
state, stacked_frames = stack_frames(stacked_frames, state, True)
print("state", len(state))
env.enemyShotReward = 105
# class ouptupt
running = True
action = 0
totalReward = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action = 1
            if event.key == pygame.K_RIGHT:
                action = 2
            if event.key == pygame.K_SPACE:
                action = 3

        if event.type == pygame.KEYUP:
            # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            action = 0

        if event.type == pygame.QUIT:
            running = False
    state, reward, done, win = env.step(action)
    state, stacked_frames = stack_frames(stacked_frames, state, False)
    prediction = classifier.predict(np.array(state)[np.newaxis, :])
    print("prediction", np.argmax(prediction[0]))
    print("prediction", prediction[0][1])
    if(reward > 2):
        print("bump")
    totalReward += reward
print(f"steps={env.steps} totalR={totalReward}", )
# if(done):
#     running = False


def randMove():
    done = False
    while not done:
        state, reward, done, win = env.step(random.sample(actions, 1)[0])

# for i in range(4):
#     env.reset()
#     randMove()
