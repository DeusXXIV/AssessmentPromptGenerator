import tkinter as tk
from tkinter import ttk, messagebox
from template_manager import TemplateManager

class PromptGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatGPT Prompt Generator")

        # Initialize TemplateManager with the root (or another parent) argument
        self.template_manager = TemplateManager(self.root)

        # Initialize UI components
        self.create_widgets()

        # Set the window size and center it on the screen
        self.window_width = 1080
        self.window_height = 800
        self.center_window(self.window_width, self.window_height)

    def center_window(self, width, height):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position x and y coordinates to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the window position and size
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Center frame for all widgets
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Label for role selection
        tk.Label(main_frame, text="What role will GPT play?").grid(row=0, column=0, pady=5, sticky="e")

        # Dropdown menu for role selection
        self.role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(main_frame, textvariable=self.role_var, state="readonly")
        role_dropdown['values'] = ("College Professor", "Student")
        role_dropdown.current(0)
        role_dropdown.grid(row=0, column=1, pady=5, sticky="w")

        # Label for assessment selection
        tk.Label(main_frame, text="What assessment?").grid(row=1, column=0, pady=5, sticky="e")

        # Dropdown menu for assessment selection
        self.assessment_var = tk.StringVar()
        assessment_dropdown = ttk.Combobox(main_frame, textvariable=self.assessment_var, state="readonly")
        assessment_dropdown['values'] = ("Exam", "Activity", "Quiz")
        assessment_dropdown.current(0)
        assessment_dropdown.grid(row=1, column=1, pady=5, sticky="w")
        assessment_dropdown.bind("<<ComboboxSelected>>", self.on_assessment_change)

        # Label and entry for topic input
        tk.Label(main_frame, text="Topic here").grid(row=2, column=0, pady=5, sticky="e")
        self.topic_entry = tk.Entry(main_frame, width=50)
        self.topic_entry.grid(row=2, column=1, pady=5, sticky="w")

        # Initialize exam options frame
        self.exam_options_frame = tk.Frame(main_frame)
        self.create_exam_options()

        # Button to generate the prompt
        tk.Button(main_frame, text="Generate Prompt", command=self.generate_prompt).grid(row=5, column=0, columnspan=2, pady=10)

        # Text widget to display the generated prompt (copy-paste-able but not editable)
        self.result_text = tk.Text(main_frame, height=10, width=100, wrap="word")
        self.result_text.grid(row=6, column=0, columnspan=2, pady=10)
        self.result_text.config(state='disabled')  # Disable editing initially

        # Button for managing templates
        tk.Button(main_frame, text="Save Template", command=self.template_manager.save_template).grid(row=7, column=0, pady=5)
        tk.Button(main_frame, text="Load Template", command=self.template_manager.load_template).grid(row=7, column=1, pady=5)
        tk.Button(main_frame, text="Delete Template", command=self.template_manager.delete_template).grid(row=7, column=2, pady=5)
        tk.Button(main_frame, text="Clear Inputs", command=self.clear_inputs).grid(row=7, column=3, pady=5)

    def create_exam_options(self):
        # Label for exam types
        tk.Label(self.exam_options_frame, text="Exam/Quiz Types, Quantities, and Points per Item:").grid(row=0, column=0, columnspan=7, pady=5)

        # Frame for exam/quiz types, quantities, points per item, and instructions
        self.exam_type_vars = {}
        self.exam_type_var = {
            "Multiple Choice": tk.BooleanVar(),
            "True or False": tk.BooleanVar(),
            "Modified True or False": tk.BooleanVar(),
            "Identification": tk.BooleanVar(),
            "Essay": tk.BooleanVar()
        }

        row = 1
        for exam_type in self.exam_type_var:
            checkbox = tk.Checkbutton(self.exam_options_frame, text=exam_type, variable=self.exam_type_var[exam_type], command=lambda et=exam_type: self.toggle_inputs(et))
            checkbox.grid(row=row, column=0, padx=5, sticky="w")

            items_label = tk.Label(self.exam_options_frame, text="Items:")
            items_label.grid(row=row, column=1, padx=5)

            item_entry = tk.Entry(self.exam_options_frame, width=5, state='disabled')
            item_entry.grid(row=row, column=2, padx=5)

            points_label = tk.Label(self.exam_options_frame, text="Points per Item:")
            points_label.grid(row=row, column=3, padx=5)

            points_entry = tk.Entry(self.exam_options_frame, width=5, state='disabled')
            points_entry.grid(row=row, column=4, padx=5)

            instructions_label = tk.Label(self.exam_options_frame, text="Instructions:")
            instructions_label.grid(row=row, column=5, padx=5)

            instructions_text = tk.Text(self.exam_options_frame, width=40, height=3, state='disabled', wrap="word")
            instructions_text.grid(row=row, column=6, padx=5)

            self.exam_type_vars[exam_type] = {
                'items': item_entry,
                'points': points_entry,
                'instructions': instructions_text
            }

            row += 1

        self.exam_options_frame.grid(row=4, column=0, columnspan=2, pady=10)

    def toggle_inputs(self, exam_type):
        if self.exam_type_var[exam_type].get():
            self.exam_type_vars[exam_type]['items'].config(state='normal')
            self.exam_type_vars[exam_type]['points'].config(state='normal')
            self.exam_type_vars[exam_type]['points'].delete(0, tk.END)  # Clear existing text
            self.exam_type_vars[exam_type]['points'].insert(0, "1")  # Set default value to 1
            self.exam_type_vars[exam_type]['instructions'].config(state='normal')
        else:
            self.exam_type_vars[exam_type]['items'].config(state='disabled')
            self.exam_type_vars[exam_type]['points'].config(state='disabled')
            self.exam_type_vars[exam_type]['instructions'].config(state='disabled')

    def generate_prompt(self):
        role = self.role_var.get()
        assessment = self.assessment_var.get()
        topic = self.topic_entry.get()

        # Ensure the topic is provided
        if not topic:
            messagebox.showerror("Input Error", "Please enter a topic.")
            return

        # Start forming the prompt message
        prompt_message = f"Pretend you are a {role}, I want you to create a {assessment} for the topic {topic}."

        # Handle exam/quiz types if the assessment is an exam or quiz
        if assessment in ["Exam", "Quiz"]:
            selected_exam_types = []
            for exam_type, entries in self.exam_type_vars.items():
                if self.exam_type_var[exam_type].get():
                    items_count = entries['items'].get()
                    points_per_item = entries['points'].get()
                    instructions = entries['instructions'].get("1.0", tk.END).strip()

                    if not items_count.isdigit() or int(items_count) <= 0:
                        messagebox.showerror("Input Error", f"Please enter a valid number of items for {exam_type}.")
                        return
                    if not points_per_item.isdigit() or int(points_per_item) <= 0:
                        messagebox.showerror("Input Error", f"Please enter a valid number of points for {exam_type}.")
                        return

                    exam_type_message = f"{exam_type} with {items_count} items, {points_per_item} points each"
                    if instructions:
                        exam_type_message += f", Instructions: {instructions}"

                    selected_exam_types.append(exam_type_message)

            if not selected_exam_types:
                messagebox.showerror("Input Error", "Please select at least one exam/quiz type.")
                return

            # Append exam/quiz types to the prompt message
            exam_types_message = f" The {assessment.lower()} should include: " + ", ".join(selected_exam_types) + "."
            prompt_message += exam_types_message

        # Enable the Text widget to modify its content, then insert and disable editing
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, prompt_message)
        self.result_text.config(state='disabled')  # Disable editing

    def on_assessment_change(self, event):
        selected_assessment = self.assessment_var.get()
        if selected_assessment in ["Exam", "Quiz"]:
            self.exam_options_frame.grid(row=4, column=0, columnspan=2, pady=10)
        else:
            self.exam_options_frame.grid_forget()

    def clear_inputs(self):
        self.role_var.set("College Professor")
        self.assessment_var.set("Exam")
        self.topic_entry.delete(0, tk.END)
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state='disabled')

        for exam_type, entries in self.exam_type_vars.items():
            self.exam_type_var[exam_type].set(False)
            entries['items'].config(state='disabled')
            entries['points'].config(state='disabled')
            entries['instructions'].config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = PromptGeneratorApp(root)
    root.mainloop()

