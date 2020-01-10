#!/bin/bash

echo "Make sure you clone the repo www.github.com/g0josh/configs.git and run this script inside the folder 'configs'"
read -p 'Continue[y/n] :' cont
if [ "$cont" == "n" ]; then
	exit 1
fi
read -p 'Office(1) or Home(0): ' office

sudo apt install xorg

echo ""
echo "---------------------------------------"
echo "Installing Qtile"
echo "---------------------------------------"
echo ""
sudo apt-get install libpangocairo-1.0-0
pip3 install xcffib cairocffi qtile

# Misc
sudo apt install software-properties-common
sudo apt install rxvt-unicode ranger 

curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt-get install apt-transport-https
sudo add-apt-repository ppa:codejamninja/jam-os

sudo apt update
sudo apt install code i3lock-color tmux

if [ "$office" == "1" ]; then
    echo "-----------------------------------------------"
    echo "Installing Office tools only..."
    echo "-----------------------------------------------"
    sudo cp qtile.desktop /usr/share/xsessions
else
    echo "-----------------------------------------------"
    echo "Installing home tools..."
    echo "-----------------------------------------------"
    curl -s https://syncthing.net/release-key.txt | sudo apt-key add -
    echo "deb https://apt.syncthing.net/ syncthing stable" | sudo tee /etc/apt/sources.list.d/syncthing.list
    sudo apt install syncthing transmission uget mpd nomacs ncmpcpp numlockx bcmwl-kernel-source network-manager
    sudo dpkg -i ./resemsmice_1.1.3_amd64.deb
    cp ./.profile ~/
    cp ./.xinitrc ~/
fi

echo ""
echo "---------------------------------------"
echo "Setting up configs"
echo "---------------------------------------"
echo ""

mkdir ~/.config/qtile
mkdir ~/.config/ranger
cp ./.config/qtile/* ~/.config/qtile/
cp ./.config/ranger/* ~/.config/ranger/
cp ./.config/compton.conf ~/.config/compton.conf
cp ./.config/nvim ~/.config/nvim -r
cp ./.Xresources ~/
cp ./.bashrc ~/
cp ./.tmux.conf ~/
sudo cp fonts/* /usr/local/share/fonts/ 
fc-cache -fv
cp ./Wallpaper ~/Pictures/
systemctl enable network-manager

sudo apt autoremove
