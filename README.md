1. start server
docker-compose up 
-> you can see api in localhost:8000,
you can see admin page in localhost:8000/admin using root/root

2. create application
docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && python manage.py startapp users"
->you can see users folder in api

3. add application to project
api/api/settings.py inst apps "users"

4. create model

5. migrate to db
 docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && python manage.py makemigrations"
 docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && python manage.py migrate"

 6. you can create user in admin page

 7. create thread app