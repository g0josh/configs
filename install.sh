#!/bin/bash

echo "Make sure you clone the repo www.github.com/g0josh/configs.git and run this script inside the folder 'configs'"
read -p 'Continue[y/n] :' cont
if [ "$cont" == "n" ]; then
	exit 1
fi

echo ""
echo "---------------------------------------"
echo "Installing Qtile"
echo "---------------------------------------"
echo ""
sudo apt-get install libxcb-render0-dev libffi-dev libcairo2 python3-pip -y
pip3 install xcffib
pip3 install --no-cache-dir cairocffi
pip3 install qtile
sudo cp qtile.desktop /usr/share/xsessions/

echo ""
echo "---------------------------------------"
echo "Installing packages"
echo "---------------------------------------"
echo ""
sudo apt update
sudo apt install code tmux pavucontrol firefox rxvt-unicode imagemagick \
feh bc lm-sensors zsh lxappearance arandr rofi udiskie \
shotwell numlockx polybar neovim python3-opencv -y

echo ""
echo "---------------------------------------"
echo "Setting up configs"
echo "---------------------------------------"
echo ""
cp .config/qtile ~/.config/ -r
cp .config/polybar ~/.config/ -r
cp .config/autostart.sh ~/.config
sudo chmod u+x ~/.config/autostart.sh
cp .config/mpd ~/.config/ -r
cp .config/ncmpcpp ~/.config/ -r
cp .config/nvim ~/.config/ -r
cp .config/themes ~/.config/ -r
cp .config/picom ~/.config -r
cp .Xresources ~/
cp .tmux.conf ~/
cp .zshrc ~/
cp .zshenv ~/
cp .fonts ~/ -r
fc-cache -fv

echo ""
echo "---------------------------------------"
echo "Installing picom"
echo "---------------------------------------"
echo ""
sudo apt install libxext-dev libxcb1-dev libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev \
libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev libpixman-1-dev \
libdbus-1-dev libconfig-dev libgl1-mesa-dev libpcre2-dev libpcre3-dev libevdev-dev uthash-dev libev-dev libx11-xcb-dev ninja-build meson -y
mkdir $HOME/tools
cd $HOME/tools
git clone git@github.com:yshui/picom.git
cd picom
git submodule update --init --recursive
meson --buildtype=release . build
sudo ninja -C build install

echo ""
echo "---------------------------------------"
echo "Installing CLI tools"
echo "---------------------------------------"
echo ""
cd $HOME/tools
git clone git@github:g0josh/pycliutils
cd pycliutils
git checkout qtile
pip3 install .

echo ""
echo "---------------------------------------"
echo "Installing zsh theme"
echo "---------------------------------------"
echo ""
chsh -s $(which zsh)
cd $HOME/tools
git clone git@github.com:romkatv/powerlevel10k.git

echo ""
echo "---------------------------------------"
echo "Cleaning up"
echo "---------------------------------------"
echo ""
sudo apt autoremove
