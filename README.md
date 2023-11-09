# ISO_Checksum_Check
Simple tool for calculating checksum of your ISO file

To use it, install dependences :

#
### pip install -r requirements.txt
#

run **checksum_for_ISO.py** wit argument of your .ISO file
#
### python3 main.py /path/to/your/file.iso
#


# Generate Checksum For Structured Folder

run **Store_Checksum_from_FW.py** with path to folder that need to be generated checksum as argument
#
### python3 Store_Checksum_from_FW.py /path/to/your/folder
#
After will be generated file ***stored_fw_data.json*** with checksum of each file inside
#
# Checksum Verification

run **verify_FW_structure_checksum.py** with 2 arguments:
- path to folder that need to be generated checksum
- path to file with already generated checksum
#
### python3 verify_FW_structure_checksum.py /path/to/your/folder  /path/to/your/file_with_checksum
#
After you will see that Checksum was verified successfull or list of files, that was modified

