def read_header(file):
    """Read the header of the file and extract useful data
    14 bytes for the BMP file header
    40 bytes for the BMP information header"""
    header = file.read(54)

    # Check if it's a BMP file
    if header[:2] != b'BM':
        raise ValueError('BMP information header is not BMP')

    # Read every header data
    header_file_field = header[:2]
    header_file_size = int.from_bytes(header[2:6], byteorder='little')
    header_file_reserved = header[6:10]
    header_file_offset = int.from_bytes(header[10:14], byteorder='little')

    # Read DIB (Device Independent Bitmap) image values stored in little endian
    header_dib_header_size = int.from_bytes(header[14:18], byteorder='little')
    header_dib_width = int.from_bytes(header[18:22], byteorder='little')
    header_dib_height = int.from_bytes(header[22:26], byteorder='little')
    header_dib_plane = header[26:28]
    header_dib_bpp = header[28:30]
    header_dib_compression = header[30:34]
    header_dib_size = int.from_bytes(header[34:38], byteorder='little')
    header_dib_horizontal_resolution = int.from_bytes(header[38:42], byteorder='little')
    header_dib_vertical_resolution = int.from_bytes(header[42:46], byteorder='little')
    header_dib_color_palette = header[46:50]
    header_dib_color_important = header[50:54]

    return header, header_dib_width, header_dib_height, header_file_offset


def invert_color(input_file, output_file):
    """Read a BMP image, invert colors and save result"""
    try:
        with open(input_file, 'rb') as input:
            header, header_dib_width, header_dib_height, header_file_offset = read_header(input)

            input.seek(header_file_offset)

            pixels = []
            padding = (4 - (header_dib_width * 3 % 4)) % 4
            for _ in range(header_dib_height):
                line_pixels = []
                for _ in range(header_dib_width):
                    blue = int.from_bytes(input.read(1), byteorder='little')
                    green = int.from_bytes(input.read(1), byteorder='little')
                    red = int.from_bytes(input.read(1), byteorder='little')

                    line_pixels.append((255 - blue, 255 - green, 255 - red))
                pixels.append(line_pixels)

                input.read(padding)

        with open(output_file, 'wb') as output:
            output.write(header)

            for line_pixels in pixels:
                for blue, green, red in line_pixels:
                    output.write(bytes([blue, green, red]))
                output.write(b'\x00' * padding)

    except Exception as e:
        print(f"Erreur : {e}")


# Exemple d'utilisation
input_image = "images/image3.bmp"  # Nom du fichier BMP d'entrée
output_image = "output.bmp"  # Nom du fichier BMP de sortie
invert_color(input_image, output_image)