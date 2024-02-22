import random
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.input_csv_full_path = ''
        self.input_csv_display_path = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        self.include_capital = tk.IntVar()
        self.include_numbers = tk.IntVar()
        self.include_special = tk.IntVar()

        self.output_password = tk.StringVar()

        # define widgets
        lb_header = tk.Label(self, text='Settings:', font=('Arial', 16))

        ckb_capital = tk.Checkbutton(self, text='Capital letters', variable=self.include_capital)
        ckb_numbers = tk.Checkbutton(self, text='Numbers', variable=self.include_numbers)
        ckb_special = tk.Checkbutton(self, text='Special characters', variable=self.include_special)

        lbl_length = tk.Label(self, text='Length:')
        self.ent_length = tk.Entry(self)

        btn_generate_single = tk.Button(self,
                                        text='Generate single password',
                                        command=lambda: self.generate_single_password())
        ent_output = tk.Entry(self, state='readonly', textvariable=self.output_password, width=40)

        separator = ttk.Separator(self, orient='horizontal')

        lb_header2 = tk.Label(self, text='Generate password list:', font=('Arial', 16))

        btn_select_file = tk.Button(self, text='Select .csv input file', command=lambda: self.open_csv_file())
        lb_file_name = tk.Label(self, textvariable=self.input_csv_display_path, fg='#349eeb')
        btn_generate_list = tk.Button(self, text='Generate list', command=lambda: self.generate_list())

        # display widgets
        lb_header.grid(row=0, column=0, columnspan=2, pady=12)
        ckb_capital.grid(row=1, column=0, sticky='w', columnspan=2)
        ckb_numbers.grid(row=2, column=0, sticky='w', columnspan=2)
        ckb_special.grid(row=3, column=0, sticky='w', columnspan=2)
        lbl_length.grid(row=4, sticky='w', column=0)
        self.ent_length.grid(row=4, sticky='w', column=1)
        btn_generate_single.grid(row=5, column=0, columnspan=2, pady=12)
        ent_output.grid(row=6, column=0, columnspan=2)
        separator.grid(row=7, column=0, sticky='ew', columnspan=2, pady=16)
        lb_header2.grid(row=8, column=0, columnspan=2, pady=12)
        btn_select_file.grid(row=9, column=0, columnspan=2)
        lb_file_name.grid(row=10, column=0, columnspan=2, pady=8)
        btn_generate_list.grid(row=11, column=0, columnspan=2)

    def generate_password(self):
        capital = self.include_capital.get()
        numbers = self.include_numbers.get()
        special = self.include_special.get()
        # print(f'c: {capital}, n: {numbers}, s: {special}, l: {length}')

        password = ''

        main_dict = 'qwertyuiopasdfghjklzxcvbnm'
        dict1 = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        dict2 = '1234567890'
        dict3 = '!@#$%^&*'

        if capital == 1:
            main_dict += dict1
        if numbers == 1:
            main_dict += dict2
        if special == 1:
            main_dict += dict3

        i = 0
        length = int(self.ent_length.get())
        while i < length:
            password += main_dict[random.randint(0, len(main_dict) - 1)]
            i += 1

        return password

    def validate_length(self):
        try:
            x = int(self.ent_length.get())
            if not 4 <= x <= 32:
                raise ValueError('Wrong number')
            return True

        except ValueError:
            messagebox.showwarning('Warning', 'Length should be number between 4 and 32')
            return False

    def generate_single_password(self):
        password = ''
        if self.validate_length():
            password = self.generate_password()

        # print(password)
        self.output_password.set(password)

    def open_csv_file(self):
        self.input_csv_full_path = filedialog.askopenfilename()
        self.input_csv_display_path.set(self.input_csv_full_path.split('/')[-1])

    def generate_list(self):
        if self.validate_length():
            try:
                with open(self.input_csv_full_path, 'r') as csv_input:
                    csv_reader = csv.reader(csv_input)

                    output_path = self.input_csv_full_path.split('.')[0] + '_output.csv'

                    with open(output_path, 'w', newline='') as csv_output:
                        csv_writer = csv.writer(csv_output)

                        first_flag = True

                        for line in csv_reader:
                            if first_flag:
                                first_flag = False
                                line.append('email')
                                line.append('password')
                                csv_writer.writerow(line)
                                continue

                            email = f'{line[0].lower()}.{line[1].lower()}@company.com'
                            password = self.generate_password()

                            line.append(email)
                            line.append(password)

                            csv_writer.writerow(line)

                messagebox.showinfo('Info', f'File saved successfully as {output_path.split("/")[-1]}')

            except:
                messagebox.showwarning('Warning', 'Problem with opening .csv file')


if __name__ == '__main__':
    app = App()
    app.geometry('360x480')
    app.title('Password generator')
    app.mainloop()
