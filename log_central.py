import os


def reverse_readline(filename="/home/pcadmin/1.log", buf_size=1024, num_lines=2, start_pos=2):
    """Returns the last num_lines lines of a file in reverse order as a single string"""
    lines = []
    with open(filename, 'rb') as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        count = 0
        print(file_size)
        line_count = 0
        while remaining_size > 0 and line_count < num_lines:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size)).decode(encoding='utf-8')
            remaining_size -= buf_size
            count += 1
            buffer_lines = buffer.split('\n')
            # The first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # If the previous chunk starts right from the beginning of line
                # do not concat the segment to the last line of new chunk.
                # Instead, add the segment to the beginning of the lines list
                if buffer[-1] != '\n':
                    buffer_lines[-1] += segment
                else:
                    lines.insert(0, segment)
            segment = buffer_lines[0]
            for index in range(len(buffer_lines) - 1, 0, -1):
                if buffer_lines[index]:
                    lines.insert(0, buffer_lines[index])
                    line_count += 1
                    if line_count == num_lines:
                        break
        # Don't add the segment to the lines list if the file was empty or if we have already added the desired number of lines
        if segment is not None and line_count < num_lines:
            lines.insert(0, segment)
    return '\n'.join(reversed(lines[-num_lines:])), file_size * count


logs, current_pos = reverse_readline("/home/pcadmin/1.log")
print(f'logs: {logs}')
print(f'current_pos: {current_pos}')