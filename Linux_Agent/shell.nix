{ pkgs ? import <nixpkgs> { config.allowUnfree = true; } }:

pkgs.mkShell {
  buildInputs = [
    # --- Python ---
    pkgs.python3
    pkgs.python3Packages.pyqt5
    pkgs.python3Packages.python-dotenv
    pkgs.python3Packages.pyautogui
    pkgs.python3Packages.requests
    pkgs.python3Packages.selenium
    pkgs.python3Packages.psutil
    pkgs.python3Packages.pillow
    pkgs.python3Packages.rich

    # --- Browser (Selenium) ---
    pkgs.google-chrome
    pkgs.chromedriver

    # --- Audio ---
    pkgs.portaudio
    pkgs.libpulseaudio
    pkgs.pulseaudio
    pkgs.mpv
    pkgs.SDL2
    pkgs.SDL2_mixer
    pkgs.alsa-lib

    # --- Graphics / System ---
    pkgs.stdenv.cc.cc.lib
    pkgs.libGL
    pkgs.glib
    pkgs.zlib
    pkgs.unzip

    # --- Qt ---
    pkgs.libsForQt5.qt5.qtbase
    pkgs.libsForQt5.qt5.qtwayland
    pkgs.libxkbcommon

    # --- X11 / Wayland ---
    pkgs.xorg.libX11
    pkgs.xorg.libxcb
    pkgs.xorg.libXext
    pkgs.xorg.libXtst
    pkgs.xorg.libXinerama
    pkgs.xorg.libXrandr
    pkgs.xorg.xhost
    pkgs.xdotool

    # --- System tools ---
    pkgs.procps
  ];

  shellHook = ''
    # ---------------- SDL / pygame audio ----------------
    export SDL_AUDIODRIVER=pulseaudio

    # ---------------- Library paths ----------------
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.libGL
      pkgs.glib
      pkgs.zlib
      pkgs.portaudio
      pkgs.libpulseaudio
      pkgs.libxkbcommon
      pkgs.xorg.libX11
      pkgs.xorg.libxcb
      pkgs.xorg.libXext
      pkgs.xorg.libXtst
    ]}:$LD_LIBRARY_PATH

    # ---------------- Qt / Wayland ----------------
    export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.libsForQt5.qt5.qtbase.bin}/lib/qt-5.15/plugins/platforms"
    export QT_QPA_PLATFORM=wayland
    export XDG_SESSION_TYPE=wayland

    # ---------------- Chrome for Selenium ----------------
    mkdir -p .bin
    ln -sf ${pkgs.google-chrome}/bin/google-chrome-stable .bin/google-chrome
    export PATH=$PWD/.bin:$PATH

    # ---------------- X permissions ----------------
    xhost +local: || true

    echo "🛡️ AI Environment Ready"
    echo "🌐 Selenium: Chrome + ChromeDriver"
    echo "🔊 Audio: SDL2 + PulseAudio"
    echo "🎨 GUI: Qt (Wayland)"
  '';
}
