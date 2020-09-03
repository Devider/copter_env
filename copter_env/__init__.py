from gym.envs.registration import register

register(
    id='copter-v0',
    max_episode_steps=20000,
    entry_point='copter_env.envs:CopterEnv',
)