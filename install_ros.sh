#!/bin/bash

sudo apt install -y python3 python3-dev python3-pip build-essential python3-rosdep2 python3-rosinstall python3-rosinstall-generator
sudo pip3 install --upgrade rosdep rospkg rosinstall_generator rosinstall wstool vcstools catkin_tools catkin_pkg  

sudo rosdep init
rosdep update

prv=`pwd`
mkdir $HOME/dev/ros -p && cd $HOME/dev/ros
export ROS_PYTHON_VERSION=3
catkin config --init -DCMAKE_BUILD_TYPE=Release --blacklist rqt_rviz rviz_plugin_tutorials librviz_tutorial --install

rosinstall_generator desktop --rosdistro melodic --deps --tar > melodic-desktop.rosinstall
wstool init -j8 src melodic-desktop.rosinstall
wstool update -j4 -t src
pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython

cd $prv
python3 install_ros_deps.py -p $HOME/dev/ros/src
cd $HOME/dev/ros

catkin build -DPYTHON_VERSION=3.6 -DPYTHON_EXECUTABLE=/usr/bin/python3
source ~/dev/ros/install/setup.bash

