# URLSHORTENER

Encurtador de links usando django, sqlite e django-rest-framework.

# SETUP

#### Criando virtual environment

>$ conda create --name myenv

#### Ativando virtual environment
>$ activate myenv

#### Instalando requirements
>$ pip install -U -r requirements.txt

#### Migrations
>$ python manage.py migrate
>>$ python manage.py makemigrations
>>>$ python manage.py migrate

#### Superuser
>$ python manage.py createsuperuser

#### Runserver
>$ python manage.py runserver

# API

#### Chamada sem alias
>$ http put  http://127.0.0.1:8000/api/create/ original=http://bemobi.com

#### Chamada com custom alias
>$ http put  http://127.0.0.1:8000/api/create/ original=http://bemobi.com alias=bemobi

#### Retrieve URL
>$ http get http://127.0.0.1:8000/api/u/bemobi

#### Dez URLs mais acessadas
>$ http get http://127.0.0.1:8000/api/u/top_entry

#### Client interface
>$ http get http://127.0.0.1:8000

# Client
Foi criada uma interface simples utilizando html e a biblioteca bulma.io

# Diagrama de sequência
![enter image description here](https://i.imgur.com/jb1oEJi.png)



