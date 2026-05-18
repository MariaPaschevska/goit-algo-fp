# Налаштування віртуального середовища

## 1. Створити віртуальне середовище

Виконайте команду у папці проєкту:

```bash
python -m venv venv
```

## 2. Активувати його

**macOS / Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

> ✅ Перевірка: після активації на початку рядка терміналу має з'явитися `(venv)`:
> 
> Якщо `(venv)` немає — середовище не активовано, і `pip install` встановить пакети глобально, а не у середовище.

## 3. Встановити залежності

```bash
pip install -r requirements.txt
```

Перевірити, що пакети встановлено:
```bash
pip list
```

У списку мають бути `matplotlib` та `networkx`.

## 4. Запускати завдання

```bash
python task3_dijkstra.py
python task4_heap_visualization.py
python task5_tree_traversal.py
python task6_greedy_dp.py
python task7_monte_carlo.py
```

> ⚠️ Завдання 1 і 2 не потребують додаткових бібліотек і запускаються без віртуального середовища.

## 5. Деактивувати середовище після роботи

```bash
deactivate
```

---

## Типові помилки

**`ModuleNotFoundError: No module named 'networkx'`**
→ Середовище не активовано або `pip install -r requirements.txt` не виконано. Активуйте `venv` і повторіть крок 3.

**`python: command not found`**
→ Спробуйте `python3` замість `python`.

**`pip: command not found`**
→ Спробуйте `pip3` замість `pip`.
