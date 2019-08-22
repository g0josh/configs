#!/bin/bash

echo "Make sure you clone the repo www.github.com/g0josh/configs.git and run this script inside the folder 'configs'"
read -p 'Continue[y/N] :' cont
if [ "$cont" != "y" ]; then
	exit 1
fi

echo ""
echo "---------------------------------------"
echo "Setting up configs"
echo "---------------------------------------"
echo ""

mkdir ~/.config
cp ./.config/i3 ~/.config -r
cp ./.config/polybar ~/.config -r
cp ./.config/rofi ~/.config -r
cp ./.config/ranger ~/.config -r
cp ./.config/nvim ~/.config -r
cp ./.config/mpd ~/.config -r
cp ./.config/ncmpcpp ~/.config -r
cp ./.config/firefox ~/.config -r
cp ./.config/compton.conf ~/.config/compton.conf
cp ./.Xresources ~/
cp ./.xinitrc ~/
cp ./.bashrc ~/
cp ./.bash_profile ~/
cp ./.tmux.conf ~/
sudo cp ./Iosevka* /usr/local/share/fonts/
sudo cp ./Font\ Awesome* /usr/local/share/fonts/
fc-cache -fv

echo ""
echo "---------------------------------------"
echo "Installing all I need"
echo "---------------------------------------"
echo ""
sudo pacman -Syu xorg-server xorg-xset xorg-xrandr xorg-xinit mpd mpc ncmpcpp pulseaudio pulseaudio-alsa pavucontrol ranger neovim i3-gaps firefox rxvt-unicode uget transmission-gtk tmux numlockx syncthing feh nvidia nvidia-settings connman gtk2 vlc mpc

echo ""
echo "---------------------------------------"
echo "Setting up Yay"
echo "---------------------------------------"
echo ""
cd ~/Downloads
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

echo ""
echo "---------------------------------------"
echo "Getting AUR packages"
echo "---------------------------------------"
echo ""
yay -S i3lock-color resetmsmice compton-tryone-git



