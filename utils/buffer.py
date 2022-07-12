import numpy as np
import os
from .utils import plot_curve

class ReplayBuffer():
    def __init__(self, max_size, input_shape, n_actions) -> None:
        self.mem_size = max_size
        self.mem_cntr = 0
        self.state_memory = np.zeros((self.mem_size, input_shape))
        self.next_state_memory = np.zeros((self.mem_size, input_shape))
        self.action_memory = np.zeros((self.mem_size, n_actions))
        self.reward_memory = np.zeros(self.mem_size)
        self.terminal_memory = np.zeros(self.mem_size, dtype = np.bool)
    
    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.next_state_memory[index] = state_
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = done

        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)

        batch = np.random.choice(max_mem, batch_size)

        states = self.state_memory[batch]
        states_ = self.next_state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        dones = self.terminal_memory[batch]

        return states, actions, rewards, states_, dones

class Info():
    def __init__(self, board_structure, num_turrent, output_dir = 'results/') -> None:
        self.board = board_structure
        self.num_turrent = num_turrent
        self.timestamp = 0

        self.position_t = []
        self.action_t = []
        self.data_collected_t = []
        self.data_left_t = []
        self.data_collect_rate_t = []

        self.output_dir = output_dir
        self.num_plots = 0
        

    def store(self, position_t, action_t, data_collected_t, data_left_t, data_collect_rate_t):
        self.timestamp += 1
        self.position_t.append(position_t)
        self.action_t.append(action_t)

        self.data_collected_t.append(data_collected_t)
        self.data_left_t.append(data_left_t)
        self.data_collect_rate_t.append(data_collect_rate_t)

    def save(self):
        data_collected = np.array(self.data_collected_t).T.tolist()
        data_left = np.array(self.data_left_t).T.tolist()
        data_collect_rate = np.array(self.data_collect_rate_t).T.tolist()

        print(len(data_collected))
        self.plot(type='data_collected/', data=data_collected)
        self.plot(type='data_left/', data=data_left)
        self.plot(type='data_collect_rate/', data=data_collect_rate)

        with open(self.output_dir + 'position_t.txt', 'w') as f:
            timestamp = 0
            for line in self.position_t:
                f.write(str(timestamp) + ' ' + str(line[0]) + '  ' + str(line[1]))
                f.write('\n')
                timestamp += 1

    def plot(self, type, data):
        self.mkdir(type)
        t = [i+1 for i in range(self.timestamp)]
        for i in range(self.num_turrent):
            self.num_plots += 1
            plot_curve(t, data[i], self.filename(type=type, turrent=i), self.num_plots)

    def filename(self, type, turrent):
        return self.output_dir + type + str(turrent) + '.png'

    def mkdir(self, path):
        isExist = os.path.exists(self.output_dir + path)
        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(self.output_dir + path)
            # print("The new directory is created!")

    def reset(self):
        self.position_t = []
        self.action_t = []
        self.data_collected_t = []
        self.data_left_t = []
        self.data_collect_rate_t = []
