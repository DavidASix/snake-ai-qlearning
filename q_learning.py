import numpy as np
import pickle
from datetime import datetime
from game.game import Game 

class QLearning:
    def __init__(self, game, learning_rate=0.5, discount_factor=0.6, exploration_rate=0.9):
        self.game = game
        self.learning_rate = 0.2
        self.discount_factor = 0.9
        self.exploration_rate = 0.5
        self.q_table = {}
        self.high_score = 0

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
                next_state, reward, done, score = self.game.step(action, episode, slow=episode >= episodes-2)
                #print(f'Trying Action {action} -- Got Reward {reward}')
                self.update_q_table(state, action, reward, next_state)
                state = next_state
            #print(f'Score: {state[5]}')
            if score >= self.high_score and score > 3:
                self.high_score = score
                print(f'New high score: {self.high_score}')
        self.save_model(f'./snake-ai_{episodes}-episodes-{datetime.now().strftime("%Y-%m-%d-%H:%M")}.pkl')
        print(f'HIGH SCORE: {self.high_score}')

    def play_games(self, num_games=5):
        for episode in range(num_games):
            self.game.reset()
            state = self.game.get_state()
            done = False
            while not done:
                if state in self.q_table:
                    action = np.argmax(self.q_table[state])
                else:
                    action = np.random.choice(self.game.get_possible_actions())
                next_state, reward, done, score = self.game.step(action, episode, slow=True)
                state = next_state
            print(f'Score: {score}')

game = Game()
q_learning = QLearning(game)
# Train the QLearning for n instances
q_learning.train(15000)

#q_learning.load_model('snake-ai_3000-episodes-2024-03-05-20:18.pkl')
#q_learning.play_games()
