"""
Завдання 7: Метод Монте-Карло — симуляція кидання двох кубиків
Обчислює імовірності кожної суми (2–12) та порівнює з аналітичними значеннями.
"""

import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# ── Аналітичні ймовірності ────────────────────────────────────────────────────

ANALYTICAL = {
    2:  1/36,  3:  2/36,  4:  3/36,
    5:  4/36,  6:  5/36,  7:  6/36,
    8:  5/36,  9:  4/36,  10: 3/36,
    11: 2/36,  12: 1/36,
}


# ── Симуляція Монте-Карло ─────────────────────────────────────────────────────

def monte_carlo_dice(num_rolls: int = 1_000_000) -> dict[int, float]:
    """
    Симулює кидання двох кубиків num_rolls разів.
    Повертає словник {сума: ймовірність}.
    """
    counts = {s: 0 for s in range(2, 13)}

    for _ in range(num_rolls):
        roll = random.randint(1, 6) + random.randint(1, 6)
        counts[roll] += 1

    return {s: counts[s] / num_rolls for s in counts}


# ── Таблиця порівняння ────────────────────────────────────────────────────────

def print_table(mc_probs: dict, num_rolls: int):
    print(f"\n{'Сума':>5} │ {'Монте-Карло':>12} │ {'Аналітично':>12} │ {'Різниця':>10}")
    print("──────┼──────────────┼──────────────┼────────────")
    for s in range(2, 13):
        mc   = mc_probs[s]
        ana  = ANALYTICAL[s]
        diff = abs(mc - ana)
        print(f"  {s:>2}  │  {mc*100:>8.4f} %  │  {ana*100:>8.4f} %  │  {diff*100:>7.4f} %")


# ── Візуалізація ──────────────────────────────────────────────────────────────

def visualize(mc_probs: dict, num_rolls: int):
    sums = list(range(2, 13))
    mc_vals  = [mc_probs[s] * 100  for s in sums]
    ana_vals = [ANALYTICAL[s] * 100 for s in sums]

    x = range(len(sums))
    width = 0.35

    fig, ax = plt.subplots(figsize=(11, 6))

    bars_mc  = ax.bar([i - width/2 for i in x], mc_vals,  width,
                      label=f"Монте-Карло ({num_rolls:,} кидків)",
                      color='#2E86C1', alpha=0.85)
    bars_ana = ax.bar([i + width/2 for i in x], ana_vals, width,
                      label="Аналітично (теорія)",
                      color='#E67E22', alpha=0.85)

    ax.set_xlabel("Сума двох кубиків", fontsize=12)
    ax.set_ylabel("Імовірність (%)", fontsize=12)
    ax.set_title("Метод Монте-Карло vs аналітичні розрахунки\n"
                 "Імовірності сум при киданні двох кубиків", fontsize=13)
    ax.set_xticks(list(x))
    ax.set_xticklabels(sums)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    # Підписи значень на стовпцях
    for bar in bars_mc:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                f"{bar.get_height():.2f}%",
                ha='center', va='bottom', fontsize=7.5, color='#1A5276')

    plt.tight_layout()
    out_path = "task7_monte_carlo.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"\nГрафік збережено: {out_path}")


# ── Демонстрація ──────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  Завдання 7: Метод Монте-Карло (два кубики)")
    print("=" * 55)

    NUM_ROLLS = 1_000_000
    print(f"\nСимулюємо {NUM_ROLLS:,} кидків...")

    random.seed(42)   # для відтворюваності результатів
    mc_probs = monte_carlo_dice(NUM_ROLLS)

    print_table(mc_probs, NUM_ROLLS)
    visualize(mc_probs, NUM_ROLLS)

    # Середня абсолютна похибка
    mae = sum(abs(mc_probs[s] - ANALYTICAL[s]) for s in range(2, 13)) / 11
    print(f"\nСередня абсолютна похибка: {mae*100:.5f} %")
    print("\nВисновок: результати методу Монте-Карло добре узгоджуються з")
    print("аналітичними значеннями. Чим більше кидків — тим точніший результат")
    print("(закон великих чисел). Детальніші висновки — у README.md.")


if __name__ == "__main__":
    main()