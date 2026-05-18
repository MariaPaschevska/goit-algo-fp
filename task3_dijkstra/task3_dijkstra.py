"""
Завдання 3: Алгоритм Дейкстри з бінарною купою
Знаходить найкоротші шляхи від початкової вершини до всіх інших у зваженому графі.
"""

import heapq
import networkx as nx
import matplotlib.pyplot as plt


# ── Алгоритм Дейкстри ─────────────────────────────────────────────────────────

def dijkstra(graph: dict, start: str) -> tuple[dict, dict]:
    """
    Алгоритм Дейкстри з використанням бінарної мін-купи (heapq).

    Параметри:
        graph — словник суміжності {вузол: [(сусід, вага), ...]}
        start — початкова вершина

    Повертає:
        distances    — {вузол: мінімальна відстань від start}
        predecessors — {вузол: попередник у найкоротшому шляху}
    """
    # Ініціалізація: усі відстані — нескінченність
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}

    # Мін-купа: (відстань, вузол)
    heap = [(0, start)]
    visited = set()

    while heap:
        current_dist, current_node = heapq.heappop(heap)

        # Якщо вузол вже оброблено — пропускаємо
        if current_node in visited:
            continue
        visited.add(current_node)

        # Релаксація ребер
        for neighbor, weight in graph[current_node]:
            if neighbor in visited:
                continue
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = current_node
                heapq.heappush(heap, (new_dist, neighbor))

    return distances, predecessors


def get_path(predecessors: dict, start: str, end: str) -> list:
    """Відновлює найкоротший шлях від start до end за словником попередників."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    return path if path[0] == start else []


# ── Візуалізація ──────────────────────────────────────────────────────────────

def visualize(graph: dict, distances: dict, predecessors: dict, start: str):
    """Малює граф, виділяючи найкоротші шляхи від start."""
    G = nx.DiGraph()

    for node, neighbors in graph.items():
        for neighbor, weight in neighbors:
            G.add_edge(node, neighbor, weight=weight)

    # Збираємо ребра найкоротших шляхів
    shortest_edges = set()
    for node in graph:
        if node != start and predecessors[node] is not None:
            shortest_edges.add((predecessors[node], node))

    pos = nx.spring_layout(G, seed=42, k=2)

    plt.figure(figsize=(10, 7))

    # Кольори вузлів: початковий — помаранчевий, решта — блакитні
    node_colors = ['#FF8C00' if n == start else '#AED6F1' for n in G.nodes()]

    # Малюємо всі ребра (сірі)
    normal_edges = [e for e in G.edges() if e not in shortest_edges]
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges,
                           edge_color='#AAAAAA', arrows=True,
                           arrowsize=15, width=1.2)

    # Малюємо ребра найкоротших шляхів (зелені, товстіші)
    nx.draw_networkx_edges(G, pos, edgelist=list(shortest_edges),
                           edge_color='#27AE60', arrows=True,
                           arrowsize=18, width=2.5)

    # Вузли
    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                           node_size=800)

    # Мітки вузлів + відстань
    labels = {n: f"{n}\n({distances[n]})" for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=9)

    # Ваги ребер
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title(f"Алгоритм Дейкстри  |  початкова вершина: «{start}»\n"
              f"Зелені ребра — найкоротші шляхи", fontsize=12)
    plt.axis('off')
    plt.tight_layout()

    out_path = "task3_dijkstra.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Збережено: {out_path}")


# ── Демонстрація ──────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Завдання 3: Алгоритм Дейкстри")
    print("=" * 50)

    # Зважений орієнтований граф (словник суміжності)
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 5), ('D', 10)],
        'C': [('E', 3)],
        'D': [('F', 11)],
        'E': [('D', 4), ('F', 7)],
        'F': [],
    }

    start = 'A'
    distances, predecessors = dijkstra(graph, start)

    print(f"\nНайкоротші відстані від вершини «{start}»:")
    for node, dist in distances.items():
        path = get_path(predecessors, start, node)
        path_str = " -> ".join(path) if path else "недосяжна"
        print(f"  до {node}: {dist:>5}   шлях: {path_str}")

    visualize(graph, distances, predecessors, start)


if __name__ == "__main__":
    main()