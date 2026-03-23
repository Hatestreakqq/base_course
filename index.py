import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
import os

# Параметры модели
SIZE = 100          # Размер поля
PARTICLES = 1500    # Количество частиц
SAVE_EVERY = 20     # Сохранять каждый N-й шаг для скорости

def simulate_crystal():
    field = np.zeros((SIZE, SIZE))
    center = SIZE // 2
    field[center, center] = 1
    
    frames = []
    
    print("Моделирование началось...")

    for p in range(PARTICLES):
        # Появление частицы на границе
        side = random.randint(0, 3)
        if side == 0: x, y = random.randint(0, SIZE-1), 0
        elif side == 1: x, y = random.randint(0, SIZE-1), SIZE-1
        elif side == 2: x, y = 0, random.randint(0, SIZE-1)
        else: x, y = SIZE-1, random.randint(0, SIZE-1)

        while True:
            # Броуновское движение
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < SIZE and 0 <= ny < SIZE:
                # Проверка соседей на наличие кристалла
                subset = field[max(0, nx-1):min(SIZE, nx+2), max(0, ny-1):min(SIZE, ny+2)]
                if np.any(subset == 1):
                    field[nx, ny] = 1
                    
                    # Сохраняем кадр каждые SAVE_EVERY частиц
                    if p % SAVE_EVERY == 0:
                        # Преобразуем массив в картинку (инвертируем цвета для красоты)
                        img_data = (1 - field) * 255
                        img = Image.fromarray(img_data.astype(np.uint8)).convert("L")
                        frames.append(img.resize((400, 400), resample=Image.NEAREST))
                    break
                x, y = nx, ny
            else:
                break # Вылет за границы

        if p % 500 == 0:
            print(f"Обработано частиц: {p}")

    # Сохранение в GIF
    if frames:
        frames[0].save(
            'crystal.gif',
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=50,
            loop=0
        )
        print("Готово! Файл 'crystal.gif' создан.")

if __name__ == "__main__":
    simulate_crystal()
