{pkgs ? import <nixpkgs> {}}:

with pkgs;

mkShell {
    buildInputs = [
        python312
        python312Packages.dbus-python
        python312Packages.googlemaps
        python312Packages.kivy-garden
        python312Packages.kivy
        python312Packages.opencv4
        python312Packages.plyer
        python312Packages.polyline
        python312Packages.pulsectl
    ];
}
