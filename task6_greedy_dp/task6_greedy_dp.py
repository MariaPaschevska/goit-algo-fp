"""
Завдання 6: Жадібний алгоритм та динамічне програмування
Оптимізація вибору їжі з максимальною калорійністю в межах бюджету.
"""

# ── Вхідні дані ───────────────────────────────────────────────────────────────

items = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}


# ── Жадібний алгоритм ─────────────────────────────────────────────────────────

def greedy_algorithm(items: dict, budget: int) -> tuple[list, int]:
    """
    Жадібний алгоритм: обирає страви з найкращим співвідношенням
    калорії/вартість, поки вистачає бюджету.

    Параметри:
        items  — словник страв {назва: {cost, calories}}
        budget — максимальний бюджет

    Повертає:
        (список обраних страв, сумарна калорійність)
    """
    # Сортуємо за спаданням співвідношення калорії/вартість
    sorted_items = sorted(
        items.items(),
        key=lambda x: x[1]["calories"] / x[1]["cost"],
        reverse=True
    )

    chosen = []
    total_calories = 0
    remaining_budget = budget

    for name, info in sorted_items:
        if info["cost"] <= remaining_budget:
            chosen.append(name)
            total_calories += info["calories"]
            remaining_budget -= info["cost"]

    return chosen, total_calories


# ── Динамічне програмування ───────────────────────────────────────────────────

def dynamic_programming(items: dict, budget: int) -> tuple[list, int]:
    """
    Алгоритм динамічного програмування (задача про рюкзак 0/1).
    Знаходить оптимальний набір страв для максимізації калорійності.

    Параметри:
        items  — словник страв {назва: {cost, calories}}
        budget — максимальний бюджет

    Повертає:
        (список обраних страв, максимальна сумарна калорійність)
    """
    names = list(items.keys())
    n = len(names)
    costs = [items[name]["cost"] for name in names]
    calories = [items[name]["calories"] for name in names]

    # Таблиця DP: dp[i][w] = максимальна калорійність для перших i страв і бюджету w
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(budget + 1):
            # Не беремо страву i
            dp[i][w] = dp[i - 1][w]
            # Беремо страву i (якщо вистачає бюджету)
            if costs[i - 1] <= w:
                take = dp[i - 1][w - costs[i - 1]] + calories[i - 1]
                if take > dp[i][w]:
                    dp[i][w] = take

    # Відновлення обраних страв (traceback)
    chosen = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(names[i - 1])
            w -= costs[i - 1]
    chosen.reverse()

    return chosen, dp[n][budget]


# ── Демонстрація ──────────────────────────────────────────────────────────────

def print_result(method: str, chosen: list, total_cal: int,
                 items: dict, budget: int):
    spent = sum(items[name]["cost"] for name in chosen)
    print(f"\n  Метод: {method}")
    print(f"  Бюджет: {budget} грн   Витрачено: {spent} грн")
    print(f"  Обрані страви:")
    for name in chosen:
        info = items[name]
        ratio = info["calories"] / info["cost"]
        print(f"    • {name:<12}  вартість={info['cost']:>3}  "
              f"калорії={info['calories']:>4}  "
              f"кал/грн={ratio:.1f}")
    print(f"  Загальна калорійність: {total_cal} ккал")


def main():
    print("=" * 55)
    print("  Завдання 6: Оптимізація бюджету")
    print("=" * 55)

    budget = 100

    print(f"\nДоступні страви (бюджет = {budget} грн):")
    print(f"  {'Назва':<12} {'Вартість':>9} {'Калорії':>8} {'кал/грн':>8}")
    print("  " + "-" * 40)
    for name, info in items.items():
        ratio = info["calories"] / info["cost"]
        print(f"  {name:<12} {info['cost']:>9} {info['calories']:>8} {ratio:>8.1f}")

    # Жадібний
    g_chosen, g_cal = greedy_algorithm(items, budget)
    print_result("Жадібний алгоритм", g_chosen, g_cal, items, budget)

    # Динамічне програмування
    d_chosen, d_cal = dynamic_programming(items, budget)
    print_result("Динамічне програмування", d_chosen, d_cal, items, budget)

    # Порівняння
    print("\n" + "=" * 55)
    print("  Порівняння результатів:")
    print(f"  Жадібний:  {g_cal} ккал  →  {g_chosen}")
    print(f"  Динамічне: {d_cal} ккал  →  {d_chosen}")
    if d_cal > g_cal:
        print(f"\n  ✓ ДП знайшло кращий розв'язок на {d_cal - g_cal} ккал")
    elif d_cal == g_cal:
        print("\n  ✓ Обидва методи дали однаковий результат")


if __name__ == "__main__":
    main()