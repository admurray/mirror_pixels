import logging
import os.path
import sys

from mirror_conts import *
from mirror_exceptions import *

# Set up logging
root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


class Frame:
    """
    This class represents the Frame object that contains the information
    about the frame, such as frame height and width, pixel size, frame data.
    """
    def __init__(self, frame_data=None, frame_height=255, frame_width=255, pixel_size=3,):
        """
        Initialize the frame vairables.
        frame_data: bytestring representing the pixels for the frame
        frame_height: height of the frame in pixels
        frame_width: width of the frame in pixels
        pixel_size: number of bytes per pixel
                    example 3 for RGB and 4 for CYMK etc.

        """
        self.frame_data = frame_data
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.pixel_size = pixel_size

    def mirror_bytes(self):
        """
        Reads the bytes provided and reorganizes each pixel (pixel_size
        number of bytes) for each line specified by the width in the reverse
        order so as to create a mirror representation of the pixel data.
        """
        if not self.frame_data:
            logging.error('Frame data empty, please ensure the frame data is '
                          'not empty to mirror.')
            return

        expected_size = self.frame_width*self.frame_height*self.pixel_size
        if expected_size != len(self.frame_data):
            raise InvalidByteData(f'Expected size: {expected_size} != '
                                  f'recieved_size : {len(self.frame_data)}')

        # Number of bytes per line
        logging.info('Starting mirroring.')
        stride = self.frame_width * self.pixel_size
        try:
            rows = bytearray()
            for i in range(self.frame_height):
                # For each row in the image data
                read_index = (i * stride) + stride - self.pixel_size
                end_index = i * stride

                while True:
                    if read_index >= end_index:
                        pixel = self.frame_data[read_index:read_index + self.pixel_size]
                        rows.extend(pixel)
                        read_index = read_index -self.pixel_size
                    else:
                        break
            logging.info(f'Mirroring complete - returning data')
            return rows

        except (TypeError, ValueError) as e:
            logging.error(f'Unable to mirror bytes - {e}')
            raise

    def mirror_pixel_file(self, fp, write_file):
        """
        When a file pointer is provided this function reads the bytes from
        the buffered reader 3 at a time for each line in starting from the
        end of the line.
        It then write this information to another file in order.
        This function has a lower performance as compared to the mirror_bytes
        function defined above
        """
        if not fp:
            logging.error('Please provide a valid file pointer.')
            raise FileNotFoundError('Null file pointer provided.')

        if not write_file:
            write_file = write_file = os.path.join(PROJECT_ROOT, 'mirrored.bin')
            logging.warning(
                f'No write file provided, using default {write_file}')

        stride = self.frame_width * self.pixel_size
        if os.path.exists(write_file):
            logging.info('Old file found, deleting!')
            # @TODO Should really back this up rather than removing
            os.remove(write_file)

        with open(write_file, 'wb') as flipped:
            logging.info('Starting mirroring.')
            for i in range(self.frame_height):
                seek_index = (i * stride) + stride - self.pixel_size
                seek_end = i * stride

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

