#!/bin/bash

echo "Make sure you clone the repo www.github.com/g0josh/configs.git and run this script inside the folder 'configs'"
read -p 'Continue[y/n] :' cont
if [ "$cont" == "n" ]; then
	exit 1
fi
read -p 'Office(1) or Home(0): ' office

sudo apt install xserver-xorg-core x11-xserver-utils udiskie curl --no-install-recommends --no-install-suggests

echo ""
echo "---------------------------------------"
echo "Installing Qtile"
echo "---------------------------------------"
echo ""
sudo apt-get install libxcb-render0-dev libffi-dev libcairo2 python3-pip cmake -y
pip3 install xcffib
pip3 install --no-cache-dir cairocffi
pip3 install qtile


echo ""
echo "---------------------------------------"
echo "Installing Misc stuff"
echo "---------------------------------------"
echo ""

curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt-get install apt-transport-https

sudo apt update
sudo apt install code tmux pavucontrol firefox rxvt-unicode imagemagick feh bc lm-sensors 


if [ "$office" == "1" ]; then
    echo "-----------------------------------------------"
    echo "Installing Office tools only..."
    echo "-----------------------------------------------"
    sudo cp qtile.desktop /usr/share/xsessions
else
    echo "-----------------------------------------------"
    echo "Installing home tools..."
    echo "-----------------------------------------------"
    sudo apt install transmission uget mpd mpc nomacs ncmpcpp numlockx network-manager 
    sudo dpkg -i resemsmice_1.1.3_amd64.deb
    cp .profile ~/
    cp .xsession ~/
    systemctl enable network-manager
fi

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
cp .config/compton.conf ~/.config/compton.conf
cp .Xresources ~/
cp .bashrc ~/
cp .tmux.conf ~/
mkdir ~/.fonts
cp fonts/* ~/.fonts/
fc-cache -fv
mkdir $HOME/tools

echo ""
echo "---------------------------------------"
echo "Installing NVIM"
echo "---------------------------------------"
echo ""
curl -LO https://github.com/neovim/neovim/releases/download/stable/nvim.appimage
mkdir $HOME/.local/bin -p
mv nvim.appimage $HOME/.local/bin/
sudo chmod u+x $HOME/.local/bin/nvim.appimage
sudo update-alternatives --install /usr/bin/vim vim "$HOME/.local/bin/nvim.appimage" 110

echo ""
echo "---------------------------------------"
echo "Installing compton"
echo "---------------------------------------"
echo ""
sudo apt install asciidoc --no-install-recommends
sudo apt install libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev libconfig9 docbook-xml libxml2-utils xsltproc libconfig-dev libxslt1-dev docbook-xsl libxdamage-dev libdrm-dev mesa-common-dev libgl1-mesa-dev libpcre3-dev
cd $HOME/tools
git clone https://github.com/tryone144/compton.git
cd compton
make
make docs
make install PREFIX=$HOME/.local/bin
sudo apt remove libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev docbook-xml libxml2-utils xsltproc asciidoc libxslt1-dev libconfig-dev docbook-xsl

echo ""
echo "---------------------------------------"
echo "Cleaning up"
echo "---------------------------------------"
echo ""
sudo apt autoremove
