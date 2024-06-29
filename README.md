# b3-tracker #

## Setup Inicial ##

Requer docker e docker-compose instalados!

Renomear o .example.env para .env e setar os valores corretos das seguintes variaveis:
```
BRAPI_TOKEN - Token da api do Brapi
EMAIL_HOST_USER - Email de remetente do disparo de aviso de venda ou compra de ativo
EMAIL_HOST_PASSWORD - Senha do email de remetente
```

OBS: Necessita de um token para a acessar a api do brapi de onde as informações do mercado financeiro são puxadas, pode ser obtido gratuitamente no link: 
* https://brapi.dev/dashboard

OBS 2: Se o email escolhido como remetente (gmail) tem autenticação em dois fatores ativada, é necessário criar uma senha de app para esse email e setar a variável de ambiente EMAIL_HOST_PASSWORD com essa senha de app (sem espaços):
* https://myaccount.google.com/apppasswords

### Rodar os seguintes comandos: ###
```
sudo docker-compose up --build -d
sudo docker-compose exec web python manage.py migrate --noinput
sudo docker-compose exec web python manage.py collectstatic --no-input --clear
```

### Verificar se os containers iniciados estão rodando corretamente ###
```
sudo docker ps
```

### Acessar a interface ###

* http://localhost:8000/gui/