from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .tasks import track_b3
from .models import TrackOrder
from .serializers import TrackOrderBasicSerializer
from celery import current_app

import logging

# Create your views here.
class TrackerView(APIView):
    """
    POST:
    Inicia o monitoramento dos ativos passados no payload
    Payload:
    {
        "email": "requester-email@gmail.com"
        "orders":[
            {
                "ticker_code": "PETR3",
                "buy_limit": 30,
                "sell_limit": 40,
                "frequency": 5,
            },
            ...
        ]
    }

    PUT:
    Interrompe o monitoramento associado a task do id passado
    """
    def post(self, request):
        try:
            payload = request.data
            email = payload["email"]
            
            created_tasks = list()

            for order in payload["orders"]:
                task = track_b3.apply_async(args=[order, email])
                created_tasks.append(task.id)

            track_orders = TrackOrder.objects.filter(task_id=created_tasks)

            return Response(TrackOrderBasicSerializer(instance=track_orders, many=True).data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logging.exception(str(e))
            return Response({"message": f"Ocorreu um erro inesperado durante a criação das tasks"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, task_id):
        
        try:
            curr_order = TrackOrder.objects.get(task_id=task_id)
            
            current_app.control.revoke(task_id, terminate=True)

            curr_order.is_active = False
            curr_order.save()

            return Response({"message": "Monitoramento interrompido!", "task_id": task_id}, status=status.HTTP_200_OK)
        
        except TrackOrder.DoesNotExist as e:
            return Response({"message": f"TrackOrder não encontrado com o task_id: {task_id}"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logging.exception(str(e))
            return Response({"message": f"Ocorreu um erro inesperado durante a interrupção do monitoramento"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TODO: View para listar os preços armazenados dos ativos
# TODO: View para listar todos os ativos da B3 para o usuario escolher quais ele quer monitorar

class TestView(APIView):
    def get(self, request):
        return Response({"msg": "api ok!"})