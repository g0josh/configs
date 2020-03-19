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
pip install xcffib cairocffi qtile


echo ""
echo "---------------------------------------"
echo "Installing Misc stuff"
echo "---------------------------------------"
echo ""
sudo apt install software-properties-common curl

curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt-get install apt-transport-https
sudo add-apt-repository ppa:codejamninja/jam-os
add-apt-repository ppa:mmstick76/alacritty

sudo apt update
sudo apt install code i3lock-color tmux pavucontrol alacritty firefox rxvt-unicode ranger imagemagick neovim feh bc lm-sensors rofi tmux


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
    sudo apt install syncthing transmission uget mpd mpc nomacs ncmpcpp numlockx bcmwl-kernel-source network-manager
    sudo dpkg -i resemsmice_1.1.3_amd64.deb
    cp .profile ~/
    cp .xinitrc ~/
    systemctl enable network-manager
fi

echo ""
echo "---------------------------------------"
echo "Setting up configs"
echo "---------------------------------------"
echo ""

cp .config/qtile ~/.config/ -r
cp .config/polybar ~/.config/ -r
cp .config/ranger ~/.config/ -r
cp .config/alacritty ~/.config/ -r
cp .config/mpd ~/.config/ -r
cp .config/ncmpcpp ~/.config/ -r
cp .config/nvim ~/.config/ -r
cp .config/themes ~/.config/ -r
cp .config/compton.conf ~/.config/compton.conf
cp .Xresources ~/
cp .bashrc ~/
cp .tmux.conf ~/
mkdir ~/.fonts
cp fonts/* ~/.fonts/
fc-cache -fv

echo ""
echo "---------------------------------------"
echo "Installing Polybar"
echo "---------------------------------------"
echo ""
cd $HOME/tools
git clone --recursive https://github.com/polybar/polybar
sudo apt install pkg-config python3-sphinx
sudo apt install libcairo2-dev libxcb1-dev libxcb-util0-dev libxcb-randr0-dev libxcb-composite0-dev python-xcbgen xcb-proto libxcb-image0-dev libxcb-ewmh-dev libxcb-icccm4-dev	
sudo apt install libxcb-xkb-dev libxcb-xrm-dev libxcb-cursor-dev libasound2-dev libpulse-dev libmpdclient-dev libcurl4-openssl-dev libnl-genl-3-dev

cd polybar
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

sudo apt remove python3-sphinx

echo ""
echo "---------------------------------------"
echo "Installing compton"
echo "---------------------------------------"
echo ""
sudo apt install asciidoc --no-install-recommends
sudo apt install libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev libconfig9 docbook-xml libxml2-utils xsltproc libconfig-dev libxslt1-dev docbook-xsl libxdamage-dev libdrm-dev mesa-common-dev
cd $HOME/tools
git clone https://github.com/tryone144/compton.git
cd compton
make
make docs
sudo make install
sudo apt remove libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev docbook-xml libxml2-utils xsltproc asciidoc libxslt1-dev libconfig-dev docbook-xsl

echo ""
echo "---------------------------------------"
echo "Cleaning up"
echo "---------------------------------------"
echo ""
sudo apt autoremove
