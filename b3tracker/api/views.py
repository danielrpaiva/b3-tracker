from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .tasks import track_b3
from .models import TrackOrder, OrderQuote
from .serializers import TrackOrderBasicSerializer, OrderQuoteListSerializer
from .api_connections.brapi_connector import BrapiApi
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

    GET:
    Busca as cotações armazenadas
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

    def get(self, request):

        try:
            email_param = request.GET.get("email")
            ticker_param = request.GET.get("ticker")
            task_id_param = request.GET.get("task")
            min_price_param = request.GET.get("min_price")
            max_price_param = request.GET.get("max_price")

            curr_order_quotes = OrderQuote.objects.all()

            if email_param:
                curr_order_quotes = curr_order_quotes.filter(track_order__requester_email=email_param)
            
            if ticker_param:
                curr_order_quotes = curr_order_quotes.filter(track_order__ticker_code=ticker_param)
            
            if task_id_param:
                curr_order_quotes = curr_order_quotes.filter(track_order__task_id=task_id_param)

            if min_price_param:
                curr_order_quotes = curr_order_quotes.filter(quote_price__gte=min_price_param)

            if max_price_param:
                curr_order_quotes = curr_order_quotes.filter(quote_price__lte=max_price_param)
            
            resp_data = {
                "quotes": OrderQuoteListSerializer(instance=curr_order_quotes, many=True).data
            }

            return Response(resp_data, status=status.HTTP_200_OK)

        except Exception as e:
            logging.exception(str(e))
            return Response({"message": f"Ocorreu um erro inesperado durante a listagem de preços"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TickerView(APIView):

    def get(self, request):

        try:
            ticker_param = request.GET.get("search", None)

            params = dict()

            if ticker_param:
                params["search"] = ticker_param

            brapi_api = BrapiApi()
            tickers_resp = brapi_api.list_tickers(params)

            all_tickers = sorted(tickers_resp["indexes"] + tickers_resp["stocks"])

            return Response(all_tickers, status=status.HTTP_200_OK)
        
        except Exception as e:
            logging.exception(str(e))
            return Response({"message": f"Ocorreu um erro inesperado "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# TODO: Colocar o tratamento de erro generico num middleware?
          

class TaskDebugView(APIView):
    def get(self, request):
        
        tasks_list = current_app.control.inspect()

        resp = {
            "scheduled": tasks_list.scheduled(),
            "active": tasks_list.active(),
            "reserved": tasks_list.reserved(),
        }

        return Response(resp)