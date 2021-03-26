# Rainbow RL Algorithm class
# Based on: https://github.com/higgsfield/RL-Adventure


from chessEnv import ChessEnv
from game import Game

import random
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from common.replay_buffer import PrioritizedReplayBuffer
from common.wrappers import wrap_pytorch

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


# Training functions
def update_target(current_model, target_model):
	target_model.load_state_dict(current_model.state_dict())


def compute_td_loss(batch_size, beta):
	state, action, reward, next_state, done, indices, weights = replay_buffer.sample(
		batch_size, beta)

	state = Variable(torch.FloatTensor(np.float32(state)))
	next_state = Variable(torch.FloatTensor(np.float32(next_state)))
	action = Variable(torch.LongTensor(action))
	reward = Variable(torch.FloatTensor(reward))
	done = Variable(torch.FloatTensor(done))
	weights = Variable(torch.FloatTensor(weights))

	q_values = current_model(state)
	next_q_values = target_model(next_state)

	q_value = q_values.gather(1, action.unsqueeze(1)).squeeze(1)
	next_q_value = next_q_values.max(1)[0]
	expected_q_value = reward + gamma * next_q_value * (1 - done)

	loss = (q_value - expected_q_value.detach()).pow(2) * weights
	prios = loss + 1e-5
	loss = loss.mean()

	optimizer.zero_grad()
	loss.backward()
	replay_buffer.update_priorities(indices, prios.data.cpu().numpy())
	optimizer.step()

	return loss


def plot(frame_idx, rewards, losses):
	plt.figure(figsize=(20, 5))
	plt.subplot(131)
	plt.title('frame %s. reward: %s' % (frame_idx, np.mean(rewards[-10:])))
	plt.plot(rewards)
	plt.subplot(132)
	plt.title('loss')
	plt.plot(losses)
	plt.show()


## Init
env = ChessEnv(Game('black-auto'))
env = wrap_pytorch(env)

try:
	current_model = pickle.load(open("current_model.pkl", "rb"))
	target_model = pickle.load(open("target_model.pkl", "rb"))
except:
	current_model = CnnDQN(env.observation_space.shape, env.action_space.n)
	target_model = CnnDQN(env.observation_space.shape, env.action_space.n)

if USE_CUDA:
	current_model = current_model.cuda()
	target_model = target_model.cuda()

optimizer = optim.Adam(current_model.parameters(), lr=0.0001)

replay_initial = 5000
replay_buffer = PrioritizedReplayBuffer(10000, 0.5)

update_target(current_model, target_model)


## Parameters
epsilon_start = 1.0
epsilon_final = 0.01
epsilon_decay = 30000

beta_start = 0.4
beta_frames = 100000

def epsilon_by_frame(frame_idx): 
	return epsilon_final + (epsilon_start - epsilon_final) * math.exp(-1. * frame_idx / epsilon_decay)

def beta_by_frame(frame_idx): 
	return min(1.0, beta_start + frame_idx * (1.0 - beta_start) / beta_frames)

## Training
num_frames = 1000000
batch_size = 32
gamma = 0.99

losses = []
all_rewards = []
episode_reward = 0

legal_moves = 0
games_played = 0
finished_games = 0
percent_legal = 0
episode_moves = 0

state = env.reset()
for frame_idx in range(1, num_frames + 1):
	epsilon = epsilon_by_frame(frame_idx)

	with torch.no_grad():  # TODO: Do I need this in other places as well?
		action = current_model.act(state, epsilon)

		next_state, reward, done, info = env.step(action)
		replay_buffer.push(state, action, reward, next_state, done)

		state = next_state
		episode_reward += reward
		episode_moves += 1

		if info == 'legal':
			legal_moves += 1
			percent_legal = ((episode_moves-1)*percent_legal + 1) / episode_moves
		else:
			percent_legal = percent_legal - percent_legal / episode_moves

		if done or (percent_legal < 0.01 and episode_moves > 1000):
			state = env.reset()
			all_rewards.append(episode_reward)
			episode_reward = 0
			episode_moves = 0
			games_played += 1
			if done:
				finished_games += 1

	if len(replay_buffer) > replay_initial:
		beta = beta_by_frame(frame_idx)
		loss = compute_td_loss(batch_size, beta)
		losses.append(loss.data.item())

	if frame_idx % 10000 == 0:
		pickle.dump(current_model, open("current_model.pkl", "wb"))
		pickle.dump(target_model, open("target_model.pkl", "wb"))
	# 	plot(frame_idx, all_rewards, losses)

	if frame_idx % 1000 == 0:
		update_target(current_model, target_model)
		frames_per_game = round(frame_idx / games_played, 2) if games_played != 0 else np.nan
		print("{} frames: {} games have been played ({} frames per game), {} moves were legal ({}%).".format(
			frame_idx, games_played, frames_per_game, legal_moves, round(100 * legal_moves / frame_idx, 2)
		))

pickle.dump(current_model, open("current_model.pkl", "wb"))
pickle.dump(target_model, open("target_model.pkl", "wb"))
plot(frame_idx, all_rewards, losses)

