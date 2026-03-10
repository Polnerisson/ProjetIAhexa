#!/bin/bash

# --- Construction du WorkSpace ---
rm -rf build install log

# --- 1️⃣ Construire le workspace si nécessaire ---
if [ ! -f install/setup.bash ]; then
    echo "Workspace non construit. Construction en cours..."
    colcon build --symlink-install
    if [ $? -ne 0 ]; then
        echo "Erreur lors du build. Corrige par ce que c'est pas ouf ton code vérifie que tu as bien sourcé "
        exit 1
    fi
fi

# --- 2️⃣ Exporter les variables pour Gazebo et ROS 2 ---
export LD_LIBRARY_PATH=/opt/ros/jazzy/lib:$LD_LIBRARY_PATH
export GZ_SYSTEM_PLUGIN_PATH=~/Desktop/Projet_Hexa/projet_ia_hexa/gz_plugins
export GZ_SIM_RESOURCE_PATH=~/Desktop/Projet_Hexa/projet_ia_hexa/install/hexa_description/share:$GZ_SIM_RESOURCE_PATH

# --- 3️⃣ Sourcer ROS 2 et workspace ---
source /opt/ros/jazzy/setup.bash
source ~/Desktop/Projet_Hexa/projet_ia_hexa/install/setup.bash

# --- 4️⃣ Lancer le robot ---
echo "Lancement du hexapode dans Gazebo..."
ros2 launch hexa_description spawn_hexapode.launch.py