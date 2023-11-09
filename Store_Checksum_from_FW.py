import hashlib
import json
import os
import sys

from termcolor import colored
from tqdm import tqdm

FW_DIR = sys.argv[1]


def calculate_checksum(file_path, algorithm="sha256", buffer_size=65536):
    """Calculate the checksum of a file."""
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as file:
        with tqdm(
            total=os.path.getsize(file_path),
            unit="B",
            unit_scale=True,
            desc=os.path.basename(file_path),
        ) as pbar:
            buffer = file.read(buffer_size)
            while len(buffer) > 0:
                hasher.update(buffer)
                pbar.update(len(buffer))
                buffer = file.read(buffer_size)
    return hasher.hexdigest()


def generate_checksums(firmware_directory):
    """Generate checksums for all files in the firmware directory."""
    checksums = {}
    for root, dirs, files in os.walk(firmware_directory):
        for file in files:
            file_path = os.path.join(root, file)
            checksum = calculate_checksum(file_path)
            checksums[file] = checksum
    return checksums


if __name__ == "__main__":
    with open("stored_fw_data.json", "w") as outfile:
        json.dump(generate_checksums(FW_DIR), outfile)

        print(
            colored("Done!", "green")
            + "\nChecksum file saved in:"
            + colored(
                f" {os.getcwd()}/{os.path.basename('stored_fw_data.json')}", "blue"
            )
        )
