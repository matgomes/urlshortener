import requests
import json

# Dez links mais acessados
r = requests.get('http://localhost:8000/api/top_entry/')
print(r.json())


print('==='*30)

# Chamada sem custom alias
data = {'original':'http://bemobi.com.br'}
r = requests.put('http://localhost:8000/api/create/', data=json.dumps(data))
print(r.json())

print('==='*30)

# Chamada com custom alias
data = {'original':'http://bemobi.com', 'alias':'bemobi'}
r = requests.put('http://localhost:8000/api/create/', data=json.dumps(data))
print(r.json())

print('==='*30)

# Chamada com custom alias que já existe
data = {'original':'http://bemobi.com', 'alias':'bemobi'}
r = requests.put('http://localhost:8000/api/create/', data=json.dumps(data))
print(r.json())

print('==='*30)

# Redirecionando a uma página
r = requests.get('http://localhost:8000/u/bemobi')
print(r)
#print(r.text)
