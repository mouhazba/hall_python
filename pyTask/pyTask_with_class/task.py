class Task:
    def __init__(self):
        self.list_task = []


    def create_task(self):
        """create and append a task"""
        name_task = input("task: ")
        dic_task = {
            "name" : name_task,
            "status" : False,
        }
        self.list_task.append(dic_task)
        print(f"{name_task} is added")

    def complete_task(self):
        """complete a status of a task"""
        task_name = input("task: ")
        if self.list_task:
            for task in self.list_task:
                if task_name in task["name"]:
                    task['status'] = True
                    print(f"{task} is completed")
                    return
            else:
                print(f"{task_name} not found in : {self.list_task}")
        else:
            print("List empty")

    def display_all_tasks(self):
        """display all task"""
        if self.list_task:
            for task in self.list_task:
                print(task)
        else:
            print("Tasks empty")
    
    def delete_task(self):
        """delete a task by his name"""
        if self.list_task:
            task_name = input("task: ")
            for task in self.list_task:
                if task["name"] == task_name:
                    self.list_task.remove(task)
                    print("f{task_name} is deleted")
                    return
            print("f{task_name} is not found")
        else:
            print("Tasks empty")