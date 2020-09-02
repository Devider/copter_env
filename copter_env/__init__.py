from gym.envs.registration import register

register(
    id='copter-v0',
    entry_point='copter_env.envs:CopterEnv',
)