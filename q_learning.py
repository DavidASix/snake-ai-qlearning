import numpy as np
import pickle
from datetime import datetime
from game.game import Game 

class QLearning:
    def __init__(self, game, learning_rate=0.5, discount_factor=0.6, exploration_rate=0.9):
        self.game = game
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}

    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

    def get_action(self, state):
        if np.random.uniform(0, 1) < self.exploration_rate:
            # Assuming the game has a method to get all possible actions
            return np.random.choice(self.game.get_possible_actions())
        else:
            if state in self.q_table:
                return np.argmax(self.q_table[state])
            else:
                return np.random.choice(self.game.get_possible_actions())

    def update_q_table(self, old_state, action, reward, new_state):
        old_value = self.q_table.get((old_state, action), None)
        if old_value is None:
            self.q_table[(old_state, action)] = reward
        else:
            max_q_value_new_state = max([self.q_table.get((new_state, a), 0) for a in self.game.get_possible_actions()])
            new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * max_q_value_new_state)
            self.q_table[(old_state, action)] = new_value

    def train(self, episodes):
        for episode in range(episodes):
            self.game.reset()
            state = self.game.get_state()
            done = False
            while not done:
                action = self.get_action(state)
                print(f'Trying Action {action}')
                next_state, reward, done = self.game.step(action)
                self.update_q_table(state, action, reward, next_state)
                state = next_state
            self.save_model(f'./snake-ai_{episodes}-episodes-{datetime.now().strftime("%Y-%m-%d-%H:%M")}.pkl')

game = Game()
q_learning = QLearning(game)
# Train the QLearning for n instances
q_learning.train(50)