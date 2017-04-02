#! /bin/bash

PWD=$(cd `dirname $0`; pwd)
DEP=$PWD/deps

# build and install libta_lib
cd $DEP
tar zxf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure
#mkdir $DEP/libta_lib-devel; ./configure --prefix=$DEP/libta_lib-devel
make -j16
make install
ln -s /usr/local/lib/libta_lib.so.0.0.0 /usr/lib64/libta_lib.so.0

cd $DEP
rm -rf ta-lib

# install TA-Lib
pip3 install TA-Lib

#dnf install python3-matplotlib python3-pandas python3-PyMySQL python3-psutil
# install pandas
pip3 install pandas

# install matplotlib
pip3 install matplotlib 

# install PyMySQL
pip3 install PyMySQL
# install psutil
pip3 install psutil

exit

# build and install TA-Lib
#gcc: error: /usr/lib/rpm/redhat/redhat-hardened-cc1: No such file or directory
dnf search redhat-hardened-cc1

tar zxf TA-Lib-0.4.10.tar.gz

cd TA-Lib-0.4.9
python3 setup.py install

exit

wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
sed -i '$aexport LD_LIBRARY_PATH=/usr/local/lib' /etc/profile
yum install freetype-devel libpng-devel -y #matplotlib

yum install openssl-devel #pip3

pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install numpy
pip3 install pandas
pip3 install ta-lib
pip3 install matplotlib

iptables -I INPUT -p tcp --dport 1234 -j ACCEPT


dnf install python3-matplotlib python3-PyMySQL python3-pandas
dnf install mysql-server
