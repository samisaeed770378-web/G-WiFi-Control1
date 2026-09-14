#!/bin/bash
set -e

PROJECT="$HOME/G-WiFi-Control"
SDK="/opt/android-sdk"
NDK="$SDK/ndk/28.0.13004108"
REAL="$NDK/toolchains/llvm/prebuilt/linux-x86_64/bin"
FAKE="$NDK/toolchains/llvm/prebuilt/android-x86_64/bin"
QEMU="/usr/bin/qemu-x86_64"

export ANDROIDSDK="$SDK"
export ANDROID_HOME="$SDK"
export ANDROID_SDK_ROOT="$SDK"
export ANDROIDNDK="$NDK"
export ANDROID_NDK_HOME="$NDK"
export ANDROIDAPI=35
export NDKAPI=23

mkdir -p "$FAKE" "$HOME/qemu-ndk-bin" "$PROJECT/dist"

# QEMU wrappers for NDK host tools
TOOLS="clang clang++ clang-19 clang++-19 ld.lld llvm-ar llvm-ranlib llvm-strip llvm-objcopy llvm-objdump llvm-nm llvm-readelf llvm-as"

for T in $TOOLS; do
cat > "$FAKE/$T" <<WRAPPER
#!/bin/sh
exec $QEMU -L /usr/amd64 "$REAL/$T" "\$@"
WRAPPER
chmod +x "$FAKE/$T"

cat > "$HOME/qemu-ndk-bin/$T" <<WRAPPER
#!/bin/sh
exec $QEMU -L /usr/amd64 "$REAL/$T" "\$@"
WRAPPER
chmod +x "$HOME/qemu-ndk-bin/$T"
done

export PATH="$HOME/qemu-ndk-bin:$PATH"
export CC="$HOME/qemu-ndk-bin/clang"
export CXX="$HOME/qemu-ndk-bin/clang++"
export LD="$HOME/qemu-ndk-bin/ld.lld"
export AR="$HOME/qemu-ndk-bin/llvm-ar"
export RANLIB="$HOME/qemu-ndk-bin/llvm-ranlib"
export STRIP="$HOME/qemu-ndk-bin/llvm-strip"
export OBJCOPY="$HOME/qemu-ndk-bin/llvm-objcopy"
export OBJDUMP="$HOME/qemu-ndk-bin/llvm-objdump"
export NM="$HOME/qemu-ndk-bin/llvm-nm"
export READELF="$HOME/qemu-ndk-bin/llvm-readelf"

# Make the NDK path expected by p4a point to QEMU wrappers.
# Keep the real NDK sysroot and libraries available.
rm -rf "$FAKE"
mkdir -p "$FAKE"

for T in $TOOLS; do
cat > "$FAKE/$T" <<WRAPPER
#!/bin/sh
exec $QEMU -L /usr/amd64 "$REAL/$T" "\$@"
WRAPPER
chmod +x "$FAKE/$T"
done

ln -s "$NDK/toolchains/llvm/prebuilt/linux-x86_64/sysroot" "$FAKE/../sysroot" 2>/dev/null || true

cd "$PROJECT"

# Clear only the failed libffi recipe so it is rebuilt with the wrappers.
rm -rf "$HOME/.local/share/python-for-android/build/other_builds/libffi"

echo "======================================"
echo " G-WiFi Control - REAL PHONE BUILD"
echo " ARM64 phone + QEMU + Android NDK"
echo "======================================"
echo "CC=$CC"
echo "NDK=$NDK"
echo

p4a apk \
  --private "$PROJECT" \
  --package=com.sami.gwificontrol \
  --name="G-WiFi Control" \
  --version=1.0.0 \
  --bootstrap=sdl2 \
  --requirements=python3,kivy,requests \
  --arch=arm64-v8a \
  --android-api=35 \
  --ndk-api=23 \
  --orientation=portrait \
  --debug \
  --output="$PROJECT/dist/G-WiFi-Control.apk"

echo
echo "======================================"
echo " BUILD FINISHED"
echo "======================================"

if [ -f "$PROJECT/dist/G-WiFi-Control.apk" ]; then
    ls -lh "$PROJECT/dist/G-WiFi-Control.apk"

    TERMUX_DOWNLOAD="/data/data/com.termux/files/home/storage/downloads"

    if [ -d "$TERMUX_DOWNLOAD" ]; then
        cp "$PROJECT/dist/G-WiFi-Control.apk" "$TERMUX_DOWNLOAD/"
        echo
        echo "APK copied to:"
        echo "$TERMUX_DOWNLOAD/G-WiFi-Control.apk"
    else
        echo
        echo "APK created at:"
        echo "$PROJECT/dist/G-WiFi-Control.apk"
        echo
        echo "Termux Downloads directory is not mounted yet."
    fi
else
    echo "ERROR: APK was not created."
    exit 1
fi
