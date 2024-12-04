from task import Task


a = """
1. Ajouter une tâche"
2. Marquer une tâche comme terminée
3. Lister toutes les tâches"
4. Supprimer une tâche (admin seulement)"""


task = Task()

response = input(f"Quel est votre choix : {a} \n => ")
while response != "0":
    if response == "1":
        task.create_task()

    if response == "2":
        task.complete_task()
    
    if response == "3":
        task.display_all_tasks()

    if response == "4":
        task.delete_task()

    print("*****" * 10)
    response = input(f"Quel est votre choix : {a} \n => ")