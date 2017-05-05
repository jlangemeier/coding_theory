import unittest
import random
import numpy as np
import coding_theory as ct

M_GENERATOR = np.array([[1, 1, 0, 1],
                        [1, 0, 1, 1],
                        [1, 0, 0, 0],
                        [0, 1, 1, 1],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]], dtype='int8')

M_PARITY = np.array([[0, 0, 0, 1, 1, 1, 1],
                     [0, 1, 1, 0, 0, 1, 1],
                     [1, 0, 1, 0, 1, 0, 1]], dtype='int8')

M_DECODE = np.array([[0, 0, 1, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0, 0, 1]], dtype='int8')


class TestHammingCode(unittest.TestCase):

    def setUp(self):
        self.hamming_code = ct.HammingCode(M_GENERATOR, M_PARITY, M_DECODE)
        self.data = random.choice(list(ct.CODE_WORDS.values()))

    def tearDown(self):
        pass

    # Encoding
    def test_encode_size(self):
        encoded = self.hamming_code.encode(self.data)
        self.assertEqual(encoded.size, self.hamming_code.channel_size)

    # Error Insertion
    def test_error_specific(self):
        error_loc = 4
        error_vector = self.hamming_code.error_specific(error_loc)
        self.assertEqual(error_vector[error_loc], 1)

    # Error Detection/Correction
    def test_syndrome_vector_size(self):
        encoded = self.hamming_code.encode(self.data)
        syndrome_vector = self.hamming_code.parity(encoded)
        self.assertEqual(syndrome_vector.size, encoded.size - self.data.size)

    def test_syndrome_vector_noerror(self):
        encoded = self.hamming_code.encode(self.data)
        syndrome_vector = self.hamming_code.parity(encoded)
        no_error_vector = np.array([0, 0, 0], dtype='int8')
        self.assertTrue(np.array_equal(syndrome_vector, no_error_vector))

    def test_syndrome_vector_error(self):
        encoded = self.hamming_code.encode(self.data)
        error_val = self.hamming_code.error_random()
        encoded_error = self.hamming_code.compute_error(encoded, error_val)
        syndrome_vector = self.hamming_code.parity(encoded_error)
        no_error_vector = np.array([0, 0, 0], dtype='int8')
        self.assertFalse(np.array_equal(syndrome_vector, no_error_vector))

    def test_syndrome_vector_error_location(self):
        encoded = self.hamming_code.encode(self.data)
        error_loc = 4
        error_val = self.hamming_code.error_specific(error_loc)
        encoded_error = self.hamming_code.compute_error(encoded, error_val)
        syndrome_vector = self.hamming_code.parity(encoded_error)
        error_located_loc = int(''.join(map(str, syndrome_vector)), 2) - 1
        self.assertEqual(error_loc, error_located_loc)

    # Decoding
    def test_decode_size(self):
        encoded = self.hamming_code.encode(self.data)
        decoded = self.hamming_code.decode(encoded)
        self.assertEqual(self.data.size, decoded.size)

    def test_decode_noerror(self):
        encoded = self.hamming_code.encode(self.data)
        decoded = self.hamming_code.decode(encoded)
        self.assertTrue(np.array_equal(self.data, decoded))

    # End to End Test
    def test_error_correction(self):
        encoded = self.hamming_code.encode(self.data)
        error_val = self.hamming_code.error_random()
        encoded_error = self.hamming_code.compute_error(encoded, error_val)
        syndrome_vector = self.hamming_code.parity(encoded_error)
        encoded_corrected = self.hamming_code.parity_correction(encoded_error, syndrome_vector)
        decoded = self.hamming_code.decode(encoded_corrected)
        self.assertTrue(np.array_equal(self.data, decoded))


if __name__ == '__main__':
    unittest.main()
