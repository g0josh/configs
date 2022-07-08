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
sudo apt install code pavucontrol firefox rxvt-unicode imagemagick \
feh bc lm-sensors zsh lxappearance arandr rofi nomacs \
shotwell numlockx polybar neovim python3-opencv flameshot -y

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
sudo apt install picom

echo ""
echo "---------------------------------------"
echo "Installing CLI tools"
echo "---------------------------------------"
echo ""
cd $HOME/tools
git clone git@github.com:g0josh/pycliutils
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

echo ""
echo "---------------------------------------"
echo "Mounting drives"
echo "---------------------------------------"
echo ""
sudo mkdir /mnt/storage /mnt/media
sudo mount /dev/sda2 /mnt/media
sudo mount /dev/sdb2 /mnt/storage
rm -rf Music Videos Documents Pictures
ln -s /mnt/storage Storage
ln -s /mnt/media Media
ln -s /mnt/storage/documents Documents
ln -s /mnt/storage/music Music
ln -s /mnt/storage/pictures Pictures
ln -s /mnt/storage/videos Videos
echo "---------------------------------------"
echo "Mounted drives, refer fstab and fix /etc/fstab"
echo "---------------------------------------"
echo ""
