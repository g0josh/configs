#!/bin/bash

echo "Make sure you clone the repo www.github.com/g0josh/configs.git and run this script inside the folder 'configs'"
read -p 'Continue[y/n] :' cont
if [ "$cont" == "n" ]; then
	exit 1
fi
read -p 'Office(1) or Home(0): ' office

sudo pacman -Syu xorg-server xorg-xset xorg-xrandr mpd mpc ranger code qtile firefox rxvt-unicode uget transmission-gtk ncmpcpp vim tmux git openssh
echo ""
echo "---------------------------------------"
echo "Installing yay"
echo "---------------------------------------"
echo ""

echo ""
echo "---------------------------------------"
echo "Installing Qtile"
echo "---------------------------------------"
echo ""
sudo apt-get install libpangocairo-1.0-0
pip3 install xcffib cairocffi qtile

# Misc
sudo apt install rxvt-unicode ranger 

curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt-get install apt-transport-https

wget -qO- https://deb.opera.com/archive.key | sudo apt-key add -
sudo add-apt-repository "deb [arch=i386,amd64] https://deb.opera.com/opera-stable/ stable non-free"


sudo add-apt-repository ppa:codejamninja/jam-os

sudo apt update
sudo apt install opera-stable code i3lock-color tmux

if [ "$office" == "1" ]; then
    echo "-----------------------------------------------"
    echo "Installing Office tools only..."
    echo "-----------------------------------------------"
else
    echo "-----------------------------------------------"
    echo "Installing home tools..."
    echo "-----------------------------------------------"
    curl -s https://syncthing.net/release-key.txt | sudo apt-key add -
    echo "deb https://apt.syncthing.net/ syncthing stable" | sudo tee /etc/apt/sources.list.d/syncthing.list
    sudo apt install syncthing transmission uget mpd nomacs ncmpcpp numlockx
    sudo dpkg -i ./resemsmice_1.1.3_amd64.deb
    cp ./.Xsession ~/
fi

echo ""
echo "---------------------------------------"
echo "Setting up configs"
echo "---------------------------------------"
echo ""

git checkout sweet
git pull
mkdir ~/.config/qtile
mkdir ~/.config/ranger
cp ./.config/qtile/* ~/.config/qtile/
sudo cp qtile.desktop /usr/share/xsessions
cp ./.config/ranger/* ~/.config/ranger/
cp ./.config/compton.conf ~/.config/compton.conf
cp ./.Xresources ~/
cp ./.bashrc ~/
cp ./.tmux.conf ~/
cp ./.vimrc ~/
sudo cp ./Iosevka* /usr/local/share/fonts/
sudo cp ./Font\ Awesome* /usr/local/share/fonts/
fc-cache -fv
cp ./Wallpaper ~/Pictures/

sudo apt autoremove
echo "Please install NVIDIA drivers next"
