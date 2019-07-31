---
title: DEEPi Notes
author: Undersea Robotics and Imagine Lab, University of Rhode Island
---

## Contact

rshomberg@uri.edu

## Network Information

### Using TP Link Router

SSID and pin written on bottom of router.

This should be changed to DEEPiNet and deepinet via the router admin page for the 2.4GHz network.

#### Router Admin page

  * http://tplinkwifi.net or http://192.168.0.1 
  * username: admin
  * password: admin

For information on connected devices: IP & MAC Binding/ARP List

## Initial Pi Set up

1. Flash image using balena etcher.
2. Mount the /boot partition of the newly flashed drive
3. Place an empty file called ssh in /boot
4. Create a file wpa_supplicant.conf in /boot

```
# wpa_supplicant.conf

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
	ssid="DEEPiNet"
	psk="deepinet"
	key_mgmt=WPA-PSK
}
```

5. Boot up the pi and and ssh in while on the same network

```
$ ssh pi@raspberrypi.local
```

Default password should be raspberry.

6. Start camera interface

```
$ sudo raspi-config
```

7. Reboot pi
8. Install linux packages
9. Install python modules
10. Transfer DEEPi program


## Installing Software

### Installing linux packages

If the DEEPi is connected to the internet, open a terminal and type:

```
sudo apt-get install packagename
```

If not connected to internet, you need to use a computer that has internet access.
Some packages that might be needed on new installs will be included.

1. Download the package

Packages can be downloaded from: (https://packages.debian.org/stable/).
Stable is probably the correct release for downloads. 
To find out your release, use the following command in the DEEPi terminal.

```
lsb_release -a | grep Codename
```

As of writing this, the resulting codename is **strech**.
The correct packages can be found at (https://packages.debian.org/strech).

Scroll to the bottom of the package page and view the download link.
For pi zero, the **armhf** archetecture is correct. 
Confirm this with the following command in the pi terminal.

```
dpkg --print-architecture
```

Follow the correct architecture link and download the package from any of the mirrors.
This will save a **deb** file on your computer.

2. Transfer the file to the DEEPi

All DEEPi should have SSH enabled.
Otherwise there is no way to connect to it.
*scp* is a file transfer protocol built on SSH can be used to move the package.

Connect the computer that downloaded the package to the same network as the DEEPi.
Open a terminal and navigate to the folder with package deb file.
Figure out the IP address of the DEEPi and use the following command.
Replace 'package.deb' with the file name and '192.168.0.3' with DEEPi's IP address.
Don't forget the colon.
'pi' is the default username for any Raspberry Pi install. This could change.

```
scp package.deb pi@192.168.0.3:
```

3. Install the package

SSH into the DEEPi using the same IP address and username as before.

```
ssh pi@192.168.03
```

The package should be in the home folder.
Install it with this command replacing package.deb with the package name.

```
sudo dpkg -i package.deb
```

If you run into issues with dependencies, you will need to install those first using the same process.
Each package site has a list of dependencies..

### List of linux packages to install

 - [ ] emacs

### Install Python modules

1. Make list of requirements

In a folder named "packages" create a file called "requirements.txt"
List each module required on it's own line.

1. Download all packages

On a computer with pip3 installed and an internet connection use the following command from the packages folder.

```
pip download -r requirements.txt 
pip download -r requirements.txt --platform linux_arm71 --no-deps

```
This should download all required packages and dependencies.

3. Move packages to the pi

Make sure you have a packages folder on pi.
Then run this command.

```
scp packages/* pi@192.168.0.100:packages/
```

4. Install packages on pi.

SSH onto pi.
Install packages

```
pip3 install packages/requirements.txt --find-links packages/ --no-index
```

Dependencies might become an issue if they are not included in your original requirements list.
Go back and update your requirements list and restart the process.


## Time syncing

??Time sync using chrony.

## Hardware

### Potting 

The crystal ocilators are the most fragile part because they have an air gap.
There are two on the pi zero.
Put a dollop of epoxy over them before potting the whole thing.
This will help stress flow around the ocilators.
