import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

g = 9.81          # ускорение свободного падения
m = 1.0           # масса
k = 0.1           # коэффициент сопротивления
v0 = 50.0         # начальная скорость
angle = 45        # угол (градусы)
y0 = 0.0          # начальная высота

# Перевод угла в радианы
angle_rad = np.radians(angle)

# Начальные скорости 
vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)

# Шаги исследования
steps = [1, 0.1, 0.01, 0.001, 0.0001]

# Таблица результатов
results = []

plt.figure(figsize=(10,6))

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
    
    plt.plot(x_values, y_values, label=f"dt={dt}")

plt.xlabel("Дальность, м")
plt.ylabel("Высота, м")
plt.title("Траектории полёта при разных шагах")
plt.legend()
plt.grid()
plt.show()

# Таблица
df = pd.DataFrame(results, columns=[
    "Шаг, с",
    "Дальность полёта, м",
    "Максимальная высота, м",
    "Скорость в конечной точке, м/с"
])

print(df)
