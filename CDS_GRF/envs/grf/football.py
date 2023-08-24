from .. import MultiAgentEnv
import gfootball.env as football_env
from gfootball.env import observation_preprocessing
import gym
import numpy as np
from .state import State
from .encoders.encoder_basic import FeatureEncoder

def register_new_scenarios():
    import sys
    import pkgutil
    import os
    import importlib
    path=os.path.join(os.path.dirname(__file__),"scenarios")
    for _,module_name,_ in pkgutil.walk_packages(path=[path]):
        module=importlib.import_module("envs.grf.scenarios.{}".format(module_name))
        sys.modules["gfootball.scenarios.{}".format(module_name)]=module

class Football(MultiAgentEnv):

    def __init__(
        self,
        dense_reward=False,
        write_full_episode_dumps=False,
        write_goal_dumps=False,
        dump_freq=1000,
        render=False,
        n_agents=3,
        time_limit=150,
        time_step=0,
        obs_dim=26,
        env_name='academy_3_vs_1_with_keeper',
        stacked=False,
        representation="simple115",
        rewards='scoring',
        logdir='football_dumps',
        write_video=True,
        number_of_right_players_agent_controls=0,
        seed=0
    ):
        register_new_scenarios()
        
        self.dense_reward = dense_reward
        self.write_full_episode_dumps = write_full_episode_dumps
        self.write_goal_dumps = write_goal_dumps
        self.dump_freq = dump_freq
        self.render = render
        self.n_agents = n_agents
        self.episode_limit = time_limit
        self.time_step = time_step
        self.env_name = env_name
        self.stacked = stacked
        self.representation = representation
        self.rewards = rewards
        self.logdir = logdir
        self.write_video = write_video
        self.number_of_right_players_agent_controls = number_of_right_players_agent_controls
        self.seed = seed
        
        # may remove later
        assert self.representation=="raw"
        assert self.rewards=="scoring,checkpoints"

        self.env = football_env.create_environment(
            write_full_episode_dumps = self.write_full_episode_dumps,
            write_goal_dumps = self.write_goal_dumps,
            env_name=self.env_name,
            stacked=self.stacked,
            representation=self.representation,
            rewards=self.rewards,
            logdir=self.logdir,
            render=self.render,
            write_video=self.write_video,
            dump_frequency=self.dump_freq,
            number_of_left_players_agent_controls=self.n_agents,
            number_of_right_players_agent_controls=self.number_of_right_players_agent_controls,
            channel_dimensions=(observation_preprocessing.SMM_WIDTH, observation_preprocessing.SMM_HEIGHT))
        self.env.seed(self.seed)
        
        num_players_dict={
            "benchmark_academy_3_vs_1_with_keeper": 6,
            "benchmark_academy_corner": 22,
            "benchmark_academy_counterattack_easy": 22,
            "benchmark_academy_counterattack_hard": 22,
            "benchmark_academy_pass_and_shoot_with_keeper": 5,
            "benchmark_academy_run_pass_and_shoot_with_keeper": 5,
            "benchmark_full_game_5_vs_5_hard": 10,
            "benchmark_full_game_11_vs_11_hard": 22
        }
        
        self.num_players=num_players_dict[self.env_name]
        self.encoder=FeatureEncoder(num_players=self.num_players)

        self.action_space = [self.encoder.action_space for _ in range(self.n_agents)]
        self.observation_space = [self.encoder.observation_space for _ in range(self.n_agents)]
        self.global_state_space = self.encoder.global_state_space

        self.n_actions = self.action_space[0].n
        
        self.global_state_dim = self.global_state_space.shape[0]
        self.obs_dim = self.observation_space[0].shape[0]
        self.unit_dim = self.obs_dim  # QPLEX unit_dim  for cds_gfootball
        # self.unit_dim = 6  # QPLEX unit_dim set as that in Starcraft II

    def get_global_state(self):
        return self.global_state

    def step(self, actions):
        """Returns reward, terminated, info."""
        self.time_step += 1
        for state,action in zip(self.states,actions):
            state.update_action(action)
        
        raw_observations, rewards, done, infos = self.env.step(actions.to('cpu').numpy().tolist())
                
        score=raw_observations[0]["score"]
        
        for obs,state in zip(raw_observations,self.states):
            state.update_obs(obs)

        self.observations=self.encoder.encode(self.states)
        self.available_actions=self.observations[:,:self.get_total_actions()]
        self.global_state=self.encoder.get_global_state(self.states[0])

        if self.time_step >= self.episode_limit:
            done = True
        
        if done:
            diff=score[0]-score[1]
            if score[0]>score[1]:
                win=1
                lose=0
                draw=0
            elif score[0]==score[1]:
                win=0
                lose=0
                draw=1
            else:
                win=0
                lose=1
                draw=0
            infos["win"]=win
            infos["lose"]=lose
            infos["draw"]=draw
            infos["goal_diff"]=diff
            infos["my_goal"]=score[0]
        
        # official rewards should be shared, but checkpoint reward is assigned to individual.
        r=np.mean(rewards)*100

        return r, done, infos

    def get_obs(self):
        """Returns all agent observations in a list."""
        # obs = np.array([self.get_simple_obs(i) for i in range(self.n_agents)])
        return self.observations

    def get_obs_agent(self, agent_id):
        """Returns observation for agent_id."""
        return self.observations[agent_id]

    def get_obs_size(self):
        """Returns the size of the observation."""
        return self.obs_dim

    def get_state(self):
        """Returns the global state."""
        return self.get_global_state()

    def get_state_size(self):
        """Returns the size of the global state."""
        # TODO: in wrapper_grf_3vs1.py, author set state_shape=obs_shape
        return self.global_state_dim

    def get_avail_actions(self):
        """Returns the available actions of all agents in a list."""
        return self.available_actions

    def get_avail_agent_actions(self, agent_id):
        """Returns the available actions for agent_id."""
        return self.available_actions[agent_id]

    def get_total_actions(self):
        """Returns the total number of actions an agent could ever take."""
        return self.action_space[0].n

    def reset(self):
        """Returns initial observations and states."""
        self.time_step = 0
        self.states=[State() for i in range(self.n_agents)]
        
        raw_observations=self.env.reset()
        
        for raw_observation,state in zip(raw_observations,self.states):
            state.update_obs(raw_observation)
            
        self.observations=self.encoder.encode(self.states)
        self.available_actions=self.observations[:,:self.get_total_actions()]
        self.global_state=self.encoder.get_global_state(self.states[0])

        return self.get_obs(), self.get_global_state()

    def render(self):
        pass

    def close(self):
        self.env.close()

    def seed(self):
        pass

    def save_replay(self):
        """Save a replay."""
        pass

