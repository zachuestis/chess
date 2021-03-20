import gym
from gym import spaces

import numpy as np
import pickle

# Libraries to create input image
import chess.svg
from cairosvg import svg2png
import cv2

## Parameters
try:
    ACTIONS = pickle.load(open("actions.pkl", "rb"))
except:
    from common.helper_functions import getAllPossibleMoves
    ACTIONS = np.array(getAllPossibleMoves())
    pickle.dump(ACTIONS, open("actions.pkl", "wb"))

N_DISCRETE_ACTIONS = ACTIONS.size
HEIGHT = 64
WIDTH = 64
N_CHANNELS = 1

REWARDS = [ -4e-5, -4e-4, 1 , -1 , 0 ]      # move, illegal move, win, loss, draw


class ChessEnv(gym.Env):

    def __init__(self, game):
        super(ChessEnv, self).__init__()
        self.game = game
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8)

    def step(self, action):
        done = False
        info = []
        # Execute action
        move_name = ACTIONS[action]
        legal, result = self.game.play(move_name)
        # Choose Reward
        if result is not None:
            done = True
            if result == 0:         # white wins --> TODO: match player color
                reward = REWARDS[2]
            elif result == 1:       # black wins
                reward = REWARDS[3]
            elif result == 2:       # draw
                reward = REWARDS[4]
        elif legal:
            reward = REWARDS[0]
        else:           # illegal move
            reward = REWARDS[1]
        
        # Get new state
        observation = self.getCurrentState()     # Next state
        
        return observation, reward, done, info

    def reset(self):
        self.game.reset()
        return self.getCurrentState() 

    def getCurrentState(self):      
        # TODO: directly create image / current state
        flipped = True if self.game.game_mode == 'white-auto' else False
        chessboard = chess.svg.board(
            self.game.board, size=WIDTH, coordinates=False, flipped=flipped).encode("UTF-8")

        chessboard = svg2png(chessboard)
        chessboard = np.frombuffer(chessboard, np.uint8)
        chessboard = cv2.imdecode(chessboard, cv2.IMREAD_GRAYSCALE)

        return chessboard.reshape(HEIGHT, WIDTH, N_CHANNELS)


if __name__ == "__main__":

    from game import Game
    game = Game('black-auto')
    env = ChessEnv(game)

    state = env.reset()
    env.step(8)



