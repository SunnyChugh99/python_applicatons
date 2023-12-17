import os
def reverse_lines(file_path, start_position, num_lines):
    # Open the file in binary mode to ensure correct byte positioning
    with open(file_path, 'rb') as file:
        # Set the file pointer to the start position
        file.seek(start_position)

        # Find the end of the file by seeking to the end and getting the byte position
        file.seek(0, 2)  # go to the end of the file
        end_position = file.tell()

        # Start reading from the byte before the last line
        file.seek(-2, 2)
        while file.tell() > start_position and file.read(1) != b'\n':
            file.seek(-2, 1)

        # Read the previous num_lines lines in reverse order
        lines = []
        while len(lines) < num_lines and file.tell() > start_position:
            # Find the start of the previous line
            file.seek(-2, 1)
            while file.tell() > start_position and file.read(1) != b'\n':
                file.seek(-2, 1)

            # Read the previous line
            line = file.readline().decode().rstrip('\r\n')
            lines.append(line)

        # Print the lines in reverse order
        for line in reversed(lines):
            print(line)

        # Return the current byte position
        return file.tell()



file_path = "/home/10683796/Desktop/EVERYTHING/sunny/read.py"
start_position = 0
num_lines = 2
print(reverse_lines(file_path, start_position, num_lines))