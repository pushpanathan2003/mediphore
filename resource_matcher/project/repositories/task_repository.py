from project.models import Task

# def create_task(data):
#     return Task.objects.create(**data)
def create_task(data):
    required_skills = data.pop("required_skill", [])  
    task = Task.objects.create(**data)                
    task.required_skill.set(required_skills)         
    return task


def get_task_by_id(task_id):
    try:
        return Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return None

def list_tasks_by_creator(user):
    return Task.objects.filter(project__created_by=user)

def list_all_tasks():
    return Task.objects.all()
