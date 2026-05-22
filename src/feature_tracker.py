import cv2
import numpy as np


class FeatureTracker:
    def __init__(self):
        self.fast = cv2.FastFeatureDetector_create(threshold=25)

        self.fx = 525.0
        self.fy = 525.0
        self.cx = 319.5
        self.cy = 239.5
        self.scale = 5000.0

    def load_rgbd(self, rgb_path, depth_path):
        rgb = cv2.imread(rgb_path)
        depth = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)

        if rgb is None:
            raise FileNotFoundError(f"RGB não encontrado: {rgb_path}")

        if depth is None:
            raise FileNotFoundError(f"Depth não encontrado: {depth_path}")

        return rgb, depth

    def process(self, rgb1_path, depth1_path, rgb2_path, depth2_path):
        rgb1, depth1 = self.load_rgbd(rgb1_path, depth1_path)
        rgb2, depth2 = self.load_rgbd(rgb2_path, depth2_path)

        gray1 = cv2.cvtColor(rgb1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(rgb2, cv2.COLOR_BGR2GRAY)

        keypoints = self.fast.detect(gray1, None)

        if not keypoints:
            empty = np.array([])
            return rgb2, empty, empty, empty, empty, empty

        fast_points = np.array([kp.pt for kp in keypoints], dtype=np.float32)

        tracked_points, status, _ = cv2.calcOpticalFlowPyrLK(
            gray1,
            gray2,
            fast_points,
            None,
            winSize=(21, 21),
            maxLevel=3,
            criteria=(
                cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                30,
                0.01
            )
        )

        if tracked_points is None or status is None:
            empty = np.array([])
            return rgb2, fast_points, empty, empty, empty, empty

        status = status.flatten()

        points1 = fast_points[status == 1]
        points2 = tracked_points[status == 1]

        source, target = self.project_to_3d(
            points1,
            points2,
            depth1,
            depth2
        )

        return rgb2, fast_points, points1, points2, source, target

    def pixel_to_3d(self, point, depth):
        u, v = point

        u = int(round(u))
        v = int(round(v))

        height, width = depth.shape

        if u < 0 or u >= width or v < 0 or v >= height:
            return None

        z = depth[v, u] / self.scale

        if z <= 0:
            return None

        x = (u - self.cx) * z / self.fx
        y = (v - self.cy) * z / self.fy

        return np.array([x, y, z], dtype=np.float64)

    def project_to_3d(self, points1, points2, depth1, depth2):
        source = []
        target = []

        for p1, p2 in zip(points1, points2):
            point3d_1 = self.pixel_to_3d(p1, depth1)
            point3d_2 = self.pixel_to_3d(p2, depth2)

            if point3d_1 is not None and point3d_2 is not None:
                source.append(point3d_1)
                target.append(point3d_2)

        return np.array(source), np.array(target)