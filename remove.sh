#!/bin/bash

echo "This will uninstall all the custom configuration"
read -p 'Continue[y/n] :' cont
if [ "$cont" != "y" ]; then
	exit 1
fi

echo ""
echo "---------------------------------------"
echo "Uninstalling compton"
echo "---------------------------------------"
echo ""
cd ~/Downloads/compton/build
sudo make uninstall
sudo apt remove libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev docbook-xml libxml2-utils xsltproc asciidoc libxslt1-dev libconfig-dev docbook-xsl
rm -rf ~/.config/compton.conf

echo ""
echo "---------------------------------------"
echo "Uninstalling Qtile"
echo "---------------------------------------"
echo ""
sudo apt-get remove libpangocairo-1.0-0
pip3 uninstall xcffib cairocffi qtile

sudo apt remove rxvt-unicode ranger i3lock-color
sudo rm -rf /etc/apt/sources.list.d/codejamninja-ubuntu-jam-os-bionic*

sudo dpkg -P resetmsmice
sudo rm -rf ~/.config/qtile ~/.config/ranger /usr/share/xsessions/qtile.desktop

sudo apt remove syncthing
sudo rm -rf /etc/apt/sources.list.d/syncthing*
sudo apt-key del 58CD2BD7 00654A3E
sudo apt autoremove
