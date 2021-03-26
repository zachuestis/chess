import random
import numpy as np

import torch

import cv2
import chess.svg
from chessEnv import HEIGHT, WIDTH, N_CHANNELS
from cairosvg import svg2png

from common.wrappers import wrap_pytorch

model_path = "model.pkl"

class AI():

    def __init__(self, board):
        self.board = board
        self.model = torch.load(model_path, map_location={'cuda:0':'cpu'})

    def choose_move(self):
        # Currently chooses random legal move
        legal_moves = [move for move in self.board.legal_moves]
        state = self.getCurrentState()

        if self.model:
            move = self.model.act(state, epsilon=0)  # on-policy
            if move not in legal_moves: print("AI choose illegal move.")
            return move if move in legal_moves else random.choice(legal_moves)
        else:
            return random.choice(legal_moves)

    def getCurrentState(self):
        # TODO: directly create image / current state
        chessboard = chess.svg.board(
            self.board, size=WIDTH, coordinates=False).encode("UTF-8")

        chessboard = svg2png(chessboard)
        chessboard = np.frombuffer(chessboard, np.uint8)
        chessboard = cv2.imdecode(chessboard, cv2.IMREAD_GRAYSCALE)
        chessboard = chessboard.reshape(HEIGHT, WIDTH, N_CHANNELS)

        return np.swapaxes(chessboard, 2, 0)
