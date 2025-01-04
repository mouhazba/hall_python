import time

#use fonction decorateurs
from decorators_func import timing_x, check_role_user

list_task = []

@timing_x
def create_task():
    name = input("Name of task : ")
    dic_task = {"name":name, "status":False}
    list_task.append(dic_task)
    print("task ajoute avec succes")

@timing_x
def task_complete():
    if list_task:
        task_name = input("Name of task to complete : ")
        for t in list_task:
            if (t.get("name")) == task_name:
                t['status'] = True
                print(f"{t} is completed !")
                return
        print("Not found")
    else:
        print("Empty")

@timing_x
def display_all_tasks():
    if list_task:
        for t in list_task:
            print(f"- {t}")
    else:
        print("Empty")

@check_role_user("autre")
def delete_task():
    if list_task:
        task_name = input("Name of task to delete : ")
        for t in list_task:
            if (t.get("name")) == task_name:
                list_task.remove(t)
                print(f"{t} is deleted !")
                return
        print("Not found")
    else:
        print("Empty")