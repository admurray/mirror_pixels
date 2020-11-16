import logging
import os.path
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# SUPPORTED FORMATS
ARRAY = 'array'
BYTESTRING = 'bytestring'


class Frame:
    def __init__(self, frame_data=None, pixel_size=3, frame_height=255,
                 frame_width=255):

        self.frame = frame_data
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.pixel_size = pixel_size

        if isinstance(self.frame, list):
            self.format = ARRAY
        elif isinstance(self.frame, bytes):
            self.format = BYTESTRING

    def mirror_pixel_file(self, fp, write_file):
        stride = self.frame_width * self.pixel_size
        if os.path.exists(write_file):
            logging.info('Old file found, deleting!')
            os.remove(write_file)

        with open(write_file, 'wb') as flipped:
            logging.info('Starting mirroring.')
            for i in range(self.frame_height):
                seek_index = (i * stride) + stride - self.pixel_size
                seek_end = i * stride
                # print(f'seek_index : {seek_index}, seek_end: {seek_end}')
                while True:
                    if seek_index >= seek_end:
                        fp.seek(seek_index)
                        pixel = fp.read(3)
                        # print(list(pixel))
                        flipped.write(pixel)
                        seek_index = seek_index - self.pixel_size
                    else:
                        break
        logging.info(f'Mirroring complete - data written to {write_file}')

    def mirror_bytes(self, frame_data):
        stride = self.frame_width * self.pixel_size
        try:
            rows = bytearray()
            for i in range(self.frame_height):
                read_index = (i * stride) + stride - self.pixel_size
                end_index = i * stride
                # print(f'read_index : {read_index}, end_index: {end_index}')

                while True:
                    if read_index >= end_index:
                        pixel = frame_data[read_index:read_index + 3]
                        rows.extend(pixel)
                        read_index = read_index - 3
                    else:
                        break
            return rows
        except (TypeError, ValueError) as e:
            logging.error(f'Unable to mirror bytes - {e}')
            raise
