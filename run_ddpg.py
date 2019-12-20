import time

import cv2

from brain.base_brain import BaseBrain
from device.emulator import Emulator
from device.mobile import Mobile
from game.clash_royal_env import ClashRoyalEnv

if __name__ == '__main__':

    i = 0

    # root = "/home/chengli/data/gym_data/clash_royal"
    root = "F:\\gym_data\\clash_royal"

    device_id = "cd9faa7f"
    # device_id = "127.0.0.1:62001"

    host_address = "http://127.0.0.1:2224/device/" + device_id + "/video.flv"

    device = Mobile(device_id, host_address)
    # device = Emulator(device_id, "夜神模拟器")

    host = ClashRoyalEnv(root, device, mode=ClashRoyalEnv.MODE["battle"], name="host")

    brain = PolicyGradient(host.img_shape, host.state_shape, BaseBrain.BrainType["runner"], "battle")

    while True:

        frame, state_code = device.get_frame()

        if frame is not None:
            host_observation = host.frame_step(frame)
            if host_observation is not None:
                host_action = brain.choose_action(host_observation)
                host.step(host_observation, host_action)

            if host.game_start and host.game_finish and host.retry <= 1:
                brain.load_model()
        else:
            if state_code == -1:
                print("没有信号")
