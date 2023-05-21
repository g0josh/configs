#!/bin/bash

echo "Make sure you clone the repo www.github.com/g0josh/configs.git and run this script inside the folder 'configs'"
read -p 'Continue[y/n] :' cont
if [ "$cont" == "n" ]; then
	exit 1
fi

echo ""
echo "---------------------------------------"
echo "Installing packages"
echo "---------------------------------------"
echo ""
yay -S --noconfirm alacritty neovim code zsh numlockx python-opencv flameshot ncmpcpp mpc mpd qtile-extras-git

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
cp .config/picom ~/.config -r
cp .config/alacritty ~/.config -r
cp .tmux.conf ~/
cp .zshrc ~/
cp .zshenv ~/
cp .fonts ~/ -r
fc-cache -fv

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
yay -S --noconfirm zsh-theme-powerlevel10k-git

echo ""
echo "---------------------------------------"
echo "Cleaning up"
echo "---------------------------------------"
echo ""
yay -Yc

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
