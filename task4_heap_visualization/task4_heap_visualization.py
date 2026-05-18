"""
Завдання 4: Візуалізація бінарної купи
Використовує наданий базовий код як основу.
Функція heap_to_tree будує дерево із купи (списку) та відображає його.
"""

import uuid
import networkx as nx
import matplotlib.pyplot as plt


# ── Базовий код (наданий у завданні) ─────────────────────────────────────────

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title="Бінарне дерево"):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(9, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2000, node_color=colors, font_size=12, font_weight='bold')
    plt.title(title, fontsize=13)
    plt.tight_layout()

    out_path = "task4_heap_tree.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Збережено: {out_path}")


# ── Нова функція: побудова дерева з купи ─────────────────────────────────────

def heap_to_tree(heap: list) -> Node | None:
    """
    Перетворює список-купу на бінарне дерево з вузлів Node.

    У бінарній купі (представленій масивом):
        - лівий нащадок елемента i  → індекс 2*i + 1
        - правий нащадок елемента i → індекс 2*i + 2

    Параметри:
        heap — список значень, що представляє бінарну купу

    Повертає:
        корінь побудованого бінарного дерева або None для порожнього списку
    """
    if not heap:
        return None

    # Створюємо всі вузли одразу
    nodes = [Node(val) for val in heap]

    # Зв'язуємо нащадків
    for i in range(len(heap)):
        left_idx  = 2 * i + 1
        right_idx = 2 * i + 2
        if left_idx < len(heap):
            nodes[i].left = nodes[left_idx]
        if right_idx < len(heap):
            nodes[i].right = nodes[right_idx]

    return nodes[0]  # корінь — перший елемент


def visualize_heap(heap: list):
    """Головна функція: приймає список-купу і візуалізує її як дерево."""
    print(f"Купа (масив): {heap}")

    root = heap_to_tree(heap)
    if root is None:
        print("Порожня купа.")
        return

    draw_tree(root, title=f"Візуалізація бінарної купи: {heap}")


# ── Демонстрація ──────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Завдання 4: Візуалізація бінарної купи")
    print("=" * 50)

    # Мін-купа (heapq за замовчуванням будує мін-купу)
    import heapq
    data = [15, 10, 8, 5, 4, 20, 3, 1, 12, 7]
    heapq.heapify(data)

    print(f"\nВихідні дані:  {sorted(data)}")
    print(f"Після heapify: {data}")
    print()

    visualize_heap(data)


if __name__ == "__main__":
    main()