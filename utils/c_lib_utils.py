import ctypes

MENU_STATE = 0

RUNNING_STATE = 1

FINISH_STATE = 2

ERROR_STATE = 3

STATE_DICT = {"MENU_STATE": 0,
              "RUNNING_STATE": 1,
              "FINISH_STATE": 2,
              "ERROR_STATE": 3}


class PyMat(ctypes.Structure):
    _fields_ = [
        ('frame_data', ctypes.c_char_p),
        ('height', ctypes.c_int),
        ('width', ctypes.c_int),
        ('channel', ctypes.c_int),
    ]


class Result(ctypes.Structure):
    _fields_ = [
        ('game_state', ctypes.c_int),
        ('frame_state', ctypes.c_int),
        ('index', ctypes.c_int),
        ('is_grey', ctypes.c_bool),
        ('purple_loc', ctypes.c_int * 2),
        ('yellow_loc', ctypes.c_int * 2),
        ('opp_crown', ctypes.c_int),
        ('mine_crown', ctypes.c_int),
        ('card_type', ctypes.c_int * 4),
        ('available', ctypes.c_int * 4),
        ('prob', ctypes.c_float * 4),
        ('opp_hp', ctypes.c_float * 3),
        ('mine_hp', ctypes.c_float * 3),
        ('battle_result', ctypes.c_int),
        ('frame_index', ctypes.c_int),
        ('time', ctypes.c_int),
        ('remain_elixir', ctypes.c_int),
        ('milli', ctypes.c_float),
    ]


def convert2pymat(mat):
    py_mat = PyMat()
    py_mat.frame_data = mat.ctypes.data_as(ctypes.c_char_p)
    shape = mat.shape
    py_mat.height = ctypes.c_int(shape[0])
    py_mat.width = ctypes.c_int(shape[1])
    py_mat.channel = 1 if len(shape) == 2 else 3
    return py_mat
