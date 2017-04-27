# Global Imports
import numpy as np
import random

CODES = {'E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'U', 'G', 'V', '_', '.', '?', '!'}

CODE_WORDS = {
    'E': np.transpose(np.array([0, 0, 0, 0], dtype='int8')),
    'T': np.transpose(np.array([0, 0, 0, 1], dtype='int8')),
    'A': np.transpose(np.array([0, 0, 1, 0], dtype='int8')),
    'O': np.transpose(np.array([0, 0, 1, 1], dtype='int8')),
    'I': np.transpose(np.array([0, 1, 0, 0], dtype='int8')),
    'N': np.transpose(np.array([0, 1, 0, 1], dtype='int8')),
    'S': np.transpose(np.array([0, 1, 1, 0], dtype='int8')),
    'H': np.transpose(np.array([0, 1, 1, 1], dtype='int8')),
    'R': np.transpose(np.array([1, 0, 0, 0], dtype='int8')),
    'U': np.transpose(np.array([1, 0, 0, 1], dtype='int8')),
    'G': np.transpose(np.array([1, 0, 1, 0], dtype='int8')),
    'V': np.transpose(np.array([1, 0, 1, 1], dtype='int8')),
    '_': np.transpose(np.array([1, 1, 0, 0], dtype='int8')),
    '.': np.transpose(np.array([1, 1, 0, 1], dtype='int8')),
    '?': np.transpose(np.array([1, 1, 1, 0], dtype='int8')),
    '!': np.transpose(np.array([1, 1, 1, 1], dtype='int8')),
}

ZERO_VECTOR = np.transpose(np.array([0, 0, 0, 0, 0, 0, 0], dtype='int8'))


def hamming_distance(s1, s2):
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


class HammingCode:

    def __init__(self, generator, parity_check, decoding):
        self.generator = generator
        self.parity_check = parity_check
        self.decoding = decoding
        self.channel_size = generator.shape[0]

    def encode(self, data):
        return np.dot(self.generator, data) % 2

    def parity(self, data):
        return np.dot(self.parity_check, data) % 2

    def decode(self, data):
        return np.dot(self.decoding, data) % 2

    def parity_correction(self, data, syndrome):
        print(''.join(map(str, syndrome)))
        error_loc = int(''.join(map(str, syndrome)), 2) - 1
        print(error_loc)
        error_val = np.eye(1, self.channel_size, error_loc, dtype='int8')[0]
        return (data + error_val) % 2

    def error_random(self):
        return self.error_specific(random.randint(0, self.channel_size - 1))

    def error_specific(self, error_loc):
        error_val = np.eye(1, self.channel_size, error_loc, dtype='int8')[0]
        return error_val

    def compute_error(self, data, error_vector):
        return (data + error_vector) % 2


def hamming_74():
    m_generator = np.array([[1, 1, 0, 1],
                            [1, 0, 1, 1],
                            [1, 0, 0, 0],
                            [0, 1, 1, 1],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]
                            ], dtype='int8')

    m_parity = np.array([[0, 0, 0, 1, 1, 1, 1],
                         [0, 1, 1, 0, 0, 1, 1],
                         [1, 0, 1, 0, 1, 0, 1]], dtype='int8')

    m_decode = np.array([[0, 0, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 0, 1]], dtype='int8')

    return HammingCode(m_generator, m_parity, m_decode)


if __name__ == '__main__':
    data = np.transpose(np.array([1, 0, 1, 1], dtype='int8'))

    hc_7_4 = hamming_74()

    # Running through an encode/decode with Error
    print("Initial Data")
    print(data)
    print(hc_7_4.generator)

    encoded_data = hc_7_4.encode(data)
    syndrome_data = hc_7_4.parity(encoded_data)

    print("\nEncoded Data and Syndrome Vector with NO Errors")
    print(encoded_data)
    print(syndrome_data)

    error_vector = hc_7_4.error_specific(3)
    encoded_error_data = hc_7_4.compute_error(encoded_data, error_vector)
    syndrome_error_data = hc_7_4.parity(encoded_error_data)

    print("\nEncoded Data and Syndrome Vector with Error at e^4")
    print(encoded_error_data)
    print(syndrome_error_data)

    encoded_corrected_data = hc_7_4.parity_correction(encoded_error_data, syndrome_error_data)
    syndrome_corrected_data = hc_7_4.parity(encoded_corrected_data)

    print("\nEncoded Data and Syndrome Vector after correction - NO Errors")
    print(encoded_corrected_data)
    print(syndrome_corrected_data)

    decoded_data = hc_7_4.decode(encoded_corrected_data)

    print("\nDecoded Data")
    print(decoded_data)
