#!/bin/bash

sudo apt install asciidoc --no-install-recommends
sudo apt install libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev libconfig9 docbook-xml libxml2-utils xsltproc
cd ~/Downloads
git clone https://github.com/tryone144/compton.git
cd compton
make
make docs
sudo make install
sudo apt remove libxinerama-dev libxrandr-dev libxcomposite-dev libdbus-1-dev docbook-xml libxml2-utils xsltproc asciidoc
sudo apt autoremove
