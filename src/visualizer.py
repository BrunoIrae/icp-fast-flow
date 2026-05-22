import cv2
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self):
        self.window_name = "FAST + Optical Flow"

        plt.ion()

        self.fig = plt.figure(
            "ICP 3D + Trajetoria",
            figsize=(9, 8)
        )

        self.ax = self.fig.add_subplot(
            111,
            projection="3d"
        )

    def show(
        self,
        rgb,
        fast_points,
        points1,
        points2,
        aligned,
        target,
        trajectory,
        frame_index,
        error
    ):
        image = rgb.copy()

        # FAST em amarelo
        for point in fast_points[:400]:
            x, y = point.astype(int)

            cv2.circle(
                image,
                (x, y),
                2,
                (0, 255, 255),
                -1
            )

        # Optical Flow em verde/azul
        for p1, p2 in zip(points1[:120], points2[:120]):
            x1, y1 = p1.astype(int)
            x2, y2 = p2.astype(int)

            cv2.circle(
                image,
                (x2, y2),
                3,
                (0, 255, 0),
                -1
            )

            cv2.line(
                image,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                1
            )

        cv2.putText(
            image,
            "FAST + Optical Flow",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        cv2.putText(
            image,
            f"Frame: {frame_index}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            f"Erro ICP: {error:.6f}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            f"Pares 3D: {len(target)}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            "Amarelo: FAST",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        cv2.putText(
            image,
            "Verde/Azul: Optical Flow",
            (20, 190),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.imshow(self.window_name, image)

        self.update_3d(
            aligned,
            target,
            trajectory
        )

        key = cv2.waitKey(30) & 0xFF

        return key != ord("q")

    def update_3d(self, aligned, target, trajectory):
        self.ax.clear()

        self.ax.scatter(
            target[:, 0],
            target[:, 1],
            target[:, 2],
            s=1,
            c="blue",
            label="Alvo"
        )

        self.ax.scatter(
            aligned[:, 0],
            aligned[:, 1],
            aligned[:, 2],
            s=1,
            c="green",
            label="ICP alinhado"
        )

        if trajectory is not None and len(trajectory) > 1:
            self.ax.plot(
                trajectory[:, 0],
                trajectory[:, 1],
                trajectory[:, 2],
                c="red",
                linewidth=2,
                label="Trajetoria estimada"
            )

            self.ax.scatter(
                trajectory[-1, 0],
                trajectory[-1, 1],
                trajectory[-1, 2],
                c="red",
                s=40
            )

        self.ax.set_title("Registro 3D ICP + Trajetoria")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.legend()

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def close(self):
        cv2.destroyAllWindows()
        plt.close(self.fig)