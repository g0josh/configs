#!/bin/bash

echo "Make sure you clone the repo www.github.com/g0josh/configs.git and run this script inside the folder 'configs'"                                                                                                         
read -p 'Continue[y/n] :' cont
if [ "$cont" != "y" ]; then
        exit 1
fi
read -p 'Office(1) or Home(0): ' office

echo ""
echo "---------------------------------------"
echo "Setting up configs"
echo "---------------------------------------"
echo ""
cp ./.config/i3 -r ~/.config
cp ./.config/polybar -r ~/.config
cp ./.config/nvim -r ~/.config
cp ./.config/ranger -r ~/.config
cp ./.config/compton.conf ~/.config/compton.conf
cp ./.Xresources ~/
cp ./.bashrc ~/                                                                                            
cp ./.tmux.conf ~/

sudo cp ./Iosevka* /usr/local/share/fonts/
sudo cp ./Font\ Awesome* /usr/local/share/fonts/
fc-cache -fv
cp ./Wallpaper ~/Pictures/

if [ "$office" == "0" ]; then sudo apt install xorg; fi
echo ""
echo "---------------------------------------"
echo "Installing compton"
echo "---------------------------------------"
echo ""
sudo apt install asciidoc --no-install-recommends
sudo apt install libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev libconfig9 docbook-xml libxml2-utils xsltproc libconfig-dev libxslt1-dev docbook-xsl
cd ~/Downloads
git clone https://github.com/tryone144/compton.git
cd compton
make
make docs
sudo make install
sudo apt remove libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev docbook-xml libxml2-utils xsltproc asciidoc libxslt1-dev libconfig-dev docbook-xsl

echo ""
echo "---------------------------------------"
echo "Installing i3-gaps"
echo "---------------------------------------"
echo ""
sudo apt install libxcb-xrm-dev libxcb1-dev libxcb-keysyms1-dev libpango1.0-dev libxcb-util0-dev libxcb-icccm4-dev libyajl-dev libxcb-util0-dev libxcb-icccm4-dev libyajl-dev libstartup-notification0-dev libxcb-randr0-dev libev-dev libxcb-cursor-dev libxcb-xinerama0-dev libxcb-xkb-dev libxkbcommon-dev libxkbcommon-x11-dev autoconf libxcb-xrm0 libxcb-xrm-dev automake libxcb-shape0-dev noevim
cd ~/Downloads
git clone https://www.github.com/Airblader/i3 i3-gaps
git checkout gaps
cd i3-gaps
autoreconf --force --install
rm -rf build/
mkdir -p build && cd build/
../configure --prefix=/usr --sysconfdir=/etc --disable-sanitizers
make
sudo make install

echo ""
echo "---------------------------------------"
echo "Installing polybar v3.4"
echo "---------------------------------------"
echo ""
sudo apt install build-essential git cmake cmake-data pkg-config python3-sphinx libcairo2-dev libxcb1-dev libxcb-util0-dev libxcb-randr0-dev libxcb-composite0-dev python-xcbgen xcb-proto libxcb-image0-dev libxcb-ewmh-dev libxcb-icccm4-dev libxcb-cursor-dev libasound2-dev libmpdclient-dev libiw-dev libnl-genl-3-dev libpulse-dev
cd ~/Downloads
git clone --recursive https://github.com/polybar/polybar
git checkout 3.4
cd polybar
bash build.sh

sudo add-apt-repository ppa:codejamninja/jam-os
sudo apt update
sudo apt install code i3lock-color tmux neovim rxvt-unicode ranger

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

sudo apt autoremove

