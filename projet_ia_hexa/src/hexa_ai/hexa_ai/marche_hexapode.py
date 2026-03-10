import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
from setuptools import setup, find_packages


class HexapodController(Node):
    def __init__(self):
        super().__init__('marche_hexapode')

        # dictionnaire pour stocker les publishers de chaque joint
        self.joint_publishers = {}

        # liste de tous les joints à contrôler
        self.joints = [
            "joint_buste_coxa_arriere_droite",
            "joint_coxa_femur_arriere_droite",
            "joint_femur_tibia_arriere_droite",
            "joint_tibia_tarse_arriere_droite",

            "joint_buste_coxa_milieu_droite",
            "joint_coxa_femur_milieu_droite",
            "joint_femur_tibia_milieu_droite",
            "joint_tibia_tarse_milieu_droite",

            "joint_buste_coxa_avant_droite",
            "joint_coxa_femur_avant_droite",
            "joint_femur_tibia_avant_droite",
            "joint_tibia_tarse_avant_droite",

            "joint_buste_coxa_arriere_gauche",
            "joint_coxa_femur_arriere_gauche",
            "joint_femur_tibia_arriere_gauche",
            "joint_tibia_tarse_arriere_gauche",

            "joint_buste_coxa_milieu_gauche",
            "joint_coxa_femur_milieu_gauche",
            "joint_femur_tibia_milieu_gauche",
            "joint_tibia_tarse_milieu_gauche",

            "joint_buste_coxa_avant_gauche",
            "joint_coxa_femur_avant_gauche",
            "joint_femur_tibia_avant_gauche",
            "joint_tibia_tarse_avant_gauche",
        ]

        # création des publishers pour chaque joint
        for joint in self.joints:
            topic_name = f"/{joint}_position_controller/command"
            self.joint_publishers[joint] = self.create_publisher(Float64, topic_name, 10)

        # timer pour envoyer les commandes de marche
        self.timer = self.create_timer(0.1, self.step)  # 10 Hz

        # phase du pas pour le mouvement
        self.step_phase = 0

    def step(self):
        # simple gait cyclique (tripod-like)
        angle = 0.5 * math.sin(self.step_phase)

        for i, joint in enumerate(self.joints):
            msg = Float64()
            # alternance droite/gauche pour tripod gait
            msg.data = angle if i % 2 == 0 else -angle
            self.joint_publishers[joint].publish(msg)

        self.step_phase += 0.1

def main(args=None):
    rclpy.init(args=args)
    node = HexapodController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()