from django.db import models


# Modelo base para os campos indicando momento da criação e modificação de um objeto
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Tabela para armazenar todas as ordens de monitoramento do usuário
class TrackOrder(BaseModel):
    requester_email = models.EmailField(max_length=255) # email de quem iniciou o monitoramento
    ticker_code = models.CharField(max_length=20) # codigo do ativo monitorado
    task_id = models.CharField(max_length=255, unique=True) # id da task no celery
    buy_limit = models.DecimalField(max_digits=10, decimal_places=2) # limite inferior do tunel (limiar de compra)
    sell_limit = models.DecimalField(max_digits=10, decimal_places=2) # limite superior do tunel (limiar de venda)
    frequency = models.DecimalField(max_digits=3, decimal_places=2) # frequencia em minutos
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.task_id


# Tabela para armazenar a cotação atual de um certo ativo que está sendo monitorado
class OrderQuote(BaseModel):
    track_order = models.ForeignKey(TrackOrder, on_delete=models.PROTECT)
    quote_price = models.DecimalField(max_digits=10, decimal_places=2) # Preço do ativo no momento da busca
    
    def __str__(self):
        return f'{self.id} - {self.track_order}'