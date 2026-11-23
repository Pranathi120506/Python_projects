import json
import os
from datetime import datetime, date

TASKS_FILE = "tasks.json"

# Available priority levels
PRIORITIES = ["High", "Medium", "Low"]


def load_tasks():
    """Load saved tasks when the application starts."""
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            print("Invalid task data. Starting with an empty list.")
            return []

        # Add default values for older tasks.
        for task in tasks:
            task.setdefault("done", False)
            task.setdefault("priority", "Medium")
            task.setdefault("due_date", "")

        return tasks

    except (json.JSONDecodeError, OSError):
        print("Could not read the task file. Starting with an empty list.")
        return []


def save_tasks(tasks):
    """Save all tasks so they are available next time."""
    try:
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        print("Error: Unable to save tasks.")


def is_overdue(task):
    """Check whether a pending task has passed its deadline."""
    if task["done"] or not task["due_date"]:
        return False

    try:
        deadline = date.fromisoformat(task["due_date"])
        return deadline < date.today()
    except ValueError:
        return False


def show_tasks(tasks):
    """Display tasks with their priority, deadline and status."""
    if not tasks:
        print("\nYour task list is empty.\n")
        return

    print("\n========== YOUR TASKS ==========")

    for index, task in enumerate(tasks, start=1):
        if task["done"]:
            status = "Completed"
        elif is_overdue(task):
            status = "Overdue"
        else:
            status = "Pending"

        deadline = task["due_date"] or "No deadline"

        print(f"\n{index}. {task['title']}")
        print(f"   Priority : {task['priority']}")
        print(f"   Deadline : {deadline}")
        print(f"   Status   : {status}")

    print("\n================================\n")


def add_task(tasks):
    """Create a task with priority and an optional deadline."""
    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    print("\nSelect priority:")
    for index, priority in enumerate(PRIORITIES, start=1):
        print(f"{index}. {priority}")

    choice = input("Choose priority (1-3): ").strip()

    if choice not in ["1", "2", "3"]:
        print("Invalid priority. Task was not added.")
        return

    priority = PRIORITIES[int(choice) - 1]

    # The deadline is optional and must use YYYY-MM-DD format.
    due_date = input(
        "Enter deadline (YYYY-MM-DD) or press Enter to skip: "
    ).strip()

    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Task was not added.")
            return

    task = {
        "title": title,
        "done": False,
        "priority": priority,
        "due_date": due_date
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f'\nTask "{title}" added successfully!')


def complete_task(tasks):
    """Mark a selected pending task as completed."""
    show_tasks(tasks)

    if not tasks:
        return

    try:
        num = int(input("Enter task number to complete: "))

        if 1 <= num <= len(tasks):
            if tasks[num - 1]["done"]:
                print("This task is already completed.")
                return

            tasks[num - 1]["done"] = True
            save_tasks(tasks)
            print("Task marked as completed!")

        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


def delete_task(tasks):
    """Remove a task from the list."""
    show_tasks(tasks)

    if not tasks:
        return

    try:
        num = int(input("Enter task number to delete: "))

        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks(tasks)
            print(f'Task "{removed["title"]}" deleted successfully!')

        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


def search_tasks(tasks):
    """Find tasks using a word from their title."""
    keyword = input("Enter task name to search: ").strip().lower()

    if not keyword:
        print("Please enter a search keyword.")
        return

    results = [
        task for task in tasks
        if keyword in task["title"].lower()
    ]

    if not results:
        print("No matching tasks found.")
        return

    print("\nSearch Results:")

    for task in results:
        status = "Completed" if task["done"] else "Pending"
        print(
            f"- {task['title']} | "
            f"Priority: {task['priority']} | "
            f"Status: {status}"
        )


def show_progress(tasks):
    """Display a summary of completed and pending tasks."""
    total = len(tasks)
    completed = sum(1 for task in tasks if task["done"])
    pending = total - completed
    overdue = sum(1 for task in tasks if is_overdue(task))

    percentage = (completed / total * 100) if total else 0

    print("\n========== TASK PROGRESS ==========")
    print(f"Total Tasks     : {total}")
    print(f"Completed Tasks : {completed}")
    print(f"Pending Tasks   : {pending}")
    print(f"Overdue Tasks   : {overdue}")
    print(f"Completion Rate : {percentage:.1f}%")
    print("===================================\n")


def main():
    """Run the TaskFlow application."""
    tasks = load_tasks()

    print("\n================================")
    print("       TASKFLOW MANAGER")
    print("================================")

    while True:
        print("\n1. View All Tasks")
        print("2. Add New Task")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. View Progress Report")
        print("7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            show_tasks(tasks)

        elif choice == "2":
            add_task(tasks)

        elif choice == "3":
            complete_task(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "5":
            search_tasks(tasks)

        elif choice == "6":
            show_progress(tasks)

        elif choice == "7":
            print("\nThank you for using TaskFlow!")
            break

        else:
            print("Invalid choice. Please select between 1 and 7.")


if __name__ == "__main__":
    main()
