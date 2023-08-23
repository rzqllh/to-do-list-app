import sqlite3

class Task:
    def __init__(self, id, task, completed):
        self.id = id
        self.task = task
        self.completed = completed

class ToDoList:
    def __init__(self, db_name):
        self.db_name = db_name

    def _execute_query(self, query, params=None):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute(query, params or ())
            conn.commit()
            return cursor

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        """
        self._execute_query(query)

    def add_task(self, task_description):
        query = "INSERT INTO tasks (task) VALUES (?)"
        self._execute_query(query, (task_description,))

    def remove_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        self._execute_query(query, (task_id,))

    def complete_task(self, task_id):
        query = "UPDATE tasks SET completed = 1 WHERE id = ?"
        self._execute_query(query, (task_id,))

    def get_tasks(self):
        query = "SELECT id, task, completed FROM tasks"
        cursor = self._execute_query(query)
        tasks = [Task(id, task, completed) for id, task, completed in cursor.fetchall()]
        return tasks

def main():
    db_name = "todo.db"
    todo_list = ToDoList(db_name)
    todo_list.create_table()

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Complete Task")
        print("4. Show Tasks")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            task_description = input("Enter the task: ")
            todo_list.add_task(task_description)
        elif choice == "2":
            task_id = int(input("Enter the ID of the task to remove: "))
            todo_list.remove_task(task_id)
        elif choice == "3":
            task_id = int(input("Enter the ID of the task to mark as completed: "))
            todo_list.complete_task(task_id)
        elif choice == "4":
            tasks = todo_list.get_tasks()
            print("To-Do List:")
            for task in tasks:
                status = "✔" if task.completed else " "
                print(f"{task.id}. [{status}] {task.task}")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()
