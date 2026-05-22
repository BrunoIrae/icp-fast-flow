from pathlib import Path
import numpy as np

from feature_tracker import FeatureTracker
from icp_registration import ICPRegistration
from visualizer import Visualizer


RGB_FOLDER = "../dataset/rgb"
DEPTH_FOLDER = "../dataset/depth"


def main():
    rgb_files = sorted(Path(RGB_FOLDER).glob("*.png"))
    depth_files = sorted(Path(DEPTH_FOLDER).glob("*.png"))

    if len(rgb_files) < 2 or len(depth_files) < 2:
        raise RuntimeError("Dataset insuficiente. Verifique as pastas rgb e depth.")

    limit = min(len(rgb_files), len(depth_files))

    tracker = FeatureTracker()
    viewer = Visualizer()

    trajectory = []
    position = np.zeros(3)

    try:
        for i in range(limit - 1):
            rgb1 = str(rgb_files[i])
            depth1 = str(depth_files[i])

            rgb2 = str(rgb_files[i + 1])
            depth2 = str(depth_files[i + 1])

            (
                image,
                fast_points,
                points1,
                points2,
                source,
                target
            ) = tracker.process(
                rgb1,
                depth1,
                rgb2,
                depth2
            )

            if len(source) < 10:
                continue

            aligned, error, translation = ICPRegistration.align(
                source,
                target
            )

            position += translation
            trajectory.append(position.copy())

            trajectory_array = np.array(trajectory)

            print(
                f"Frame: {i} | "
                f"FAST: {len(fast_points)} | "
                f"Flow: {len(points1)} | "
                f"Pares 3D: {len(source)} | "
                f"Erro: {error:.6f}"
            )

            running = viewer.show(
                image,
                fast_points,
                points1,
                points2,
                aligned,
                target,
                trajectory_array,
                i,
                error
            )

            if not running:
                break

    finally:
        viewer.close()


if __name__ == "__main__":
    main()