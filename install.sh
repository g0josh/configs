#!/bin/bash
echo ""
echo "---------------------------------------"
echo "Installing packages"
echo "---------------------------------------"
echo ""
sudo pamac checkupdates -a
sudo pamac upgrade -a
sudo pamac install code pavucontrol firefox rxvt-unicode imagemagick \
feh bc lm_sensors lxappearance arandr rofi nomacs \
polybar neovim python3-opencv flameshot neovim samba mpd ncmpcpp mpc -y
pamac build picom rslsync

echo ""
echo "---------------------------------------"
echo "Setting up configs"
echo "---------------------------------------"
echo ""
sudo cp smb.conf /etc/samba
sudo mkdir /var/mpd
sudo chown job:job /var/mpd
touch /var/mpd/log
cp .config/qtile ~/.config/ -r
cp .config/polybar ~/.config/ -r
cp .config/autostart.sh ~/.config
sudo chmod u+x ~/.config/autostart.sh
cp .config/mpd ~/.config/ -r
cp .config/ncmpcpp ~/.config/ -r
cp .config/nvim ~/.config/ -r
cp .config/themes ~/.config/ -r
cp .config/picom ~/.config -r
cp .config/rslsync ~/.config -r
cp .Xresources ~/
cp .xinitrc ~/
cp .tmux.conf ~/
cp .zshrc ~/
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
cd $HOME/tools
git clone git@github.com:romkatv/powerlevel10k.git

echo ""
echo "---------------------------------------"
echo "Cleaning up"
echo "---------------------------------------"
echo ""
pamac clean --build-files

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
ln -s /mnt/hdd/sync/documents Documents
ln -s /mnt/hdd/sync/music Music
ln -s /mnt/hdd/pictures Pictures
ln -s /mnt/media/movies Videos
echo "---------------------------------------"
echo "Mounted drives, refer fstab and fix /etc/fstab"
echo "---------------------------------------"
echo ""

systemctl start smb
systemctl enable smb
systemctl start rslsync --user
systemctl enable rslsync --user
systemctl enable mpd --user
systemctl start mpd --user
