import os, math, argparse, progress.bar
from PIL import Image, ImageFont, ImageDraw

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
    "-c",
    "--color",
    help="base image color",
    required=False,
    type=str,
    default="white",
)

parser.add_argument(
    "-q",
    "--quiet",
    help="suppress all output",
    required=False,
    action=argparse.BooleanOptionalAction,
)

args = parser.parse_args()

path = args.input
file = open(path, "rb")

file_size = os.path.getsize(args.input)
image_size = math.ceil(math.sqrt((file_size + 3) / 3))

out = Image.new("RGB", (image_size, image_size), args.color)
col, row = 0, 0

if not args.quiet:
    bar = progress.bar.Bar("Working...", max=(image_size * image_size))

while col < image_size:
    rbytes = file.read(3)
    if not rbytes:
        break

    out.putpixel(
        (col, row),
        (
            rbytes[0],
            rbytes[1] if len(rbytes) > 1 else 0,
            rbytes[2] if len(rbytes) > 2 else 0,
        ),
    )

    row += 1
    if not args.quiet:
        bar.next()

    if row == image_size:
        row = 0
        col += 1


out.putpixel(
    (image_size - 1, image_size - 2),
    (
        (file_size & 0xFF0000000000) >> 40,
        (file_size & 0x00FF00000000) >> 32,
        (file_size & 0x0000FF000000) >> 24,
    ),
)

out.putpixel(
    (image_size - 1, image_size - 1),
    (
        (file_size & 0x000000FF0000) >> 16,
        (file_size & 0x00000000FF00) >> 8,
        (file_size & 0x0000000000FF),
    ),
)

out.save(args.output)
if not args.quiet:
    bar.finish()
