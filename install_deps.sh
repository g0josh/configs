!compton
git clone https://github.com/tryone144/compton.git
sudo apt-get --no-install-recommends install asciidoc -y
sudo apt install libconfig-dev libdbus-1-dev xsltproc libxslt1-dev docbook-xsl libxml2-utils
make
make docs
make install

