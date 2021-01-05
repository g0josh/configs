#!/bin/bash

echo "Make sure you clone the repo www.github.com/g0josh/configs.git and run this script inside the folder 'configs'"
read -p 'Continue[y/n] :' cont
if [ "$cont" == "n" ]; then
	exit 1
fi

sudo apt install xorg udiskie curl alsa-utils build-essentials software-properties-common
sudo apt-add-repository non-free
sudo apt update
sudo apt install firmware-iwlwifi

echo ""
echo "---------------------------------------"
echo "Installing Qtile"
echo "---------------------------------------"
echo ""
sudo apt-get install libxcb-render0-dev libffi-dev libcairo2 python3-pip cmake -y
pip3 install xcffib
pip3 install --no-cache-dir cairocffi
pip3 install qtile


echo ""
echo "---------------------------------------"
echo "Installing Misc stuff"
echo "---------------------------------------"
echo ""

curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt-get install apt-transport-https

sudo apt update
sudo apt install code tmux pulseaudio pavucontrol firefox-esr rxvt-unicode imagemagick feh bc lm-sensors 


echo "-----------------------------------------------"
echo "Installing home tools..."
echo "-----------------------------------------------"
sudo apt install transmission uget mpd mpc nomacs ncmpcpp numlockx network-manager nvim
systemctl enable network-manager

echo ""
echo "---------------------------------------"
echo "Setting up configs"
echo "---------------------------------------"
echo ""
cp .config/qtile ~/.config/ -r
cp .config/autostart.sh ~/.config
sudo chmod u+x ~/.config/autostart.sh
cp .config/mpd ~/.config/ -r
cp .config/ncmpcpp ~/.config/ -r
cp .config/nvim ~/.config/ -r
cp .config/themes ~/.config/ -r
cp .config/picom/compton.conf ~/.config/picom/compton.conf
cp .profile ~/
cp .xinitrc ~/
cp .Xresources ~/
cp .bashrc ~/
cp .tmux.conf ~/
mkdir ~/.fonts
cp fonts/* ~/.fonts/
fc-cache -fv
mkdir $HOME/tools

echo ""
echo "---------------------------------------"
echo "Installing picom"
echo "---------------------------------------"
echo ""
sudo apt install libxext-dev libxcb1-dev libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev libpixman-1-dev libdbus-1-dev libconfig-dev libgl1-mesa-dev libpcre2-dev libpcre3-dev libevdev-dev uthash-dev libev-dev libx11-xcb-dev meson ninja-build
cd $HOME/tools
git clone https://github.com/yshui/picom.git
cd picom
git checkout next
git submodule update --init --recursive
meson --buildtype=release . build
sudo ninja -C build install

echo ""
echo "---------------------------------------"
echo "Installing CLI utils"
echo "---------------------------------------"
echo ""
cd $HOME/tools
git clone https://github.com/g0josh/pycliutils.git
cd pycliutils
pip3 install .

echo ""
echo "---------------------------------------"
echo "Cleaning up"
echo "---------------------------------------"
echo ""
sudo apt autoremove
