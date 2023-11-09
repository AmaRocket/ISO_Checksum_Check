import datetime
import hashlib
import os
import sys

from tqdm import tqdm


def calculate_checksum(file_path, algorithm="sha256", buffer_size=65536):
    """Calculate the checksum of ISO file with progress bar."""
    hasher = hashlib.new(algorithm)
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as file, tqdm(
        total=file_size, unit="B", unit_scale=True
    ) as pbar:
        buffer = file.read(buffer_size)
        while len(buffer) > 0:
            hasher.update(buffer)
            pbar.update(len(buffer))
            buffer = file.read(buffer_size)

    return hasher.hexdigest()


if __name__ == "__main__":
    start = datetime.datetime.now().second
    iso_file_path = sys.argv[1]
    checksum = calculate_checksum(iso_file_path)
    end = datetime.datetime.now().second
    print(f"The SHA-256 checksum of the ISO file is: {checksum}")
    print("Calculted in: ", end - start, "sec")
