0. user change
createsuperuser

1. start server
docker-compose up 
<!-- -> you can see api in localhost:8000,
you can see admin page in localhost:8000/admin using root/root -->


2. create application
docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && python manage.py startapp users"
->you can see users folder in api

3. add application to project
api/api/settings.py inst apps "users"
AUTH_USER_MODEL = 'users.User'
default user class change

4. create superuser

4. create model

5. migrate to db
 docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && python manage.py makemigrations"
 docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && python manage.py migrate"

 6. you can create user in admin page



2. create thread app
docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && python manage.py startapp chat"

3. add application to project
api/api/settings.py inst apps "chats"

4. create thread model

5. create serializer

6. create create view

7. add routing in chats.urls and api.urls
create urls.py in chats

7. CRUD is made

8. create permission, 

9. 





