import cv2

from brain.base_brain import BaseBrain
from game.clash_royal import ClashRoyal
from utils.c_lib_utils import convert2pymat, STATE_DICT

if __name__ == '__main__':

    # address = "http://127.0.0.1:35013/device/cd9faa7f/video.flv"
    # address = "./scan/s1.mp4"
    address = "http://127.0.0.1:46539/device/cd9faa7f/video.flv"
    capture = cv2.VideoCapture(address)
    cv2.namedWindow('image')

    i = 0

    root = "../vysor/"

    clash_royal = ClashRoyal(root)

    base_brain = BaseBrain(clash_royal.n_loc_x_actions,
                           clash_royal.n_loc_y_actions,
                           clash_royal.n_card_actions,
                           clash_royal.img_shape,
                           clash_royal.state_shape)

    while True:
        i += 1
        state, img = capture.read()

        if state:
            img = cv2.resize(img, (540, 960))
            cv2.imshow('image', img)
            cv2.waitKey(1)

            if i % 10 != 0:
                continue

            pymat = convert2pymat(img)

            observation = clash_royal.frame_step(img)
            if observation is not None:
                action = base_brain.choose_action(observation[1:])
                clash_royal.step(observation[0], action)

            if clash_royal.game_start and clash_royal.game_finish:
                base_brain.store_transition(clash_royal.episode_statistics())
                base_brain.learn()


        else:
            break

    cv2.destroyAllWindows()
