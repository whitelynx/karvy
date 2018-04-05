Karvy
=====

A Kivy-based car entertainment system interface.


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

- `gst-python`
- `opencv-python`
- `plyer`
- `kivy`

### Installation on ArchLinux / Manjaro:

```bash
pacman -S python cython ffmpeg sdl2 sdl2_image sdl2_mixer sdl2_ttf zlib gstreamer gst-plugins-base gst-plugins-good hdf5 opencv gst-python python-kivy
```

You probably also want to make sure your user is a member of the `audio`, `video`, and `input` groups.


Running
-------

```bash
./karvy.py
```
