## URLSHORTENER

A simple url shortener made with Django REST Framework, nginx, gunicorn and postgres.    
    
This was my very first project, it was a challenge for an internship program.    
Recently i revisited it and made some changes.  
Challenge source: https://github.com/bemobi/hire.me

## RUNNING

Only docker compose is needed to run the project    
https://github.com/docker/compose/releases/latest  

	docker-compose up

## API  

#### Shorten with generated alias    
	curl -X PUT 'http://localhost/shorten/github.com'  
  
#### Shorten with custom alias  
	curl -X PUT 'http://localhost/shorten/github.com?custom_alias=github'  

#### Retrieve URL  
	curl -X GET -i 'http://localhost/retrieve/github'  

#### 10 most accessed urls  
	curl -X GET 'http://localhost/most_accessed'  

#### Most accessed urls with limit  
	curl -X GET 'http://localhost/most_accessed?limit=2'