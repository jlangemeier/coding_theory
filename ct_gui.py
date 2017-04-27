# Global Imports
import tkinter as tk

# Local Imports
import coding_theory


class CTApplication(tk.Frame):

    BUTTON_COLUMN = 0
    DATA_COLUMN = 1

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.default_data()
        # Local Vars
        self.has_error = False
        self.error_loc = -1
        # All the buttons
        self.frame_buttons()
        # All the matrices
        self.frame_encoding()
        self.frame_parity_check()
        self.frame_decoding()

    def default_data(self):
        self.hc74 = coding_theory.hamming_74()
        self.error_vector = coding_theory.ZERO_VECTOR

    def update_transmission_data(self, *args):
        self.error_vector = coding_theory.ZERO_VECTOR
        self.has_error = False
        self.add_error_text.set('Add Error')

        self.data = coding_theory.CODE_WORDS[self.letter_var.get()]
        self.data_encoded = self.hc74.encode(self.data)
        self.data_encoded_error = self.hc74.compute_error(self.data_encoded, self.error_vector)
        self.data_syndrome = self.hc74.parity(self.data_encoded_error)
        self.data_result = self.hc74.decode(self.data_encoded)

        # Generator Matrix
        self.display_vector(self.input_frame, self.data)
        self.display_vector(self.encoded_frame, self.data_encoded)
        self.input_frame.grid(column=2, row=2, rowspan=4, padx=5)
        self.encoded_frame.grid(column=4, row=0, rowspan=7, padx=5)

        # Parity Check Matrix
        self.display_vector(self.check_vector_frame, self.data_encoded_error, self.error_loc)
        self.display_vector(self.check_syndrome_frame, self.data_syndrome)
        self.display_vector(self.check_encoded_frame, self.data_encoded)
        self.display_vector(self.check_unitv_frame, self.error_vector)
        self.check_vector_frame.grid(column=2, row=0, rowspan=7, padx=5)
        self.check_encoded_frame.grid(column=4, row=0, rowspan=7, padx=5)
        self.check_unitv_frame.grid(column=6, row=0, rowspan=7, padx=5)
        self.check_syndrome_frame.grid(column=8, row=2, rowspan=3, padx=5)

        # Results Matrix
        self.display_vector(self.output_frame, self.data_encoded)
        self.display_vector(self.decoded_frame, self.data_result)
        self.output_frame.grid(column=2, row=0, rowspan=7, padx=5)
        self.decoded_frame.grid(column=4, row=2, rowspan=3, padx=5)

    def update_error_data(self):
        # Data Updates
        self.error_vector = coding_theory.ZERO_VECTOR if self.has_error else self.hc74.error_random()
        self.data_encoded_error = self.hc74.compute_error(self.data_encoded, self.error_vector)
        self.data_syndrome = self.hc74.parity(self.data_encoded_error)
        self.data_result = self.hc74.decode(self.data_encoded)

        # Swap Text and Button Display Info
        self.has_error = not self.has_error
        if self.has_error:
            self.add_error_text.set('Reset Error')
            self.error_loc = int(''.join(map(str, self.data_syndrome)), 2) - 1
        else:
            self.add_error_text.set('Add Error')
            self.error_loc = -1

        # Parity Check Matrix
        self.display_vector(self.check_vector_frame, self.data_encoded_error, self.error_loc)
        self.display_vector(self.check_syndrome_frame, self.data_syndrome)
        self.display_vector(self.check_encoded_frame, self.data_encoded)
        self.display_vector(self.check_unitv_frame, self.error_vector, self.error_loc)
        self.check_vector_frame.grid(column=2, row=0, rowspan=7, padx=5)
        self.check_encoded_frame.grid(column=4, row=0, rowspan=7, padx=5)
        self.check_unitv_frame.grid(column=6, row=0, rowspan=7, padx=5)
        self.check_syndrome_frame.grid(column=8, row=2, rowspan=3, padx=5)

        # Results Matrix
        self.display_vector(self.output_frame, self.data_encoded, self.error_loc, '#14D600')
        self.display_vector(self.decoded_frame, self.data_result)
        self.output_frame.grid(column=2, row=0, rowspan=7, padx=5)
        self.decoded_frame.grid(column=4, row=2, rowspan=3, padx=5)

    def display_matrix(self, cur_frame, matrix):
        cur_frame.grid(row=0, column=0, sticky=(tk.N + tk.S + tk.E + tk.W))

        num_rows, num_cols = matrix.shape

        for row in range(num_rows):
            tk.Grid.rowconfigure(cur_frame, row, weight=1)
            for col in range(num_cols):
                tk.Grid.columnconfigure(cur_frame, col, weight=1)
                btn = tk.Button(cur_frame, text=matrix[row][col], width=2, height=1, bg='#FFFFFF')
                btn.grid(row=row, column=col, sticky=(tk.N + tk.S + tk.E + tk.W))

    def display_vector(self, cur_frame, vector, error_loc=-1, error_color='#F20006'):
        cur_frame.grid(row=0, column=0, sticky=(tk.N + tk.S + tk.E + tk.W))

        num_rows = vector.shape[0]

        for row in range(num_rows):
            tk.Grid.rowconfigure(cur_frame, row, weight=1)
            bg_color = error_color if row == error_loc else '#FFFFFF'
            btn = tk.Button(cur_frame, text=vector[row], width=2, height=1, bg=bg_color)
            btn.grid(row=row, column=1, sticky=(tk.N + tk.S + tk.E + tk.W))

    def frame_buttons(self):
        self.buttons_frame = tk.Frame(self)

        self.letter_choices = sorted(coding_theory.CODES)
        self.letter_var = tk.StringVar(self)
        self.letter_var.set(self.letter_choices[0])
        self.dd_letter_menu = tk.OptionMenu(self.buttons_frame, self.letter_var, *self.letter_choices)

        self.add_error_text = tk.StringVar(self)
        self.add_error_text.set('Add Error')
        self.b_errors = tk.Button(self.buttons_frame, textvariable=self.add_error_text, width=20, height=2,
                                  command=self.update_error_data)

        self.buttons_frame.grid(column=self.BUTTON_COLUMN, row=0, padx=10, pady=10)
        self.dd_letter_menu.grid(column=0, row=0, sticky=(tk.N + tk.S + tk.E + tk.W))
        self.b_errors.grid(column=0, row=1, sticky=(tk.N + tk.S + tk.E + tk.W))

        self.letter_var.trace('w', self.update_transmission_data)

    def frame_encoding(self):
        self.encoding_frame = tk.Frame(self)
        self.generator_frame = tk.Frame(self.encoding_frame)
        self.input_frame = tk.Frame(self.encoding_frame)
        self.encoded_frame = tk.Frame(self.encoding_frame)

        self.data = coding_theory.CODE_WORDS[self.letter_var.get()]
        self.data_encoded = self.hc74.encode(self.data)

        equation_label = tk.Label(self.encoding_frame, text='x = Gp = ')
        equality_label = tk.Label(self.encoding_frame, text=' = ')
        self.display_matrix(self.generator_frame, self.hc74.generator)
        self.display_vector(self.input_frame, self.data)
        self.display_vector(self.encoded_frame, self.data_encoded)

        self.encoding_frame.grid(column=self.DATA_COLUMN, row=0, padx=10, pady=10)
        equation_label.grid(column=0, row=3)
        self.generator_frame.grid(column=1, row=0, rowspan=7, padx=5)
        self.input_frame.grid(column=2, row=2, rowspan=4, padx=5)
        equality_label.grid(column=3, row=3)
        self.encoded_frame.grid(column=4, row=0, rowspan=7, padx=5)

    def frame_parity_check(self):
        self.parity_check_frame = tk.Frame(self)
        self.check_matrix_frame = tk.Frame(self.parity_check_frame)
        self.check_vector_frame = tk.Frame(self.parity_check_frame)
        self.check_syndrome_frame = tk.Frame(self.parity_check_frame)
        self.check_encoded_frame = tk.Frame(self.parity_check_frame)
        self.check_unitv_frame = tk.Frame(self.parity_check_frame)

        self.data_encoded_error = self.hc74.compute_error(self.data_encoded, coding_theory.ZERO_VECTOR)
        self.data_syndrome = self.hc74.parity(self.data_encoded)

        equation_label = tk.Label(self.parity_check_frame, text='z = Hr = H(x + e_i) = ')
        equality_label1 = tk.Label(self.parity_check_frame, text=' = ( ')
        equality_label2 = tk.Label(self.parity_check_frame, text=' ) = ')
        addition_label = tk.Label(self.parity_check_frame, text=' + ')
        self.display_matrix(self.check_matrix_frame, self.hc74.parity_check)
        self.display_vector(self.check_vector_frame, self.data_encoded_error)
        self.display_vector(self.check_syndrome_frame, self.data_syndrome)
        self.display_vector(self.check_encoded_frame, self.data_encoded)
        self.display_vector(self.check_unitv_frame, self.error_vector)

        self.parity_check_frame.grid(column=self.DATA_COLUMN, row=1, padx=10, pady=10)
        equation_label.grid(column=0, row=3)
        self.check_matrix_frame.grid(column=1, row=2, rowspan=3, padx=5)
        self.check_vector_frame.grid(column=2, row=0, rowspan=7, padx=5)
        equality_label1.grid(column=3, row=3)
        self.check_encoded_frame.grid(column=4, row=0, rowspan=7, padx=5)
        addition_label.grid(column=5, row=3)
        self.check_unitv_frame.grid(column=6, row=0, rowspan=7, padx=5)
        equality_label2.grid(column=7, row=3)
        self.check_syndrome_frame.grid(column=8, row=2, rowspan=3, padx=5)

    def frame_decoding(self):
        self.decoding_frame = tk.Frame(self)
        self.result_frame = tk.Frame(self.decoding_frame)
        self.output_frame = tk.Frame(self.decoding_frame)
        self.decoded_frame = tk.Frame(self.decoding_frame)

        self.data_result = self.hc74.decode(self.data_encoded)

        equation_label = tk.Label(self.decoding_frame, text='d = Rx')
        equality_label = tk.Label(self.decoding_frame, text=' = ')
        self.display_matrix(self.result_frame, self.hc74.decoding)
        self.display_vector(self.output_frame, self.data_encoded)
        self.display_vector(self.decoded_frame, self.data_result)

        self.decoding_frame.grid(column=self.DATA_COLUMN, row=2, padx=10, pady=10)
        equation_label.grid(column=0, row=3)
        self.result_frame.grid(column=1, row=2, rowspan=3, padx=5)
        self.output_frame.grid(column=2, row=0, rowspan=7, padx=5)
        equality_label.grid(column=3, row=3)
        self.decoded_frame.grid(column=4, row=2, rowspan=3, padx=5)


if __name__ == '__main__':
    root = tk.Tk()
    app = CTApplication(master=root)
    app.mainloop()
