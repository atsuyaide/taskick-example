import argparse
import os

from PIL import Image

parser = argparse.ArgumentParser(description="This is example Taskick script.")
parser.add_argument("--event_type", default=None, type=str)
parser.add_argument("--src_path", default="", type=str)
parser.add_argument("--dest_path", default="", type=str)
parser.add_argument("--is_directory", default=False, action="store_true")
args = parser.parse_args()


def main():
    print(f"Input: {args.src_path}")
    basename = os.path.basename(args.src_path)
    filename = os.path.splitext(basename)[0]
    output_path = os.path.join("./output/", f"{filename}.pdf")
    img = Image.open(args.src_path)
    img = img.convert("RGB")
    img.save(output_path)
    print(f"Sccuessfuly converted: {output_path}")


if __name__ == "__main__":
    main()
