Karvy
=====

A [Kivy](https://kivy.org)-based car entertainment system interface.


![Music screen](https://i.imgur.com/6m7oeTJ.png)
![Maps screen](https://i.imgur.com/oe7OxIN.png)


Prerequisites
-------------

### System packages:

- `python3`
- `cython`
- `ffmpeg`
- `sdl2`
- `sdl2_image`
- `sdl2_mixer`
- `sdl2_ttf`
- `zlib`
- `hdf5`
- `opencv`
- `gstreamer`
- `gst-plugins-base`
- `gst-plugins-good`

### Python packages:

See [requirements.txt](./requirements.txt).

`python-gobject` can be substituted for `opencv-python` if you are unable to install the latter.

### Kivy garden flowers:

- `iconfonts`
- `mapview`

### Installation on ArchLinux / Manjaro:

```bash
pacman -S python cython ffmpeg sdl2 sdl2_image sdl2_mixer sdl2_ttf zlib gstreamer gst-plugins-base gst-plugins-good hdf5 opencv python-gobject python-kivy
./bootstrap.sh
```

You probably also want to make sure your user is a member of the `audio`, `video`, and `input` groups.


Running
-------

```bash
./karvy.py
```
