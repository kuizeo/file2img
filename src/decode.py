import argparse, progress.bar
from PIL import Image, ImageFont, ImageDraw


def col2rgb(tuple):
    return int("{:02x}{:02x}{:02x}".format(*tuple), 16)


parser = argparse.ArgumentParser(description="Represent a file as an image.")

parser.add_argument(
    "-i",
    "--input",
    help="input file",
    required=True,
    type=str,
)

parser.add_argument(
    "-o",
    "--output",
    help="output file",
    required=True,
    type=str,
)

parser.add_argument(
    "-q",
    "--quiet",
    help="suppress all output",
    required=False,
    action=argparse.BooleanOptionalAction,
)

args = parser.parse_args()

with Image.open(args.input, "re") as im:
    # semi-redundant, since it's a square
    height, width = im.size

    if not args.quiet:
        bar = progress.bar.Bar("Working...", max=(height * width))

    set1 = im.getpixel((-1, -1))
    set2 = im.getpixel((-1, -2))

    file_size = col2rgb(set2) * (255 ** 3) + col2rgb(set1)
    pixel_count = file_size // 3
    bytes_read = 0
    file_bytes = []

    while bytes_read <= pixel_count:
        pixel = im.getpixel((bytes_read / width, bytes_read % width))
        if not args.quiet:
            bar.next()

        bytes_read += 1
        if not args.quiet:
            bar.next()

    file_bytes = file_bytes[:file_size]
    with open(args.output, "wb") as f:
        f.write(bytearray(file_bytes))

if not args.quiet:
    bar.finish()
