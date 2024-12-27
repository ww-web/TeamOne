import base
import uuid
from app01 import models

def run():
    exists = models.Price.objects.filter(category=1).exists()
    if not exists:
        models.Price.objects.create(
            category=1,
            price=0,
            projects_num=3,
            projects_member=2,
            project_space=20,
            create_datatime=5
        )


if __name__ == '__main__':
    run()