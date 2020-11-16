# Mirror Pixels

## Technologies
- Python 3.8

This project provides an efficient function [mirror_bytes](https://github.com/admurray/mirror_pixels/blob/eac9e6a0a23ddb5d8cf43448f1c76cb665eaad5a/mirror_frame.py#L40)
to mirror a frame, provided as a byte sequence of the pixels.
There is another function provided as well [mirror_pixel_file](https://github.com/admurray/mirror_pixels/blob/eac9e6a0a23ddb5d8cf43448f1c76cb665eaad5a/mirror_frame.py#L80)
that works on a file pointer (BufferedReader object), however the performance
for this function is much lower than the former `mirror_bytes` function 
 
 ## Input Required
 - Height of the frame in pixels
 - Width of the frame in pixels
 - Size of each pixel in bytes
 - Pixel data as bytestring 

#### Sample Pixel Input 
*Converted to a integer list and visually edited to enhance readability*  
```
[255, 255, 254, 22, 165, 254, 226, 234, 123,  
231, 31, 162, 87, 222, 31, 32, 123, 98,  
23, 43, 78, 123, 231, 123, 65, 86, 221]
```
This list once converted to a bytestream and passed through the mirror_bytes
function yields
```
[226, 234, 123, 22, 165, 254, 255, 255, 254,  
32, 123, 98, 87, 222, 31, 231, 31, 162,  
65, 86, 221, 123, 231, 123, 23, 43, 78]
```

### Usage Information (SampleCode)
```
import mirror_frame

# filename.bin is a binary file.
with open('filename.bin', 'rb') as test_file:
    data = test_file.read()
frame = Frame(frame_data=data, frame_width=frame_width, 
                 frame_height=frame_height,
                 pixel_size=pixel_size)
mirrored_result_data = frame.mirror_bytes()
```
