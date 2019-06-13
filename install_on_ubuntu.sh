#!/bin/bash

sudo apt install xorg

# compton
sudo apt install asciidoc --no-install-recommends
sudo apt install libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev libconfig9 docbook-xml libxml2-utils xsltproc
cd ~/Downloads
git clone https://github.com/tryone144/compton.git
cd compton
make
make docs
sudo make install
sudo apt remove libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev docbook-xml libxml2-utils xsltproc asciidoc

# Qtile
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

curl -s https://syncthing.net/release-key.txt | sudo apt-key add -
echo "deb https://apt.syncthing.net/ syncthing stable" | sudo tee /etc/apt/sources.list.d/syncthing.list

sudo add-apt-repository ppa:codejamninja/jam-os

sudo apt update
sudo apt install opera-stable code i3lock-color tmux numlockx

if [ "$1" == "o" ]; then
    echo "-----------------------------------------------"
    echo "Seting up for Office..."
    echo "-----------------------------------------------"
    sudo cp qtile.desktop /usr/share/xsessions
else
    echo "-----------------------------------------------"
    echo "Seting up for Home..."
    echo "-----------------------------------------------"
    sudo apt install syncthing transmission uget mpd nomacs ncmpcpp
fi

# get the configs
cd ~/Downloads
git clone https://github.com/g0josh.configs.git
git checkout sweet
git pull
mkdir ~/.config/qtile
mkdir ~/.config/ranger
cp configs/.config/qtile/* ~/.config/qtile/
cp configs/.config/ranger/* ~/.config/ranger/
cp configs/.config/compton.conf ~/.config/compton.conf
cp configs/.X* ~/
cp configs/.bashrc ~/
cp configs/.tmux.conf ~/
cp configs/.vimrc ~/
sudo cp Iosevka* /usr/local/share/fonts/
sudo cp Font\ Awesome* /usr/local/share/fonts/
fc-cache -fv
sudo dpkg -i configs/resemsmice_1.1.3_amd64.deb
cp configs/Wallpaper ~/Pictures/

sudo apt autoremove
echo "Please install NVIDIA drivers next"
