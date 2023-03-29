import numpy as np

file_name = input("Input file to be converted:")
Zthreshold = float(input("Input z value to fix :"))
file_f = open(file_name,'r')
lines = file_f.readlines()
add_str = "    &CONSTRAINT\n" + "        &FIXED_ATOMS\n"+"            COMPONENTS_TO_FIX XYZ\n"
add_str = add_str+"            LIST "
tag_str = "        &END FIXED_ATOMS\n"+"    &END CONSTRAINT"

j=0
Z_threshold = float(Zthreshold)
for i in range(18,len(lines),1):
	if "&END COORD" in lines[i]:
		break
	j = j + 1
	z = float(lines[i].split()[3])
	if float(z < Z_threshold):
		add_str = add_str + " " + str(j)

add_str = add_str + "\n" + tag_str
for i in range(len(lines)):
	if "&MD" in lines[i]:
		lines[i] = "  &MD\n"+"    &PRINT\n"+"      &ENERGY ON\n"+"      &END ENERGY\n"+"    &END PRINT\n"

for i in range(len(lines)):
	if "&END MD" in lines[i]:
		lines[i] = lines[i]+"\n"+add_str+"\n"	

for i in range(len(lines)):
	if "ENSEMBLE" in lines[i]:
		lines[i] = "    ENSEMBLE NVT\n" +"    &THERMOSTAT\n"+"      TYPE NOSE\n"+"    &END THERMOSTAT\n"
for i in range(len(lines)):
	if "&END TRAJECTORY" in lines[i]:
		lines[i] = lines[i]+"\n"+"    &FORCES ON\n"+"      FORMAT xyz\n"+"    &END FORCES\n"
		lines[i] = lines[i]+"      &CELL ON\n"+"      &END CELL\n"

fixed_cp2k_name = "fixed-"+file_name
fixed_cp2k_file = open(fixed_cp2k_name,'w')
fixed_cp2k_file.writelines(lines)
fixed_cp2k_file.close()
file_f.close()
