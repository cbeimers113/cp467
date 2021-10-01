import os
import sys
from math import sqrt

from PIL import Image


# Accepted image formats
IMG_EXTS = ('png', 'jpg', 'jpeg', 'bmp', 'gif')

# Edge filters
FILT_X = (
    (-1, 0, 1),
    (-2, 0, 2),
    (-1, 0, 1)
)

FILT_Y = (
    (-1, -2, -1),
    (0, 0, 0),
    (1, 2, 1)
)

FILTERS = (FILT_X, FILT_Y)


def get_file():
    """Get the filename, perform checks on input."""
    error = len(sys.argv) != 2
    fname = None

    if not error:
        fname = sys.argv[1]
        error = fname.count('.') < 1 or fname[fname.rindex('.') + 1:] not in IMG_EXTS

    if error:
        print("Usage: python edges.py <filename.png | .jpg | .bmp | .gif>")
        fname = None
    else:
        if not os.path.exists(fname):
            print(f"Error: file {fname} does not exist.")
            fname = None

    return fname


def extract_edges(img: Image):
    """Extract edges from the image."""
    pixels = img.load()
    width, height = img.size

    # Make a new pixel array to store the grayscale data
    grayscale = [[0 for _ in range(height)] for __ in range(width)]

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            grayscale[x][y] = (r + g + b) / 3

    for x in range(width):
        for y in range(height):
            vals = [0, 0]  # Find edges in the x and y directions

            # Apply each filter
            for i, filter in enumerate(FILTERS):
                sum = 0  # The dot product for the filter and this pixel's neighbourhood

                for xOffs in range(-1, 2):
                    xx = x + xOffs

                    if xx < 0 or xx >= width:
                        continue

                    for yOffs in range(-1, 2):
                        yy = y + yOffs

                        if yy < 0 or yy >= height:
                            continue

                        # Multiply corresponding components together
                        sum += grayscale[xx][yy] * filter[xOffs + 1][yOffs + 1]

                vals[i] = sum
                pixels[x, y] = int(sqrt(vals[0] ** 2 + vals[1] ** 2))


def main():
    """Program begins here."""
    fname = get_file()

    if fname:
        img = Image.open(fname, 'r')
        img.show()                  # Show the original image
        extract_edges(img)
        img.save(f"edges_{fname}")  # Save the output image
        img.show()                  # Show the output image


if __name__ == "__main__":
    main()
