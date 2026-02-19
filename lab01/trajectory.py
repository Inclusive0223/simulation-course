import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class TrajectoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование траектории полёта тела")
        self.root.geometry("1200x700")
        
        # Переменные для хранения значений
        self.g = tk.DoubleVar(value=9.81)
        self.m = tk.DoubleVar(value=1.0)
        self.k = tk.DoubleVar(value=0.1)
        self.v0 = tk.DoubleVar(value=50.0)
        self.angle = tk.DoubleVar(value=45.0)
        self.y0 = tk.DoubleVar(value=0.0)
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Левая панель с параметрами
        left_frame = ttk.LabelFrame(main_frame, text="Параметры модели", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Поля ввода параметров
        params = [
            ("Ускорение свободного падения, м/с²:", self.g),
            ("Масса тела, кг:", self.m),
            ("Коэффициент сопротивления:", self.k),
            ("Начальная скорость, м/с:", self.v0),
            ("Угол бросания, градусы:", self.angle),
            ("Начальная высота, м:", self.y0)
        ]
        
        for i, (label, var) in enumerate(params):
            ttk.Label(left_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            ttk.Entry(left_frame, textvariable=var, width=15).grid(row=i, column=1, padx=5, pady=5)
        
        # Кнопки управления
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=len(params), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Рассчитать", command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить", command=self.clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Сохранить таблицу", command=self.save_table).pack(side=tk.LEFT, padx=5)
        
        # Центральная панель с графиком
        middle_frame = ttk.Frame(main_frame)
        middle_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Создание фигуры для графика
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=middle_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Правая панель с таблицей
        right_frame = ttk.LabelFrame(main_frame, text="Результаты расчёта", padding="10")
        right_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Текстовое поле для вывода таблицы
        self.text_area = scrolledtext.ScrolledText(right_frame, width=50, height=30)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Настройка весов колонок
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.columnconfigure(2, weight=2)
        main_frame.rowconfigure(0, weight=1)
        
    def calculate(self):
        try:
            # Получение значений из полей ввода
            g = self.g.get()
            m = self.m.get()
            k = self.k.get()
            v0 = self.v0.get()
            angle = self.angle.get()
            y0 = self.y0.get()
            
            # Перевод угла в радианы
            angle_rad = np.radians(angle)
            
            # Начальные скорости
            vx0 = v0 * np.cos(angle_rad)
            vy0 = v0 * np.sin(angle_rad)
            
            # Шаги исследования
            steps = [1, 0.1, 0.01, 0.001, 0.0001]
            
            # Таблица результатов
            results = []
            
            # Очистка графика
            self.ax.clear()
            
            for dt in steps:
                t = 0
                x = 0
                y = y0
                vx = vx0
                vy = vy0
                
                x_values = [x]
                y_values = [y]
                
                max_height = y
                
                while y >= 0:
                    # Метод Эйлера
                    vx = vx - (k/m)*vx*dt
                    vy = vy - (g + (k/m)*vy)*dt
                    
                    x = x + vx*dt
                    y = y + vy*dt
                    
                    t += dt
                    
                    x_values.append(x)
                    y_values.append(y)
                    
                    if y > max_height:
                        max_height = y
                
                final_speed = np.sqrt(vx**2 + vy**2)
                
                results.append([dt, x, max_height, final_speed])
                
                self.ax.plot(x_values, y_values, label=f"dt={dt}")
            
            # Настройка графика
            self.ax.set_xlabel("Дальность, м")
            self.ax.set_ylabel("Высота, м")
            self.ax.set_title("Траектории полёта при разных шагах")
            self.ax.legend()
            self.ax.grid(True)
            
            # Обновление графика
            self.canvas.draw()
            
            # Создание и отображение таблицы
            df = pd.DataFrame(results, columns=[
                "Шаг, с",
                "Дальность полёта, м",
                "Максимальная высота, м",
                "Скорость в конечной точке, м/с"
            ])
            
            # Сохраняем DataFrame для возможности сохранения
            self.current_df = df
            
            # Очистка текстового поля и вставка новой таблицы
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, df.to_string(index=False))
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при расчёте:\n{str(e)}")
    
    def clear(self):
        """Очистка графика и таблицы"""
        self.ax.clear()
        self.canvas.draw()
        self.text_area.delete(1.0, tk.END)
        
    def save_table(self):
        """Сохранение таблицы в CSV файл"""
        if hasattr(self, 'current_df'):
            try:
                filename = "trajectory_results.csv"
                self.current_df.to_csv(filename, index=False, encoding='utf-8')
                messagebox.showinfo("Успех", f"Таблица сохранена в файл: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            messagebox.showwarning("Предупреждение", "Сначала выполните расчёт!")

def main():
    root = tk.Tk()
    app = TrajectoryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()