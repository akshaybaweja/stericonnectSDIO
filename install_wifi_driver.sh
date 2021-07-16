KERNAL=$( uname -r | egrep -o "([0-9]+.[0-9]+.[0-9]+-v[0-9+])+" )
BUILD=$( uname -v | egrep -o "^#([0-9]+)" | egrep -o "([0-9]+)" )
wget http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-$KERNAL-$BUILD.tar.gz
tar xzf 8188eu-$KERNAL-$BUILD.tar.gz
sudo ./install.sh