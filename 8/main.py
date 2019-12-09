from collections import Counter


def read_input():
    with open('input', 'r') as f:
        return f.read()


def split_into_chunks(body, size):
    for i in range(0, len(body), size):
        yield body[i:i+size]


def get_pixel_color(layers, current_layer, position):
    current_pixel = layers[current_layer][position]
    if current_pixel == '2':
        return get_pixel_color(layers, current_layer+1, position)
    return current_pixel


def main():
    picture_data = read_input()
    layers = []
    for chunk in split_into_chunks(picture_data, 25*6):
        layers.append(chunk)
    decoded_image = ""
    for i in range(0, 25*6):
        pixel = get_pixel_color(layers, 0, i)
        decoded_image += pixel
    replaced_image = decoded_image.replace('0', '.')
    for row in split_into_chunks(replaced_image, 25):
        print(row)


if __name__ == "__main__":
    main()
