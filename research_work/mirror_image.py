import struct
import zlib

class Pixel:
    """
    Represents ths individual pixel in an image
    """

    def __init__(self, red=0, blue=0, yellow=0):
        self.red = red
        self.blue = blue
        self.yellow=yellow

class Image:
    """
    An image is a 2D list of pixels
    """
    def __init__(self, pixels_arr=None):
        self.pixels_arr = pixels_arr
        self.width = 0
        self.height = 0
        self.recon = []
        self.idata_done = 0

    def mirror_matrix(self, pixels: list):
        final_image = []
        for each in pixels:
            final_image.append(each[::-1])
        return final_image

    def decode_image(self, filename):
        if not filename:
            raise FileNotFoundError
        with open(filename, 'rb') as input_img:
            png_signature = input_img.read(8)
            chunks = []
            while True:
                chunk_length, chunk_type, chunk_data = self.read_chunk(
                    input_img)
                chunks.append((chunk_length, chunk_type, chunk_data))

                if chunk_type == b'IEND':
                    break
        _, _, IHDR_data = chunks[0]

        self.width, self.height, self.bitd, self.colort, self.compm, \
        self.filterm, self.interlacem = struct.unpack(
            '>IIBBBBB', IHDR_data)

        IDAT_data = b''.join(
            chunk_data for chunk_length, chunk_type, chunk_data in chunks if
            chunk_type == b'IDAT')
        print(f'WIDTH: {self.width} HEIGHT: {self.height} PIXEL_FORMAT '
              f'{self.bitd}')
        uncompressed_data = zlib.decompress(IDAT_data)
        modified_data = self.modify_idat(modification='mirror',
                                      idat_data=uncompressed_data)
        compressed_modified = zlib.compress(modified_data)
        len_before = (len(IDAT_data))

        with open('new_image.png', 'wb') as new_image:
            new_image.write(png_signature)
            self.write_chunks(new_image, chunks, compressed_modified)

    def paeth_predictor(self, a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            Pr = a
        elif pb <= pc:
            Pr = b
        else:
            Pr = c
        return Pr

    def recon_a(self, r, c, stride, bytes_per_pixel):
        return self.recon[
            r * stride + c - bytes_per_pixel] if c >= bytes_per_pixel else 0

    def recon_b(self, r, c, stride):
        return self.recon[(r - 1) * stride + c] if r > 0 else 0

    def recon_c(self, r, c, stride, bytes_per_pixel):
        return self.recon[(r - 1) * stride + c - bytes_per_pixel] \
            if r > 0 and c >= bytes_per_pixel else 0

    def modify_idat(self, modification=None, idat_data=None):
        bytes_per_pixel = 3
        stride = self.width * bytes_per_pixel
        expected_len = (self.height*(1+self.width*bytes_per_pixel))
        actual_length = len(idat_data)
        print(f'EXPECTED: {expected_len}, ACTUALLENGTH: {actual_length}')
        rows = []

        if not modification:
            raise
        elif modification == 'mirror':
            i = 0
            for r in range(self.height):
                filter_type = idat_data[i]  # first byte of scanline is filter type
                i += 1
                for c in range(stride):
                    filt_x = idat_data[i]
                    # print(filter_type)
                    i += 1
                    if filter_type == 0:  # None
                        recon_x = filt_x
                    elif filter_type == 1:  # Sub
                        recon_x = filt_x + self.recon_a(
                            r, c, stride, bytes_per_pixel)
                    elif filter_type == 2:  # Up
                        recon_x = filt_x + self.recon_b(r, c, stride)
                    elif filter_type == 3:  # Average
                        recon_x = filt_x + (
                                self.recon_a(r, c, stride, bytes_per_pixel) +
                                self.recon_b(r, c, stride)) // 2
                    elif filter_type == 4:  # Paeth
                        recon_x = filt_x + self.paeth_predictor(
                            self.recon_a(r, c, stride, bytes_per_pixel),
                            self.recon_b(r, c, stride),
                            self.recon_c(r, c, stride, bytes_per_pixel))
                    else:
                        raise Exception('unknown filter type: ' + str(filter_type))
                    self.recon.append(recon_x & 0xff)  # truncation to byte

                """
                single_row = idat_data[i*stride:(i*stride)+stride]
                # single_row = single_row.replace(b'224', b'255')
                row = [list(single_row[i:i + 3])
                       for i in range(0, len(single_row), 3)]
                rows.append(row)
            #mirrored = self.mirror_matrix(rows)
            flat = []
            for elem in rows:
                flat.extend(elem)
            """

            b_mirrored = b''.join(bytes(pixels) for pixels in self.recon)
        return b_mirrored


    def extract_idat(self, compressed_idat):
        IDAT_data_uncomp = zlib.decompress(compressed_idat)
        data = list(IDAT_data_uncomp)
        return data

    def build_idat(self, uncompressed_data_array):
        compressed_data = zlib.compress(uncompressed_data_array)

    def read_chunk(self, f):
        # Returns (chunk_type, chunk_data)
        chunk_length, chunk_type = struct.unpack('>I4s', f.read(8))
        chunk_data = f.read(chunk_length)
        chunk_expected_crc, = struct.unpack('>I', f.read(4))
        chunk_actual_crc = zlib.crc32(chunk_data, zlib.crc32(
            struct.pack('>4s', chunk_type)))
        if chunk_expected_crc != chunk_actual_crc:
            raise Exception('chunk checksum failed')
        return chunk_length, chunk_type, chunk_data

    def write_chunks(self, fp, chunks, data=None):
        for chunk in chunks:
            chunk_length, chunk_type, chunk_data = chunk

            if chunk_type == b'IDAT':
                if self.idata_done != 1:
                    chunk_length = len(data)
                    print(chunk_length)
                    chunk_info = struct.pack('>I4s', chunk_length, chunk_type)
                    fp.write(chunk_info)
                    checksum = zlib.crc32(
                        data, zlib.crc32(struct.pack('>4s', chunk_type)))
                    crc = struct.pack('>I', checksum)
                    fp.write(data)
                    fp.write(crc)

                else:
                    continue
                self.idata_done = 1

            if chunk_data != b'IDAT':
                chunk_info = struct.pack('>I4s', chunk_length, chunk_type)
                fp.write(chunk_info)

                checksum = zlib.crc32(
                    chunk_data, zlib.crc32(struct.pack('>4s', chunk_type)))
                crc = struct.pack('>I', checksum)
                fp.write(chunk_data)
                fp.write(crc)


if __name__ == '__main__':
    img = Image()
    # img.decode_image('basn6a08.png')
    img.decode_image('image.png')
