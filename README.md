# Instructions

1. Connect pi and main computer (server) to same network.
2. SSH into pi using the following command and the password set.

```{sh}
$ ssh pi@192.168.0.2
```

3. Open python and import the module.
   Recommend attaching to a screen terminal emulator first.
   The help command will be useful now.

```{sh}
$ screen -a
$ python3
```
```{python}
>>> import deepPi
>>> help(deepPi)
```

4. Using the information from help(deepPi), you can operate the camera manually.
   For more advanced commands access deepPi.camera directly.
5. To send DeepPi deep, use the deploy command.

```{python}
>>> deepPi.deploy()
```

6. Detach from screen (CTRL-d) and kill the ssh (CTRL-d).
7. Send it deep.
8. Recover
9. Reconnect via ssh and resume the screen session

```{sh}
$ ssh pi@192.168.0.2
$ screen -r
```

10. Shutdown and disconnect

```{python}
>>> shutdown()
```

```{sh}
$ exit()
```

# TODO

- [ ] Modify stream to make it faster
- [ ] Set up a package manager for the Pi itself
  - [ ] pip download with all requirements
  - [ ] scp tarball to Pi
  - [ ] pip install on Pi
  - [ ] check python versions
- [ ] Run tests to see if it is working at the start

# PI modifications

Code is added to the end dhcpcd.conf to create a static IP.
In order to connect to the net normally (to download updates), this must be commented out

 - [ ] find a different way to set this up

```
sudo nano /etc/dhcpcd.conf
```

# Pi Set Up

## Install Packages

Follow these instructions if the Pi is not already set up correctly,
and you can't use a flashed image

1. Burn a minimal pi image.

While the disk is still mounted in your computer, place an empty file named ssh in the boot directory.

- [ ] Set up for the network configuration 

```{bash}
# network config
```

2. Install python3 and related packages.

Download latest stable python as a Gzipped tarball

https://www.python.org/downloads/source/

```
scp Python-x.x.x.tgz pi@192.168.0.x
ssh pi@192.168.0.x

```
