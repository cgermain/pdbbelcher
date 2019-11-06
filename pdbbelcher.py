import os
import sys
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument('pdb', action="store", help="Path to the master PDB file")

def make_output_filename(filename, output_file_count):
	path = os.path.abspath(filename)
	directory = os.path.split(path)[0]
	full_filename = os.path.split(path)[1]
	base = os.path.splitext(full_filename)[0]
	extension = os.path.splitext(full_filename)[1]
	out_dir = os.path.join(directory, base)
	
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	return os.path.join(out_dir, base + "_" + str(output_file_count).zfill(8) + ".pdb")

def main():
	arguments = parser.parse_args()
	pdb_file = arguments.pdb

	# Example values of a pdb line
	# VALUES[0] = ATOM
	# VALUES[1] = 1
	# VALUES[2] = N
	# VALUES[3] = SER
	# VALUES[4] = P
	# VALUES[5] = 81
	# VALUES[6] = -0.409
	# VALUES[7] = 14.813
	# VALUES[8] = -0.678
	# VALUES[9] = 0.00
	# VALUES[10] = 0.00
	# VALUES[11] = PROA

	translate_dict = {'HT1':'1H' , 'HT2':'2H' , 'HT3':'3H' , 'HSD':'HIS'}
	skip_line = ['CLA', 'POT', 'SOLV', 'END', 'CRYST']

	with open(pdb_file, 'r') as master_file:
		line_count = 0
		output_file_count= 1
		first_line_not_found = True


		output_filename = make_output_filename(pdb_file, output_file_count)	
		out_file = open(output_filename,'w+')

		for line in master_file:
			values=line.split()
			if len(values) == 12 and values[0] not in skip_line and values[11] not in skip_line:
				if first_line_not_found:
					first_line_not_found = False
					
				if values[2] in translate_dict:
					values[2] = translate_dict[values[2]]

				#TODO Check if this is occupancy
				if values[10] == '0.00':
					values[10] = '1.00'

				out_line = make_pdb_line(values)

				if line_count < 1022:
					out_file.write(out_line)
					line_count +=1
				else:
					out_file.close()
					line_count = 0
					output_file_count += 1
					output_filename = make_output_filename(pdb_file, output_file_count)
					out_file = open(output_filename, 'w+')

		out_file.close()
		print("Belched out " + str(output_file_count) + " files.")

#TODO reformat this
def make_pdb_line(values):
	out_line = ''
	out_line += values[0]
	out_line += values[1].rjust(7) + '  '
	out_line += values[2].ljust(3) + ' '
	out_line += values[3] + ' '
	out_line += values[4] + ' '
	out_line += values[5] + ' '
	out_line += values[6] + ' '
	out_line += values[7] + ' '
	out_line += values[8] + ' '
	out_line += values[9] + ' '
	out_line += values[10] + ' '
	out_line += values[11]
	out_line += '\n'

	return out_line

if __name__ == "__main__":
	main()