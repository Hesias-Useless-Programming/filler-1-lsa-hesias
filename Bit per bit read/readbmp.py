def read_bit_per_bit(input_file):
    try:
        with open(input_file, "rb") as f:
            while True:
                byte = f.read(1)
                if not byte:
                    break

                value = ord(byte)

                for i in range(7, -1, -1):
                    bit = (value >> i) & 1
                    yield bit
    except FileNotFoundError:
        print(f"Error : Can't find '{input_file}'")
    except Exception as e:
        print(f"Error : {e}")


file = "output.bmp"
for bit in read_bit_per_bit(file):
    print(bit, end="")