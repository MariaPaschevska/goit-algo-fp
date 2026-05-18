"""
Завдання 1: Робота з однозв'язним списком
- Реверсування списку
- Сортування (злиттям)
- Об'єднання двох відсортованих списків
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # ── допоміжні методи ──────────────────────────────────────────────────────

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def __str__(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements) + " -> None"

    # ── Завдання 1а: реверсування ─────────────────────────────────────────────

    def reverse(self):
        """
        Реверсує однозв'язний список, змінюючи посилання між вузлами.
        Складність: O(n) за часом, O(1) за пам'яттю.
        """
        prev = None
        current = self.head
        while current:
            next_node = current.next   # зберігаємо наступний
            current.next = prev        # розвертаємо посилання
            prev = current             # рухаємо prev вперед
            current = next_node        # рухаємо current вперед
        self.head = prev

    # ── Завдання 1б: сортування злиттям ───────────────────────────────────────

    def sort(self):
        """
        Сортує список методом злиття (merge sort).
        Складність: O(n log n) за часом, O(log n) за пам'яттю (стек рекурсії).
        """
        self.head = self._merge_sort(self.head)

    def _merge_sort(self, head):
        # База рекурсії: 0 або 1 елемент — вже відсортовано
        if not head or not head.next:
            return head

        # Знаходимо середину списку (алгоритм «черепаха і заєць»)
        mid = self._get_middle(head)
        right_head = mid.next
        mid.next = None  # розрізаємо список навпіл

        # Рекурсивно сортуємо кожну половину
        left = self._merge_sort(head)
        right = self._merge_sort(right_head)

        # Зливаємо відсортовані половини
        return self._merge(left, right)

    def _get_middle(self, head):
        """Повертає середній вузол (slow/fast pointer)."""
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def _merge(self, left, right):
        """Зливає два відсортованих вузлові ланцюжки в один."""
        dummy = Node(0)
        current = dummy
        while left and right:
            if left.data <= right.data:
                current.next = left
                left = left.next
            else:
                current.next = right
                right = right.next
            current = current.next
        current.next = left if left else right
        return dummy.next

    # ── Завдання 1в: об'єднання двох відсортованих списків ────────────────────


def merge_sorted_lists(list1: LinkedList, list2: LinkedList) -> LinkedList:
    """
    Об'єднує два відсортованих однозв'язних списки в один відсортований список.
    Складність: O(n + m), де n і m — довжини списків.
    """
    merged = LinkedList()
    merged.head = _merge_nodes(list1.head, list2.head)
    return merged


def _merge_nodes(a: Node, b: Node) -> Node:
    """Ітеративно зливає два відсортованих ланцюжки вузлів."""
    dummy = Node(0)
    current = dummy
    while a and b:
        if a.data <= b.data:
            current.next = a
            a = a.next
        else:
            current.next = b
            b = b.next
        current = current.next
    current.next = a if a else b
    return dummy.next


# ── Демонстрація ───────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Завдання 1: Однозв'язний список")
    print("=" * 50)

    # 1а — реверсування
    print("\n--- 1а. Реверсування ---")
    ll = LinkedList()
    for v in [1, 2, 3, 4, 5]:
        ll.append(v)
    print(f"До:    {ll}")
    ll.reverse()
    print(f"Після: {ll}")

    # 1б — сортування
    print("\n--- 1б. Сортування злиттям ---")
    ll2 = LinkedList()
    for v in [3, 1, 4, 1, 5, 9, 2, 6]:
        ll2.append(v)
    print(f"До:    {ll2}")
    ll2.sort()
    print(f"Після: {ll2}")

    # 1в — об'єднання двох відсортованих списків
    print("\n--- 1в. Об'єднання двох відсортованих списків ---")
    la = LinkedList()
    for v in [1, 3, 5, 7]:
        la.append(v)

    lb = LinkedList()
    for v in [2, 4, 6, 8]:
        lb.append(v)

    print(f"Список A: {la}")
    print(f"Список B: {lb}")
    merged = merge_sorted_lists(la, lb)
    print(f"Злитий:   {merged}")


if __name__ == "__main__":
    main()