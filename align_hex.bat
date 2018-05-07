copy /Y .\"MAXQ30 DEBUG"\ZON_V100.hex .\boot_util\
cd boot_util
srec_cat.exe -Disable_Sequence_Warnings ZON_P5S_AMETER_V100.hex -Intel -fill 0xff 0x0000 0x80000 -o ZON_P5S_boot_t.hex -Intel --address_length=4 --line_length=44 -output_block_size=16
srec_cat.exe -Disable_Sequence_Warnings ZON_P5S_boot_t.hex -Intel -unfill 0xFF 16 -o ZON_P5S.hex -Intel --address_length=4 --line_length=44 -output_block_size=16
del ZON_P5S_boot_t.hex
del ZON_V100.hex


