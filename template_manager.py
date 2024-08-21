import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

class TemplateManager:
    def __init__(self, parent):
        self.parent = parent
        self.templates_file = "templates.json"
        self.templates = self.load_templates()

    def load_templates(self):
        if os.path.exists(self.templates_file):
            with open(self.templates_file, 'r') as file:
                return json.load(file)
        return {}

    def save_template(self):
        template_name = simpledialog.askstring("Save Template", "Enter a name for the template:")
        if not template_name:
            messagebox.showerror("Input Error", "Template name cannot be empty.")
            return

        # Create template data
        template_data = {
            'role': self.parent.role_var.get(),
            'assessment': self.parent.assessment_var.get(),
            'topic': self.parent.topic_entry.get(),
            'exam_types': {}
        }

        for exam_type, entries in self.parent.exam_type_vars.items():
            if self.parent.exam_type_var[exam_type].get():
                template_data['exam_types'][exam_type] = {
                    'items': entries['items'].get(),
                    'points': entries['points'].get(),
                    'instructions': entries['instructions'].get("1.0", tk.END).strip()
                }

        self.templates[template_name] = template_data

        with open(self.templates_file, 'w') as file:
            json.dump(self.templates, file, indent=4)

        messagebox.showinfo("Success", "Template saved successfully!")

    def load_template(self):
        if not self.templates:
            messagebox.showinfo("No Templates", "No templates available to load.")
            return

        template_name = simpledialog.askstring("Load Template", "Enter the name of the template to load:")
        if template_name not in self.templates:
            messagebox.showerror("Template Not Found", "The specified template was not found.")
            return

        template_data = self.templates[template_name]
        self.parent.role_var.set(template_data['role'])
        self.parent.assessment_var.set(template_data['assessment'])
        self.parent.topic_entry.delete(0, tk.END)
        self.parent.topic_entry.insert(0, template_data['topic'])

        for exam_type, data in template_data['exam_types'].items():
            if exam_type in self.parent.exam_type_vars:
                self.parent.exam_type_var[exam_type].set(True)
                entries = self.parent.exam_type_vars[exam_type]
                entries['items'].config(state='normal')
                entries['items'].delete(0, tk.END)
                entries['items'].insert(0, data['items'])
                entries['points'].config(state='normal')
                entries['points'].delete(0, tk.END)
                entries['points'].insert(0, data['points'])
                entries['instructions'].config(state='normal')
                entries['instructions'].delete("1.0", tk.END)
                entries['instructions'].insert("1.0", data['instructions'])
            else:
                self.parent.exam_type_var[exam_type].set(False)

        self.parent.on_assessment_change(None)

    def delete_template(self):
        if not self.templates:
            messagebox.showinfo("No Templates", "No templates available to delete.")
            return

        template_name = simpledialog.askstring("Delete Template", "Enter the name of the template to delete:")
        if template_name not in self.templates:
            messagebox.showerror("Template Not Found", "The specified template was not found.")
            return

        del self.templates[template_name]

        with open(self.templates_file, 'w') as file:
            json.dump(self.templates, file, indent=4)

        messagebox.showinfo("Success", "Template deleted successfully!")

