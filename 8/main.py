from collections import Counter


def read_input():
    with open('input', 'r') as f:
        return f.read()


def split_into_chunks(body, size):
    for i in range(0, len(body) - size, size):
        yield body[i:i+size]


def main():
    picture_data = read_input()
    layers = []
    for chunk in split_into_chunks(picture_data, 25*6):
        layers.append(chunk)
    zeroes = [x.count('0') for x in layers]
    least_zero_layer = layers[zeroes.index(min(zeroes))]
    counter = Counter(least_zero_layer)
    print(counter['1']*counter['2'])


if __name__ == "__main__":
    main()
