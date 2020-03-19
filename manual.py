from game import GameEnv
import random

env = GameEnv(1/60)
env.stepReward = 0
env.playerShotReward = 0
env.enemyShotReward = 0
env.missedShotReward = 0
env.allDeadReward = 0
env.invasionReward = 0
env.bottomReward = 0
env.underReward = 0
env.anchorReward = 0
env.cornerReward = -0.001
env.reset()
actions = [i for i in range(4)]
done = False

# print(env.reset())
env.loop()


def randMove():
    done = False
    while not done:
        state, reward, done, win = env.step(random.sample(actions, 1)[0])

# for i in range(4):
#     env.reset()
#     randMove()
