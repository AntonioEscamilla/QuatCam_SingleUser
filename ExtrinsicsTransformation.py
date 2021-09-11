import numpy as np
from scipy.spatial.transform import Rotation as R


def transform_translation(T_cam, R_newRef, T_NewRef):
    r = R.from_matrix(R_newRef)
    inv_r = r.inv()
    T_cam = T_cam.reshape((3,))
    T_NewRef = T_NewRef.reshape((3,))
    return inv_r.apply(T_cam - T_NewRef)


def transform_rotation(R_cam, R_newRef):
    R_cam = R.from_matrix(R_cam)
    R_newRef = R.from_matrix(R_newRef)
    inv_R_newRef = R_newRef.inv()
    out_quat = multiply_quaternions(inv_R_newRef.as_quat(), R_cam.as_quat())
    out_R = R.from_quat(out_quat)
    return out_R.as_matrix()


def multiply_quaternions(a, b):            # quat in form [x, y, z, w]
    return np.asarray([a[3] * b[0] + a[0] * b[3] + a[1] * b[2] - a[2] * b[1],
                       a[3] * b[1] - a[0] * b[2] + a[1] * b[3] + a[2] * b[0],
                       a[3] * b[2] + a[0] * b[1] - a[1] * b[0] + a[2] * b[3],
                       a[3] * b[3] - a[0] * b[0] - a[1] * b[1] - a[2] * b[2]])
