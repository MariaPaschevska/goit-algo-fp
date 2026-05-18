"""
Завдання 5: Візуалізація обходу бінарного дерева (DFS та BFS)
- DFS реалізовано через стек (без рекурсії)
- BFS реалізовано через чергу (без рекурсії)
- Кольори вузлів змінюються від темних до світлих за порядком відвідування
"""

import uuid
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


# ── Клас вузла (з завдання 4) ─────────────────────────────────────────────────

class Node:
    def __init__(self, key, color="#000000"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


# ── Побудова дерева з купи (з завдання 4) ─────────────────────────────────────

def heap_to_tree(heap: list) -> Node | None:
    if not heap:
        return None
    nodes = [Node(val) for val in heap]
    for i in range(len(heap)):
        if 2 * i + 1 < len(heap):
            nodes[i].left = nodes[2 * i + 1]
        if 2 * i + 2 < len(heap):
            nodes[i].right = nodes[2 * i + 2]
    return nodes[0]


# ── Генератор кольорів: темний → світлий ──────────────────────────────────────

def generate_colors(n: int, base_rgb: tuple) -> list[str]:
    """
    Генерує n кольорів від темного до світлого відтінку заданого базового кольору.

    base_rgb — базовий колір у форматі (R, G, B), де кожна компонента 0–255.
    Повертає список hex-рядків (#RRGGBB).
    """
    colors = []
    r0, g0, b0 = base_rgb
    for i in range(n):
        ratio = i / max(n - 1, 1)   # 0.0 (темний) → 1.0 (світлий)
        r = int(r0 + (255 - r0) * ratio)
        g = int(g0 + (255 - g0) * ratio)
        b = int(b0 + (255 - b0) * ratio)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors


# ── DFS — обхід у глибину через стек ──────────────────────────────────────────

def dfs(root: Node) -> list[Node]:
    """
    Обхід дерева у глибину (DFS) за допомогою стека.
    Повертає список вузлів у порядку відвідування.
    """
    if root is None:
        return []

    order = []
    stack = [root]          # стек — звичайний список Python

    while stack:
        node = stack.pop()  # беремо з вершини стека
        order.append(node)

        # Спочатку правий — щоб лівий опинився на вершині стека
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order


# ── BFS — обхід у ширину через чергу ─────────────────────────────────────────

def bfs(root: Node) -> list[Node]:
    """
    Обхід дерева у ширину (BFS) за допомогою черги.
    Повертає список вузлів у порядку відвідування.
    """
    if root is None:
        return []

    order = []
    queue = deque([root])   # deque як черга

    while queue:
        node = queue.popleft()  # беремо з початку черги
        order.append(node)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return order


# ── Візуалізація одного обходу ─────────────────────────────────────────────────

def draw_traversal(root: Node, traversal_order: list[Node],
                   title: str, base_rgb: tuple, out_path: str):
    """Малює дерево, де колір вузла відображає порядок відвідування."""

    # Призначаємо кольори вузлам за порядком обходу
    colors_list = generate_colors(len(traversal_order), base_rgb)
    color_map = {node.id: colors_list[i]
                 for i, node in enumerate(traversal_order)}

    # Будуємо граф
    def add_edges(graph, node, pos, x=0, y=0, layer=1):
        if node:
            graph.add_node(node.id,
                           color=color_map.get(node.id, "#DDDDDD"),
                           label=node.val)
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

    G = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(G, root, pos)

    node_colors = [data['color'] for _, data in G.nodes(data=True)]
    labels = {nid: data['label'] for nid, data in G.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(9, 6))
    nx.draw(G, pos=pos, labels=labels, arrows=False,
            node_size=1800, node_color=node_colors,
            font_size=11, font_weight='bold', font_color='white', ax=ax)

    # Легенда — порядок відвідування
    order_str = " → ".join(str(n.val) for n in traversal_order)
    ax.set_title(f"{title}\nПорядок: {order_str}", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Збережено: {out_path}")


# ── Демонстрація ──────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Завдання 5: Обхід дерева (DFS та BFS)")
    print("=" * 50)

    heap = [0, 4, 1, 5, 10, 3]
    root = heap_to_tree(heap)

    # DFS (темно-синій → світло-блакитний)
    print("\nDFS — обхід у глибину (стек):")
    dfs_order = dfs(root)
    print("  Порядок:", [n.val for n in dfs_order])
    draw_traversal(root, dfs_order,
                   title="DFS — обхід у глибину",
                   base_rgb=(18, 150, 240),   # #1296F0
                   out_path="task5_dfs.png")

    # Перебудовуємо дерево (вузли мають змінювані кольори)
    root = heap_to_tree(heap)

    # BFS (темно-зелений → світло-зелений)
    print("\nBFS — обхід у ширину (черга):")
    bfs_order = bfs(root)
    print("  Порядок:", [n.val for n in bfs_order])
    draw_traversal(root, bfs_order,
                   title="BFS — обхід у ширину",
                   base_rgb=(10, 120, 60),    # темно-зелений
                   out_path="task5_bfs.png")


if __name__ == "__main__":
    main()