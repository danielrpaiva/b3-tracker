from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import task_exemplo
from celery import current_app
from .api_connections.brapi_connector import BrapiApi

# Create your views here.
class TrackerView(APIView):
    def post(self, request, number):
        
        # TODO: Adaptar esse endpoint para receber via payload uma lista de tickers de ativos da B3 para monitorar

        task = task_exemplo.apply_async(args=[number])

        return Response({'task_id': task.id}, status=200)
    
    def put(self, request, task_id):
        
        current_app.control.revoke(task_id, terminate=True)

        return Response({'message': 'Monitoramento interrompido!', 'task_id': task_id})
    

class TestView(APIView):
    def get(self, request):
        return Response({"msg": "api ok!"})