import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Progressbar
import webbrowser
from time import sleep


class Intro:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("500x250")
        self.root.configure(bg="#008080")
        self.root.resizable(False, False)

        # Try to load icon
        try:
            icon = PhotoImage(file="convert.png")
            self.root.iconphoto(False, icon)
        except:
            print("⚠️ Icon file missing!")

        # Welcome Label
        Label(self.root, text="Welcome to Unit Converter!", bg="#008080", fg="white",
              font=("Arial", 14, "bold")).pack(pady=20)

        # Progress Bar
        self.load = Progressbar(self.root, orient=HORIZONTAL, length=250, mode='indeterminate')
        self.start_btn = Button(self.root, text="START", bg="white", fg="black", command=self.loading)
        self.start_btn.pack(pady=10)

    def loading(self):
        self.start_btn.pack_forget()  # Remove start button
        self.load.pack(pady=10)
        self.root.update()

        for _ in range(10):
            self.load.step(10)
            sleep(0.2)
            self.root.update()

        self.root.destroy()
        root = tk.Tk()
        UnitConverterApp(root)
        root.mainloop()


class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.units = {
            "Length": {"units": ["Meter", "Kilometer", "Mile"], "factors": [1, 1000, 1609.34]},
            "Temperature": {"units": ["Celsius", "Fahrenheit", "Kelvin"], "formula": "special"}
        }

        self.create_widgets()

    def create_widgets(self):
        Label(self.root, text="Conversion Type:").pack(pady=5)

        self.conversion_type = StringVar()
        type_combobox = ttk.Combobox(self.root, textvariable=self.conversion_type, values=list(self.units.keys()))
        type_combobox.pack()
        type_combobox.bind("<<ComboboxSelected>>", self.update_units)

        input_frame = Frame(self.root)
        input_frame.pack(pady=10)
        self.input_value = StringVar()
        self.input_unit = StringVar()
        Entry(input_frame, textvariable=self.input_value, width=10).pack(side=LEFT)
        self.input_combo = ttk.Combobox(input_frame, textvariable=self.input_unit, width=12)
        self.input_combo.pack(side=LEFT)

        output_frame = Frame(self.root)
        output_frame.pack(pady=10)
        self.output_value = StringVar()
        self.output_unit = StringVar()
        Entry(output_frame, textvariable=self.output_value, width=10, state='readonly').pack(side=LEFT)
        self.output_combo = ttk.Combobox(output_frame, textvariable=self.output_unit, width=12)
        self.output_combo.pack(side=LEFT)

        Button(self.root, text="Convert", command=self.convert).pack(pady=10)

    def update_units(self, event=None):
        conv_type = self.conversion_type.get()
        units = self.units[conv_type]["units"]
        self.input_combo["values"] = units
        self.output_combo["values"] = units
        self.input_unit.set(units[0])
        self.output_unit.set(units[1])

    def convert(self):
        try:
            value = float(self.input_value.get())
            from_unit = self.input_unit.get()
            to_unit = self.output_unit.get()
            conv_type = self.conversion_type.get()

            if self.units[conv_type].get("formula") == "special":
                if from_unit == "Celsius" and to_unit == "Fahrenheit":
                    result = (value * 9 / 5) + 32
                elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                    result = (value - 32) * 5 / 9
                else:
                    result = value
            else:
                from_idx = self.units[conv_type]["units"].index(from_unit)
                to_idx = self.units[conv_type]["units"].index(to_unit)
                factor = self.units[conv_type]["factors"][to_idx] / self.units[conv_type]["factors"][from_idx]
                result = value * factor

            self.output_value.set(f"{result:.4f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input value")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion error: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    Intro(root)
    root.mainloop()
