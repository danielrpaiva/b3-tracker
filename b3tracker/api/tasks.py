from datetime import datetime
from celery import shared_task
import time

@shared_task(bind=True)
def task_exemplo(self, number):
    
    try:
        while True:
            print(f'São {datetime.now()}')
            print(f'Número recebido foi {number}')
            time.sleep(5)
    
    except Exception as e:
        print(f'Task {self.request.id} terminated: {e}')
        return 'Task terminated'