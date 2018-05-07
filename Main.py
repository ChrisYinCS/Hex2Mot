import os
import shutil
from tkinter import messagebox
import os.path


def find_bat(exe_path):
	"""
	Find the path where the "align_hex.bat" is and loacato that path. 
	Note that the align_hex.bat must be in the same root folder with this program.
	"""
    os.chdir(exe_path)
    if not os.path.exists('align_hex.bat'):
        find_bat(os.path.pardir)


def main():
    exe_fp = os.getcwd()    # Get the path where this program is.
    find_bat(exe_fp)

    os.system('align_hex.bat')      # Execute the first align bat, get ZON_P5S.hex

    write_flag = 1
    with open('ZON_P5S.hex', 'r') as original_file:
        with open('ZON_P5S.hex_NewTemp', 'w') as temp_file:
            for each_line in original_file:
                if write_flag == 1:
                    temp_file.write(each_line)
                if each_line[0:15] == ':020000040000FA':
                    write_flag = 0  # Write the first line and stop writing from 0x0000 to 0x5FFF, this is bootloader.
                elif each_line[0:17] == ':106000005A875A87':
                    temp_file.write(each_line)
                    write_flag = 1  # Start to write from 0x6000, this is application area

    shutil.move('ZON_P5S.hex_NewTemp', 'ZON_P5S.hex')	# overwrite the priginal file with the temp file and then remove the temp file 

    os.system('align_hex-sec.bat')	# align the second time, get 'zon.srec'

    os.rename('zon.srec', 'zon.mot')

    with open('zon.mot', 'rb+') as file:
        file.seek(-12, 2)     # locate to the last line: S5033C318F
        last_line = file.readline()
        string = last_line.decode('utf-8')
        changed_str = string[0] + '8' + string[2:13]  # change S5 to S8
        last_line = changed_str.encode()
        file.seek(-12, 2)       # locate to the last line
        file.write(last_line)

    file_list_before = os.listdir()
    os.system('TransferMot.exe')    # the program will wait for closing the window before it continues
    file_list_after = os.listdir()

    # find out the new generated file by 'TransferMot.exe'
    for file_new_generated in file_list_after:
        if file_new_generated not in file_list_before:
            # print(file_new_generated)
            break

    with open(file_new_generated, 'rb+') as mot_file:
        version_line = mot_file.read(15)    # the version line is 16 bytes, the last bytes is checksum
        version_bytes = bytearray(version_line)
        version_bytes[1] = 0x0E     # change the second bytes to 0x0E only because the meter needs
        checksum = 0
        for i in version_bytes:
            checksum += i

        reversed_checksum = checksum ^ 0xff
        reversed_low_byte = hex(reversed_checksum)[-2:]      # get the lowest byte of the reversed checksum
        new_checksum_hex = int(reversed_low_byte, base=16)

        version_bytes.append(new_checksum_hex)
        mot_file.seek(0,0)
        mot_file.write(version_bytes)	# write the new version line, with the second byte changed to '0x0E' and the last byte changed to new cheksum
    """
    Result = messagebox.askokcancel('Make a choice', 'Generate Digital Signature?\nHint: you need a key pair')
    if Result:
        RSA2048_dir = bat_fp + '\\RSA2048Software'      # 'C:\\Users\\Chris\\Documents\\MyCode\\Hex2Mot'
        os.chdir(RSA2048_dir)
        os.system('RAS2048.exe')
        os.chdir(bat_fp)
    else:
        pass
    """
    print('finished')


if __name__ == '__main__':
    main()




