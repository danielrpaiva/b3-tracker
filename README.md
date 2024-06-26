# b3-tracker #

## Setup Inicial ##

Requer docker e docker-compose instalados!

Renomear o .example.env para .env e setar os valores corretos das seguintes variaveis: 
BRAPI_TOKEN - Token da api do Brapi
EMAIL_HOST_USER - Email de remetente do disparo de aviso de venda ou compra de ativo
EMAIL_HOST_PASSWORD - Senha do email de remetente

OBS: Necessita de um token para a acessar a api do brapi de onde as informações do mercado financeiro são puxadas, pode ser obtido gratuitamente no link: 
* https://brapi.dev/dashboard

### Rodar os seguintes comandos: ###
```
sudo docker-compose up --build -d
sudo docker-compose exec web python manage.py migrate --noinput
sudo docker-compose exec web python manage.py collectstatic --no-input --clear
```

### Verificar se os containers iniciados estão rodando corretamente ###
sudo docker ps