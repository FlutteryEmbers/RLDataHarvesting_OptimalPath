# from trainer.DDQN.ddqn_main import DDQN_GameAgent
from trainer.DDQN_HER import HER_Basic_Trainer
from utils import tools, graphic
from loguru import logger

def init_working_dir():
    tools.mkdir('model/q_networks')
    tools.mkdir('model/ppo')
    tools.mkdir('model/her_q_networks')

def ddqn():
    logger.critical('Start DDQN Session')
    config = tools.load_config("configs/config_ddqn.yaml")
    tools.setup_seed(config['RANDOM_SEED'])
    ## network: trainning algorithm using: MLP/CNN network 
    agent = DDQN_GameAgent(config=config, network='MLP')

    ## trainning_mode:
    ## - Default: Trainning for a specific environment;
    ## - DR: Trainning with randomized initial states
    agent.train(env_type='Default', n_games=1000)
    # agent.evaluate(env_type='Default')
    # agent.train(env_type='DR', n_games=10000)
    # agent.evaluate(env_type='DR')

def her_ddqn():
    logger.critical('Start HER_DDQN Session')
    config = tools.load_config("configs/config_ddqn.yaml")
    tools.setup_seed(config['RANDOM_SEED'])
    ## network: trainning algorithm using: MLP/CNN network 
    agent = HER_Basic_Trainer.GameAgent(config=config, network='MLP')
    agent.train(env_type='Default', n_games=2000)
    # agent.evaluate(env_type='Default')
    # agent.batch_evaluation(env_type='Default')
    # agent.batch_train('Default')

if __name__ == '__main__':
    tools.set_logger_level(3)
    init_working_dir()
    # ddqn()
    her_ddqn()
    # ddpg()
    # sac()
    # graphic.plot_result_path(x_limit=10, y_limit=10, tower_locations=[[0, 1], [4, 7], [9, 3]], paths=[[0, 0], [1, 2], [2, 3], [7, 9]])

    
   