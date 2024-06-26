import time
import logging
import math

from datetime import datetime
from celery import shared_task
from .models import OrderQuote
from .serializers import TrackOrderBasicSerializer
from .api_connections.brapi_connector import BrapiApi

# TODO: Iniciar o worker quando iniciar o servidor django! Usar docker? supervisor?

@shared_task(bind=True)
def track_b3(self, order, email):
    
    try:
        brapi_api = BrapiApi()

        frequency_in_seconds = math.floor(order["frequency"] * 60)

        order["requester_email"] = email
        order["task_id"] = self.request.id

        order_write = TrackOrderBasicSerializer(data=order)
        order_write.is_valid(raise_exception=True)
        saved_order = order_write.save()

        iteration_count = 1

        while True:
            logging.info(f"Começando iteração {iteration_count} task: {self.request.id}")

            quote_resp = brapi_api.ticker_quote(saved_order.ticker_code)

            curr_price = quote_resp["results"][0]["regularMarketPrice"]

            curr_quote = OrderQuote(
                track_order=saved_order,
                quote_price=curr_price,
            )

            curr_quote.save()

            if curr_price < saved_order.buy_limit:
                pass # TODO: Disparar email

            if curr_price > saved_order.sell_limit:
                pass # TODO: Disparar email

            iteration_count += 1

            time.sleep(frequency_in_seconds)
    
    except Exception as e:
        logging.exception("Task finalizada, ocorreu um erro!")
        return "Task finalizada"