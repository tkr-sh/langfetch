import os
from PIL import Image
import cairosvg


scale = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "][::-1]
WIDTH = 512
WIDTH_ASCII_ART = 36
COMPRESS = 2.3

for icon in sorted(os.listdir("icons")):
    ascii_art = []

    # Load SVG file
    svg_data = open(f'icons/{icon}').read()

    # Convert SVG to PNG using CairoSVG
    png_data = cairosvg.svg2png(bytestring=svg_data)

    # Save PNG to a file using PIL
    with open('tmp/example.png', 'wb') as f:
        f.write(png_data)

    # Load PNG file using PIL
    image = Image.open('tmp/example.png')

    # Get the width and height
    w,h = image.size
    image = image.resize((WIDTH, round(h / w * WIDTH)), Image.ANTIALIAS)

    # Get image size
    w,h = image.size

    step_h, step_w = round(h / w * WIDTH / WIDTH_ASCII_ART * COMPRESS), WIDTH // WIDTH_ASCII_ART
    # Iterate over pixels
    for y in range(0, WIDTH * h // w, step_h):

        s = ""
        for x in range(0, WIDTH, step_w):
            tot_brightness = 0
            it = 0

            for i in range(step_h):
                for j in range(step_w):
                    try:
                        # Get pixel value
                        r,g,b,_ = image.getpixel((x + j, y + i))

                        # Get the brightness from RGB
                        brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b

                        tot_brightness += brightness
                        it += 1
                    except IndexError:
                        pass

            s += scale[round((tot_brightness / 255 / it) * (len(scale) - 1))]

        ascii_art.append(s)
    print(f'        case "{icon.split(".")[0].split("_")[0]}":\n            return \"\"\"{chr(10).join(ascii_art)}\"\"\"')
