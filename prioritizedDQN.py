# Prioritized DQN 
# Based on: https://github.com/higgsfield/RL-Adventure

import random
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

USE_CUDA = torch.cuda.is_available()
def Variable(x): return x.cuda() if USE_CUDA else x

class CnnDQN(nn.Module):
	def __init__(self, input_shape, num_actions):
		super(CnnDQN, self).__init__()

		self.input_shape = input_shape
		self.num_actions = num_actions

		self.features = nn.Sequential(
			nn.Conv2d(input_shape[0], 32, kernel_size=8, stride=4),
			nn.ReLU(),
			nn.Conv2d(32, 64, kernel_size=4, stride=2),
			nn.ReLU(),
			nn.Conv2d(64, 64, kernel_size=2, stride=1),
			nn.ReLU()
		)

		self.fc = nn.Sequential(
			nn.Linear(self.feature_size(), 512),
			nn.ReLU(),
			nn.ReLU(),
			nn.ReLU(),
			nn.Linear(512, self.num_actions)
		)

	def forward(self, x):
		x = self.features(x)
		x = x.view(x.size(0), -1)
		x = self.fc(x)
		return x

	def feature_size(self):
		return self.features(torch.zeros(1, *self.input_shape)).view(1, -1).size(1)

	def act(self, state, epsilon):
		if random.random() > epsilon:
			state = Variable(torch.FloatTensor(np.float32(state)).unsqueeze(0))
			q_value = self.forward(state)
			action = q_value.max(1)[1].data[0]
		else:
			action = random.randrange(env.action_space.n)
		return action


