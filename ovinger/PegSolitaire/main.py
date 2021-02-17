from reinforcement_learner import ReinfocementLearner
from config import config

def main():
    rl = ReinfocementLearner(config)
    rl.train()
    rl.show_learning_graph()
    rl.show_reward_graph()
    rl.play_game()

if __name__ == '__main__':
    main()