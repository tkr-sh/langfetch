# Removing the initai file
rm langfetch/PKGBUILD

# Copy the PKGBUILd to the repo of AUR
cp src/PKGBUILD langfetch/PKGBUILD
# Copy the LICENSE
cp src/LICENSE langfetch/LICENSE

# Go in the directory and make the package for the SRCINFO
cd langfetch
makepkg --printsrcinfo > .SRCINFO
