from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
        Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

        Args:
            print_jobs: Список завдань на друк
            constraints: Обмеження принтера

        Returns:
            Dict з порядком друку та загальним часом
        """
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Сортування: спочатку за пріоритетом (від 1 до 3), потім за часом друку (від більшого)
    jobs.sort(key=lambda job: (job.priority, -job.print_time))

    print_order = []
    total_time = 0

    i = 0
    while i < len(jobs):
        group = []
        group_volume = 0.0

        j = i
        while j < len(jobs) and len(group) < printer.max_items and group_volume + jobs[j].volume <= printer.max_volume:
            group.append(jobs[j])
            group_volume += jobs[j].volume
            j += 1

        if not group:
            # якщо жодну модель не вдалося додати через обмеження — пропускаємо одну
            group.append(jobs[i])
            group_volume = jobs[i].volume
            j = i + 1

        # Час друку групи — макс. серед її елементів
        group_time = max(job.print_time for job in group)
        total_time += group_time
        print_order.extend(job.id for job in group)

        # Перейти до наступної групи
        i += len(group)

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("\nТест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
