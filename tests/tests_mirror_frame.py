import unittest

from mirror_frame import Frame
from mirror_exceptions import *

class TestMirrorBytes(unittest.TestCase):

    def setUp(self):
        self.input_list = [255, 255, 254, 22, 165, 254, 226, 234, 123,
                           231, 31, 162, 87, 222, 31, 32, 123, 98,
                            23, 43, 78, 123, 231, 123, 65, 86, 221]
        self.frame = Frame(frame_data=bytes(self.input_list), pixel_size=3,
                           frame_height=3, frame_width=3)

    def test_correct_input(self):
        output_bytes = self.frame.mirror_bytes()
        output_list = list(output_bytes)
        expected_output = [226, 234, 123,  22, 165, 254, 255, 255, 254,
                           32, 123, 98, 87, 222, 31, 231, 31, 162,
                           65, 86, 221, 123, 231, 123,  23, 43, 78]

        for i in range(len(self.input_list)):
            self.assertEqual(output_list[i], expected_output[i])

    def test_incorrect_input(self):
        self.input_list.remove(255)
        self.frame.frame_data = bytes(self.input_list)
        with self.assertRaises(InvalidByteData):
            output_bytes = self.frame.mirror_bytes()

    def test_pixel_length_four(self):
        self.input_list.extend([231,
                                52, 55, 76, 24,
                                21, 123, 76, 123])
        self.assertEqual((len(self.input_list)%4), 0)
        expected_output = [ 123, 231, 31, 162, 165, 254, 226, 234, 255, 255, 254, 22,
                           78, 123, 231, 123, 123, 98, 23, 43, 87, 222, 31, 32,
                           21, 123, 76, 123, 52, 55, 76, 24, 65, 86, 221, 231]
        self.frame.frame_width = 3
        self.frame.frame_height = 3
        self.frame.pixel_size = 4
        self.frame.frame_data = self.input_list
        output_list = self.frame.mirror_bytes()
        for i in range(len(self.input_list)):
            self.assertEqual(output_list[i], expected_output[i])



if __name__ == '__main__':
    unittest.main()
