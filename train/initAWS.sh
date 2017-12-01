#!/bin/bash

#The below steps are CUDA9 and Ubuntu 16.04 specific.
#They may serve as a reference for configuring AWS p3 instance


set -x

mkdir -p ~/wd/cache
mkdir -p ~/wd/models

wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb

sudo dpkg -i cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub

sudo apt-get update
sudo apt-get install cuda

sudo apt install python3-pip
sudo apt-get clean

pip3 install --upgrade pip
#ATTENTION: I consider it is fine for a secure spot box, that lives a few hours. You may not agree with that.
sudo chmod -R a+w /usr/local/ #Python packages permission issue.
#Just in case you need it
#Installing Pytorch on Amazon AWS
#pip3 install http://download.pytorch.org/whl/cu80/torch-0.2.0.post3-cp35-cp35m-manylinux1_x86_64.whl
#pip3 install torchvision
#pip3 install torchtext
pip3 install pandas
cd
git clone https://github.com/OpenNMT/OpenNMT

git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh

echo "Automated configuration complete. Checkout the script for required MANUAL steps."

# Required commands:
#
#. ~/.bashrc
#luarocks install tds
#luarocks install bit32
#sudo unattended-upgrades -d


# In case of locale problems
#export LC_ALL="en_US.UTF-8"
#export LC_CTYPE="en_US.UTF-8"
#sudo dpkg-reconfigure locales
