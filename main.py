"""
This file has been created to test and generate some basic stats for the
functions defined withing mirror_frame.py.
The primary mirroring function are :
    mirror_frame:Frame:mirror_bytes
    and
    mirror_frame:Frame:mirror_pixel_file
The stats previously generated for the above functions using test files can be
found in the file report.txt
"""
import time
from mirror_conts import *
from mirror_frame import Frame
from pathlib import Path


def current_milli_time():
    return time.time() * 1000


def time_mirror_byte_string(filename, frame_width, frame_height,
                                pixel_size):
    with open(filename, 'rb') as test_file:
        data = test_file.read()
    frame = Frame(data, frame_width=frame_width, frame_height=frame_height,
                  pixel_size=pixel_size)
    frame.frame_data = data
    start_time = current_milli_time()
    result_data = frame.mirror_bytes()
    end_time = current_milli_time()

    to_print_string = f'{"="*30} BYTES-MIRRORING {"="*30}\n'
    to_print_string += f'Filename: {filename}\n'
    to_print_string += f'Data Size Before: {len(data)} B\n'
    to_print_string += f'Data Size After: {len(result_data)} B\n'
    to_print_string += f'Completion duration: {end_time - start_time} ms\n\n'
    print(to_print_string)
    return to_print_string


def time_mirror_file(filename, frame_width, frame_height, pixel_size):
    frame = Frame(frame_data=None, frame_width=frame_width,
                  frame_height=frame_height,
                  pixel_size=pixel_size)
    write_file = os.path.join(PROJECT_ROOT, 'mirrored.bin')
    with open(filename, 'rb') as test_file:
        start_time = current_milli_time()
        result_data = frame.mirror_pixel_file(fp=test_file, write_file=write_file)
        end_time = current_milli_time()

    to_print_string = f'{"="*30} FILE-MIRRORING {"="*30}\n'
    to_print_string += f'Filename: {filename}\n'
    to_print_string += f'FILE Size Before: {Path(filename).stat().st_size} B\n'
    to_print_string += f'FILE Size After: {Path(write_file).stat().st_size} B\n'
    to_print_string += f'Completion duration: {end_time - start_time} ms\n\n'
    print(to_print_string)
    return to_print_string


if __name__ == '__main__':
    # This is demo code for the functions within mirror_frame.py
    # It runs the functions on various example files and records some basic
    # stats for each run. These are all printed in the file results.txt

    # Method - 1 - In memory bytes mirroring
    small_file_bytes_rep = time_mirror_byte_string(
        filename=SMALL_FILE_BIN, frame_width=3, frame_height=3, pixel_size=3)
    medium_file_bytes_rep = time_mirror_byte_string(
        filename=MEDIUM_BIN, frame_width=600, frame_height=600, pixel_size=3)
    large_file_bytes_rep = time_mirror_byte_string(
        filename=LARGE_BIN, frame_width=2500, frame_height=1010, pixel_size=3)

    # Method - 2 - Mirroring using file pointers.
    small_file_rep = time_mirror_file(
        filename=SMALL_FILE_BIN, frame_width=3, frame_height=3, pixel_size=3)
    medium_file_rep = time_mirror_file(
        filename=MEDIUM_BIN, frame_width=600, frame_height=600, pixel_size=3)
    large_file_rep = time_mirror_file(
        filename=LARGE_BIN, frame_width=2500, frame_height=1010, pixel_size=3)

    report_file = os.path.join(PROJECT_ROOT, 'report.txt')
    with open(report_file, 'wt') as report:
        report.write(small_file_bytes_rep)
        report.write(medium_file_bytes_rep)
        report.write(large_file_bytes_rep)
        report.write(small_file_rep)
        report.write(medium_file_rep)
        report.write(large_file_rep)
