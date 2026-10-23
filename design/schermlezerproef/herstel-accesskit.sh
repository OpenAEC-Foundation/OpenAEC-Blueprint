#!/bin/sh
# Makes the local AccessKit copy that cosmic-gerepareerd/ uses: the commit the
# COSMIC fork pins (wash2/accesskit 6c20249) with a one-line repair of the
# Windows adapter, which does not compile against the fork's winit otherwise.
# Run from the repository root after one `cargo build` in cosmic/ has fetched it.
set -e
SRC=$(ls -d "$HOME"/.cargo/git/checkouts/accesskit-*/6c20249 | head -1)
DST=target/schermlezerproef/accesskit-6c20249-reparatie
rm -rf "$DST"
cp -r "$SRC" "$DST"
sed -i 's/        window: &Window,/        window: \&dyn Window,/' "$DST/platforms/winit/src/platform_impl/windows.rs"
echo "Gerepareerde kopie in $DST"
