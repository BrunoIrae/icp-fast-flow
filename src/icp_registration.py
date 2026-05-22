import numpy as np


class ICPRegistration:
    @staticmethod
    def align(source, target):
        centroid_source = np.mean(source, axis=0)
        centroid_target = np.mean(target, axis=0)

        source_centered = source - centroid_source
        target_centered = target - centroid_target

        H = source_centered.T @ target_centered

        U, _, Vt = np.linalg.svd(H)

        R = Vt.T @ U.T

        if np.linalg.det(R) < 0:
            Vt[-1, :] *= -1
            R = Vt.T @ U.T

        t = centroid_target - R @ centroid_source

        aligned = (R @ source.T).T + t

        error = np.mean(
            np.linalg.norm(aligned - target, axis=1)
        )

        return aligned, error, t