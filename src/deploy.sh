# Copying the original python file
cp main.py old_main.py

# Replace the old content by the new one
python replace.py

sha=$(./makesha)
sha=$(echo $sha | tr -d '\n')

sed -i "s/^sha256sum.*/$sha/g" PKGBUILD


# Force to make a new pkg
makepkg -f

# Remove the old one and install the new one
sudo pacman -Rns langfetch
sudo pacman -U langfetch-0.0.1-1-any.pkg.tar.zst


# Change the origin main to the new main
rm main.py
mv old_main.py main.py
