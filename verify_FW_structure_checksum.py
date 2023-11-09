import hashlib
import json
import os
import sys

from termcolor import colored
from tqdm import tqdm

stored_checksums = {}
missmatch_data = []

firmware_directory = sys.argv[1]  # '/home/amarocket/BrightSensors/ExD_v2/bright_sensors_exd_v2'
stored_fw_checksums = sys.argv[2]  # '/home/amarocket/BrightSensors/GIT/CRC_CHECKSUM/ISO_Checksum_Check/stored_fw_data.json'

with open(stored_fw_checksums) as json_file:
    stored_checksums = json.load(json_file)


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


def verify_firmware_integrity(firmware_directory, stored_checksums):
    """Verify the integrity of the firmware."""
    current_checksums = generate_checksums(firmware_directory)

    for file, stored_checksum in stored_checksums.items():
        current_checksum = current_checksums.get(file)
        if current_checksum != stored_checksum:
            print(
                colored(
                    f"Checksum mismatch for file {file}. Firmware may be tampered.",
                    "red",
                )
            )
            missmatch_data.append(f"mismatch for file: {file}")
        else:
            print(colored("Checsum are equal", "blue"))


if __name__ == "__main__":
    verify_firmware_integrity(firmware_directory, stored_checksums)
    try:
        if missmatch_data:  # list is not empty
            print(colored(missmatch_data, "red"))
        else:
            print(colored("\nChecksum verified successfully!", "green"))
    except Exception as ex:
        print(colored(ex, "red"))
