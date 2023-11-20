import time
from pywinauto.application import Application
from pywinauto import Desktop,keyboard

import os
import numpy as np
import imageio
from tqdm import tqdm
from stable_baselines3  import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from dino.ChromeDinoEnv import ChromeDinoEnv

def main():
    # app = Application(backend="uia").start(r"C:\Program Files\Google\Chrome\Application\chrome.exe --force-renderer-accessibility") 
    # app = Application(backend="uia").connect(title='New Tab - Google Chrome',timeout=5)
    # win=app.NewTabGoogleChrome
    # win.type_keys('chrome://dino/')
    # win.type_keys('{ENTER}')
    # win=app['chrome://dino/ - Network error - Google ChromePane']
    # while(True):
    #     time.sleep(3)
    #     win.capture_as_image().save('test.png')
    #     win.type_keys('{SPACE}')

    env_lambda = lambda: ChromeDinoEnv(
        screen_width=96,
        screen_height=96,
        chromedriver_path=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "dino",
            "chromedriver.exe"
        )
    )
    do_train = True
    num_cpu = 4
    save_path = "chrome_dino_ppo_cnn"
    env = SubprocVecEnv([env_lambda for i in range(num_cpu)])
    if do_train:
        checkpoint_callback = CheckpointCallback(
            save_freq=200000, 
            save_path='./dino/',
            name_prefix=save_path,
        )
        model = PPO(
            "MlpPolicy",
            env,
            verbose=1,
            tensorboard_log="./dino/",
        )
        model.learn(
            total_timesteps=2000000, 
            callback=[checkpoint_callback]
        )
        model.save(save_path)
    
    model = PPO.load(save_path, env=env)
    images = []
    obs = env.reset()
    img = model.env.render(mode='rgb_array')
    for i in tqdm(range(500)):
        images.append(img)
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = env.step(action)
        # env.render(mode='human')
        img = env.render(mode='rgb_array')

    imageio.mimsave('dino.gif', [np.array(img) for i, img in enumerate(images)], fps=15)
    exit()

if __name__ == '__main__':
    main()