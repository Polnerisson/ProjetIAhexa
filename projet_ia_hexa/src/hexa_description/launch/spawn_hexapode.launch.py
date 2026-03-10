from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_path = get_package_share_directory('hexa_description')

    urdf_file = os.path.join(pkg_path, 'urdf', 'hexapode.urdf')
    world_file = '/home/mecadec/Desktop/Projet_Hexa/projet_ia_hexa/worlds/my_world.world'

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([

        DeclareLaunchArgument(
            'world',
            default_value=world_file
        ),

        ExecuteProcess(
            cmd=['gz', 'sim', '-r', LaunchConfiguration('world')],
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}],
            output='screen'
        ),

        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-topic', 'robot_description',
                '-name', 'hexapode',
                '-x', '0.0',
                '-y', '0.0',
                '-z', '0.25'  
            ],
            output='screen'
        ),

        Node(
            package='hexa_ai',
            executable='marche_hexapode',
            output='screen'
        )
    ])