"""
Завдання 2: Фрактал «Дерево Піфагора» за допомогою рекурсії
Користувач вказує рівень рекурсії.
Малюємо лише лінії, без заповнених квадратів.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def draw_pythagorean_tree(ax, x1, y1, x2, y2, depth, max_depth):
    """
    Рекурсивно малює гілки дерева Піфагора.

    Параметри:
        ax            — об'єкт осей matplotlib
        x1, y1        — нижня-ліва точка основи поточного квадрата
        x2, y2        — нижня-права точка основи поточного квадрата
        depth         — поточна глибина рекурсії
        max_depth     — максимальна глибина рекурсії (задає користувач)
    """
    if depth > max_depth:
        return

    # Вектор основи квадрата
    dx = x2 - x1
    dy = y2 - y1

    # Чотири кути квадрата (проти годинникової стрілки)
    # p1 = (x1, y1), p2 = (x2, y2)
    # p3 = p2 + перпендикуляр, p4 = p1 + перпендикуляр
    p3x = x2 - dy
    p3y = y2 + dx
    p4x = x1 - dy
    p4y = y1 + dx

    # Малюємо контур квадрата (4 сторони)
    square_x = [x1, x2, p3x, p4x, x1]
    square_y = [y1, y2, p3y, p4y, y1]
    ax.plot(square_x, square_y, color='#8B1A1A', linewidth=0.8)

    # Вершина рівнобедреного прямокутного трикутника
    # між верхніми двома кутами квадрата
    apex_x = p4x + (p3x - p4x) / 2 - (p3y - p4y) / 2
    apex_y = p4y + (p3y - p4y) / 2 + (p3x - p4x) / 2

    # Ліва гілка: від p4 до вершини трикутника
    draw_pythagorean_tree(ax, p4x, p4y, apex_x, apex_y, depth + 1, max_depth)

    # Права гілка: від вершини трикутника до p3
    draw_pythagorean_tree(ax, apex_x, apex_y, p3x, p3y, depth + 1, max_depth)


def visualize(max_depth: int):
    """Будує та відображає дерево Піфагора заданої глибини."""
    fig, ax = plt.subplots(figsize=(9, 9), facecolor='white')
    ax.set_facecolor('white')
    ax.set_aspect('equal')
    ax.axis('off')

    # Основа дерева — горизонтальний відрізок внизу по центру
    base = 1.0
    x1, y1 = -base / 2, 0
    x2, y2 =  base / 2, 0

    draw_pythagorean_tree(ax, x1, y1, x2, y2, depth=0, max_depth=max_depth)

    ax.set_title(
        f"Дерево Піфагора  |  рівень рекурсії = {max_depth}",
        fontsize=13, color='#8B1A1A', pad=10
    )
    ax.autoscale()
    plt.tight_layout()

    out_path = "task2_pythagorean_tree.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    print(f"Збережено: {out_path}")


def main():
    print("=" * 50)
    print("  Завдання 2: Дерево Піфагора (рекурсія)")
    print("=" * 50)

    try:
        level = int(input("\nВведіть рівень рекурсії (рекомендовано 5–11): "))
        if level < 1:
            raise ValueError
    except ValueError:
        print("Некоректне значення. Використовую рівень 9.")
        level = 9

    print(f"\nБудую дерево глибиною {level}...")
    visualize(level)


if __name__ == "__main__":
    main()