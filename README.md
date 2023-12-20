Karvy
=====

A [Kivy](https://kivy.org)-based car entertainment system interface.


<div style="color: #880000; font-weight: bold">NOTE: This project has been on hold since April 2020. Since then I've moved overseas - I no longer own this car, and the rest of the hardware for this project is sitting in storage on a different continent. Once I get a new car, there's a chance I'll pick this up again.</div>


![Music screen](https://i.imgur.com/6m7oeTJ.png)
![Maps screen](https://i.imgur.com/oe7OxIN.png)


Prerequisites
-------------

### System packages:

Note: On systems like Alpine Linux, you'll also need the `-dev` variants of most of these packages installed.

- `gcc`
- `make`
- `python3`
- `cython`
- `ffmpeg`
- `sdl2`
- `sdl2_image`
- `sdl2_mixer`
- `sdl2_ttf`
- `pango`
- `zlib`
- `hdf5`
- `opencv`
- `gstreamer`
- `gst-plugins-base`
- `gst-plugins-good`
- `pulseaudio`
- `pulseaudio-bluez` (for Bluetooth audio)
- `dbus`
- `mtdev`

### Python packages:

See [requirements.txt](./requirements.txt).

`python-gobject` can be substituted for `opencv-python` if you are unable to install the latter.

### Kivy garden flowers:

- `iconfonts`
- `mapview`

### Installation on ArchLinux / Manjaro:

```bash
pacman -S python cython ffmpeg sdl2 sdl2_image sdl2_mixer sdl2_ttf pango zlib hdf5 opencv gstreamer gst-plugins-base gst-plugins-good pulseaudio pulseaudio-bluetooth mtdev python-gobject python-kivy
./bootstrap.sh
```

If installing in Arch Linux ARM on a Raspberry Pi, `bootstrap.sh` will likely fail. In that case, run these steps manually:
```bash
pip install --user -r requirements-rpi.txt
garden install --app iconfonts
garden install --app mapview
```

You probably also want to make sure your user is a member of the `audio`, `video`, and `input` groups.

### Installation on Alpine Linux on a Raspberry Pi:

You will first need to manually build a package for `opencv` with `python3` support and without GTK support. (TODO: instructions coming soon?) This cannot be built on the Raspberry Pi if using diskless mode (the default) because of space constraints. (not to mention the sheer amount of time building on the RPi would take)

Similarly, in order to install Kivy in diskless mode, you first have to mount a persistent volume at `/home` so it doesn't attempt to build the entire source tree in memory. (and so you don't lose the results of this process once you reboot)

We also currently need to install Kivy master due to an error that hasn't had a fix released yet; see [this StackOverflow question](https://stackoverflow.com/questions/59125232/how-to-deal-with-kivy-installing-error-in-python) for more info.

As a normal (non-`root`) user with `sudo` privileges, in the `karvy` directory:
```sh
# Add the `testing` repo, for `hdf5-dev`
echo 'https://dl-2.alpinelinux.org/alpine/edge/testing' | sudo tee -a /etc/apk/repositories

# Assuming you've built `opencv-nogtk` and copied the resulting `packages` dir to `/media/mmcblk0p1/packages`
echo '/media/mmcblk0p1/packages/unmaintained' | sudo tee -a /etc/apk/repositories

sudo apk update
sudo apk add gcc make python3-dev cython ffmpeg-dev sdl2-dev sdl2_image-dev sdl2_mixer-dev sdl2_ttf-dev pango-dev zlib-dev hdf5-dev gstreamer-dev gst-plugins-base gst-plugins-good pulseaudio pulseaudio-bluez dbus dbus-dev mtdev libjpeg-turbo-dev musl-dev mesa-dev opencv-nogtk

# Ensure DBus is running
sudo rc-update add dbus boot
sudo /etc/init.d/dbus start

pip3 install --upgrade pip
pip3 install --upgrade --user cython pillow
mkdir -p ~/tmp
TMPDIR=~/tmp pip3 install --user kivy[base] --pre --extra-index-url https://kivy.org/downloads/simple/
pip3 install --user $(grep -vE 'opencv-python|Kivy' requirements.txt)

~/.local/bin/garden install --app iconfonts
~/.local/bin/garden install --app mapview
```

You probably also want to make sure your user is a member of the `audio`, `video`, and `input` groups.


Running
-------

```bash
./karvy.py
```
