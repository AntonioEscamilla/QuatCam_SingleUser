###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    MULTIPLE CAMERA CALIBRATION                      ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

from pymvg.camera_model import CameraModel
from pymvg.multi_camera_system import MultiCameraSystem
import math


def build_multi_camera_system(cameras):
    """Build a multi-camera system with pymvg package for triangulation
    Args:
        cameras: List of camera parameters
    Returns:
        cams_system: A multi-cameras system
    """
    pymvg_cameras = []
    for camera in cameras:
        camera = CameraModel.from_dict(camera, extrinsics_required=True)
        pymvg_cameras.append(camera)
    return MultiCameraSystem(pymvg_cameras)


def triangulate_frame_pose(camera_system, detections, videos_metadata):
    """
    Triangulate 3d points in world coordinates of multi-view 2d poses
    Args:
        camera_system: System of multiple cameras
        detections: List (size n) of ndarray (shape 33x3). n = len(cameras)
        videos_metadata: List of video metadata, each corresponding to a camera in the system
    Returns:
        all_frames_poses: All valid keypoints in world coordinates (dict: idx_to_coordinates format)
    """

    # read all cams and create list of dictionaries with 2d coordinates of valid keypoints
    list_valid_keypoints = []
    for cam_idx, metadata in enumerate(videos_metadata):
        keypoints_dict = valid_keypoints(detections[cam_idx], metadata['width'], metadata['height'])
        list_valid_keypoints.append(keypoints_dict)
    # for each keypoint create triangulation data with detected keypoints on each cam view
    pose3d_dict = {}
    for keypoint_idx in range(33):
        triangulation_data = []
        for cam_idx, keypoints_dict in enumerate(list_valid_keypoints):
            if keypoint_idx in keypoints_dict:
                triangulation_data.append((videos_metadata[cam_idx]['name'], keypoints_dict[keypoint_idx]))
        if len(triangulation_data) > 1:
            pose3d_dict[keypoint_idx] = camera_system.find3d(triangulation_data)

    return pose3d_dict


def valid_keypoints(landmarks, image_cols, image_rows):
    """Identify keypoints with high prediction confidence.
    Args:
        landmarks: A normalized landmark numpy array
        image_cols: pixels wide
        image_rows: pixels high
    Returns:
        idx_to_coordinates: Dictionary with existing keypoints (2d points) based on prediction confidence
    """
    idx_to_coordinates = {}
    for idx in range(33):
        landmark_px = normalized_to_pixel_coordinates(landmarks[idx][0], landmarks[idx][1], image_cols, image_rows)
        if landmark_px and landmarks[idx][2] > 0.9:
            idx_to_coordinates[idx] = landmark_px
    return idx_to_coordinates


def normalized_to_pixel_coordinates(normalized_x, normalized_y, image_width, image_height):
    """Converts normalized value pair to pixel coordinates."""
    # Checks if the float value is between 0 and 1.
    def is_valid_normalized_value(value: float) -> bool:
        return (value > 0 or math.isclose(0, value)) and (value < 1 or math.isclose(1, value))

    if not (is_valid_normalized_value(normalized_x) and is_valid_normalized_value(normalized_y)):
        return None
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px


def triangulate_poses(camera_system, detections, videos_metadata):
    """
    Triangulate 3d points in world coordinates of multi-view 2d poses
    Args:
        camera_system: System of multiple cameras
        detections: List (size n) of ndarray (shape kx33x3). n = len(cameras), k = number of frames
        videos_metadata: List of video metadata, each corresponding to a camera in the system
    Returns:
        all_frames_poses: List (size k) with all valid keypoints in world coordinates (dict: idx_to_coordinates format)
    """
    all_frames_poses = []
    for frame in range(detections[0].shape[0]):
        # read all cams and create list of dictionaries with 2d coordinates of valid keypoints
        list_valid_keypoints = []
        for cam_idx, metadata in enumerate(videos_metadata):
            keypoints_dict = valid_keypoints(detections[cam_idx][frame], metadata['width'], metadata['height'])
            list_valid_keypoints.append(keypoints_dict)

        # for each keypoint create triangulation data with detected keypoints on each cam view
        pose3d_dict = {}
        for keypoint_idx in range(33):
            triangulation_data = []
            for cam_idx, keypoints_dict in enumerate(list_valid_keypoints):
                if keypoint_idx in keypoints_dict:
                    triangulation_data.append((videos_metadata[cam_idx]['name'], keypoints_dict[keypoint_idx]))
            if len(triangulation_data) > 1:
                pose3d_dict[keypoint_idx] = camera_system.find3d(triangulation_data)

        all_frames_poses.append(pose3d_dict)
    return all_frames_poses