import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageFilter, ImageEnhance
import threading

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        root.title("Обработка изображений")

        # Переменные для хранения путей к входной и выходной папкам
        self.input_folder_var = tk.StringVar()
        self.output_folder_var = tk.StringVar()

        # Создаем стили ttk
        style = ttk.Style()
        style.configure("TButton", padding=5, relief="flat", background="#ccc")

        # Выбор входной папки
        input_folder_frame = tk.Frame(root)
        input_folder_frame.pack(pady=10)
        input_folder_label = ttk.Label(input_folder_frame, text="Выберите входную папку:")
        input_folder_label.grid(row=0, column=0, padx=5)
        input_folder_entry = ttk.Entry(input_folder_frame, textvariable=self.input_folder_var, width=30)
        input_folder_entry.grid(row=0, column=1, padx=5)
        input_folder_button = ttk.Button(input_folder_frame, text="Обзор", command=self.browse_input_folder)
        input_folder_button.grid(row=0, column=2, padx=5)

        # Выбор выходной папки
        output_folder_frame = tk.Frame(root)
        output_folder_frame.pack(pady=10)
        output_folder_label = ttk.Label(output_folder_frame, text="Выберите выходную папку:")
        output_folder_label.grid(row=0, column=0, padx=5)
        output_folder_entry = ttk.Entry(output_folder_frame, textvariable=self.output_folder_var, width=30)
        output_folder_entry.grid(row=0, column=1, padx=5)
        output_folder_button = ttk.Button(output_folder_frame, text="Обзор", command=self.browse_output_folder)
        output_folder_button.grid(row=0, column=2, padx=5)

        # Флажки для выбора фильтров
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)
        self.sharpness_var = tk.BooleanVar()
        sharpness_checkbox = ttk.Checkbutton(filter_frame, text="Увеличение резкости", variable=self.sharpness_var)
        sharpness_checkbox.grid(row=0, column=0, padx=5)
        self.sepia_var = tk.BooleanVar()
        sepia_checkbox = ttk.Checkbutton(filter_frame, text="Сепия", variable=self.sepia_var)
        sepia_checkbox.grid(row=0, column=1, padx=5)
        self.resize_var = tk.BooleanVar()
        resize_checkbox = ttk.Checkbutton(filter_frame, text="Уменьшение размера", variable=self.resize_var)
        resize_checkbox.grid(row=0, column=2, padx=5)

        # Кнопка для обработки изображений
        process_button = ttk.Button(root, text="Обработать изображения", command=self.start_processing, style="TButton")
        process_button.pack(pady=10)

    def browse_input_folder(self):
        input_folder = filedialog.askdirectory()
        self.input_folder_var.set(input_folder)

    def browse_output_folder(self):
        output_folder = filedialog.askdirectory()
        self.output_folder_var.set(output_folder)

    def process_image(self, image_path, output_folder, filters):
        try:
            img = Image.open(image_path)

            if "sharpness" in filters:
                img = ImageEnhance.Sharpness(img).enhance(7.0)
            if "sepia" in filters:
                img = img.convert('L').filter(ImageFilter.CONTOUR)
            if "resize" in filters:
                img = img.resize((100, 100))

            # Сохраняем обработанное изображение в выходную папку
            output_path = os.path.join(output_folder, 'processed_' + os.path.basename(image_path))
            img.save(output_path)
            print(f"Обработано изображение: {output_path}")
        except Exception as e:
            print(f"Ошибка обработки {image_path}: {str(e)}")

    def start_processing(self):
        input_folder = self.input_folder_var.get()
        output_folder = self.output_folder_var.get()

        # Проверка, выбраны ли хотя бы один фильтр и указаны ли папки
        if not any([self.sharpness_var.get(), self.sepia_var.get(), self.resize_var.get()]):
            print("Выберите хотя бы один фильтр для обработки.")
            return

        if not input_folder or not output_folder:
            print("Выберите входную и выходную папки.")
            return

        # Обработка изображений в отдельных потоках
        threads = []
        for filename in os.listdir(input_folder):
            image_path = os.path.join(input_folder, filename)
            thread = threading.Thread(target=self.process_image, args=(image_path, output_folder, self.get_selected_filters()))
            threads.append(thread)
            thread.start()

        # Ожидание завершения всех потоков
        for thread in threads:
            thread.join()

    def get_selected_filters(self):
        selected_filters = []
        if self.sharpness_var.get():
            selected_filters.append("sharpness")
        if self.sepia_var.get():
            selected_filters.append("sepia")
        if self.resize_var.get():
            selected_filters.append("resize")
        return selected_filters

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()
