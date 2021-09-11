import cv2
import math


class BodyPoseDraw(object):

    def __init__(self):
        self.color_1 = (0, 0, 255)
        self.color_2 = (0, 255, 0)
        self.thickness = 2

    def draw_center_point(self, image, landmark_px, pose_size):
        image_height, image_width, _ = image.shape
        landmark_px = self._normalized_to_pixel_coordinates(landmark_px[0], landmark_px[1], image_width, image_height)
        pose_size = math.floor(pose_size * image_height)
        cv2.circle(image, landmark_px, 6, self.color_1, -1)
        cv2.circle(image, landmark_px, pose_size, self.color_2, self.thickness)

    def _normalized_to_pixel_coordinates(self, normalized_x, normalized_y, image_width, image_height):
        """Converts normalized value pair to pixel coordinates."""

        # Checks if the float value is between 0 and 1.
        def is_valid_normalized_value(value: float) -> bool:
            return (value > 0 or math.isclose(0, value)) and (value < 1 or math.isclose(1, value))

        if not (is_valid_normalized_value(normalized_x) and is_valid_normalized_value(normalized_y)):
            return None
        x_px = min(math.floor(normalized_x * image_width), image_width - 1)
        y_px = min(math.floor(normalized_y * image_height), image_height - 1)
        return x_px, y_px

    def draw_landmarks(self, image, landmarks, connections=None):
        """Draws the landmarks and the connections on the image.
        Args:
          image: A three channel RGB image represented as numpy ndarray.
          landmarks: A normalized landmark numpy array
          connections: A list of landmark index tuples that specifies how landmarks to be connected in the drawing.
        Raises:
          ValueError: If one of the followings:
            a) If the input image is not three channel RGB.
            b) If any connetions contain invalid landmark index.
        """
        if image.shape[2] != 3:
            raise ValueError('Input image must contain three channel rgb data.')
        image_rows, image_cols, _ = image.shape
        idx_to_coordinates = {}
        for idx in range(33):
            landmark_px = self._normalized_to_pixel_coordinates(landmarks[idx][0], landmarks[idx][1], image_cols, image_rows)
            if landmark_px and landmarks[idx][2] > 0.9:
                idx_to_coordinates[idx] = landmark_px
        if connections:
            num_landmarks = 33
            # Draws the connections if the start and end landmarks are both visible.
            for connection in connections:
                start_idx = connection[0]
                end_idx = connection[1]
                if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
                    raise ValueError(f'Landmark index is out of range. Invalid connection '
                                     f'from landmark #{start_idx} to landmark #{end_idx}.')
                if start_idx in idx_to_coordinates and end_idx in idx_to_coordinates:
                    cv2.line(image, idx_to_coordinates[start_idx], idx_to_coordinates[end_idx], (0, 255, 0), 2)

        # Draws landmark points after finishing the connection lines, which is aesthetically better.
        for landmark_px in idx_to_coordinates.values():
            cv2.circle(image, landmark_px, 2, (255, 0, 0), 2)
