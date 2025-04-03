import tkinter as tk
from tkinter import ttk, messagebox


class UnitConverterApp:
    def __init__(self):
        """Initialize the Unit Converter Application"""
        self.root = tk.Tk()
        self.root.title("Unit Converter")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Conversion units and factors
        self.units = {
            "Length": {
                "units": ["Meter", "Kilometer", "Mile"],
                "factors": [1, 1000, 1609.34]
            },
            "Temperature": {
                "units": ["Celsius", "Fahrenheit", "Kelvin"],
                "formula": "special"
            },
        }

        self.create_widgets()
        self.center_window()
        self.root.mainloop()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        """Create the GUI components"""
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Conversion type selector
        tk.Label(main_frame, text="Conversion Type:").grid(row=0, column=0, pady=5, sticky="w")

        self.conversion_type = tk.StringVar()
        type_combobox = ttk.Combobox(main_frame, textvariable=self.conversion_type, values=list(self.units.keys()))
        type_combobox.grid(row=0, column=1, pady=5)
        type_combobox.bind("<<ComboboxSelected>>", self.update_units)

        # Input section
        tk.Label(main_frame, text="Input Value:").grid(row=1, column=0, pady=5, sticky="w")
        self.input_value = tk.StringVar()
        tk.Entry(main_frame, textvariable=self.input_value, width=15).grid(row=1, column=1, pady=5)

        tk.Label(main_frame, text="From:").grid(row=2, column=0, pady=5, sticky="w")
        self.input_unit = tk.StringVar()
        self.input_unit_dropdown = ttk.Combobox(main_frame, textvariable=self.input_unit, width=12)
        self.input_unit_dropdown.grid(row=2, column=1, pady=5)

        # Output section
        tk.Label(main_frame, text="Converted Value:").grid(row=3, column=0, pady=5, sticky="w")
        self.output_value = tk.StringVar()
        tk.Entry(main_frame, textvariable=self.output_value, width=15, state='readonly').grid(row=3, column=1, pady=5)

        tk.Label(main_frame, text="To:").grid(row=4, column=0, pady=5, sticky="w")
        self.output_unit = tk.StringVar()
        self.output_unit_dropdown = ttk.Combobox(main_frame, textvariable=self.output_unit, width=12)
        self.output_unit_dropdown.grid(row=4, column=1, pady=5)

        # Convert button
        tk.Button(main_frame, text="Convert", command=self.convert).grid(row=5, column=1, pady=20)

    def update_units(self, event=None):
        """Update available units based on selected conversion type"""
        conv_type = self.conversion_type.get()
        units = self.units[conv_type]["units"]

        self.input_unit_dropdown.config(values=units)  # Update dropdown values
        self.output_unit_dropdown.config(values=units)  # Update dropdown values

        self.input_unit.set(units[0])  # Set default unit
        self.output_unit.set(units[1])

    def convert(self):
        """Perform unit conversion"""
        try:
            value = float(self.input_value.get())
            from_unit = self.input_unit.get()
            to_unit = self.output_unit.get()
            conv_type = self.conversion_type.get()

            # Special case for temperature conversions
            if self.units[conv_type].get("formula") == "special":
                result = self.convert_temperature(value, from_unit, to_unit)
            else:
                # Normal unit conversions
                from_idx = self.units[conv_type]["units"].index(from_unit)
                to_idx = self.units[conv_type]["units"].index(to_unit)
                factor = self.units[conv_type]["factors"][to_idx] / self.units[conv_type]["factors"][from_idx]
                result = value * factor

            self.output_value.set(f"{result:.4f}")

        except ValueError:
            messagebox.showerror("Error", "Invalid input value! Please enter a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion error: {str(e)}")

    def convert_temperature(self, value, from_unit, to_unit):
        """Handles temperature conversions separately"""
        if from_unit == to_unit:
            return value
        elif from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9 / 5) + 32
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5 / 9
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5 / 9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9 / 5 + 32
        else:
            raise ValueError("Invalid temperature conversion")


if __name__ == "__main__":
    UnitConverterApp()
