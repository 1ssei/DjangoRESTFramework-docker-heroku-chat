0. 
create er
create api list
start developing and testing
upload to heroku
developing front
binding
developing
upload to aws

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

8. create permission -> common file

9. too simple , paging filter
add django-filter to requirements
docker-compose build
docker-compose up
https://www.django-rest-framework.org/api-guide/settings/

9. create unit test
docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && python manage.py test chats.tests.ThreadTests.test_user_cannot_create_too_long_title"

get_queryset
is_public false の問題が残ったのでfail するtest を作っておく


10. create threadmember model

11. serializer add user serializer
userはidではなくUsername も出すとかはuserserializer側でやった方が今後も使う

12. view and url
CRUDそれぞれについて考えてみる。
まず、createはownerだけができる必要がある。
重複はなしにしとくかなあ
readはthreadmember（もちろんownerも） はみることができる
Updateは別にいらないか
Deleteはownerだけ

viewsets.ModelViewSet だとCRUD全てを実装してしまう
permissionでraise error してもいいけどmixinで必要なviewだけ選ぶ方がおすすめ
DRFの画面でも出てこなくなるし抜け道なくなりやすいから安全
ちなみにstatus codeはHTTP_405_METHOD_NOT_ALLOWED

具体的には以下から必要なものを親にする（一番下は必須！）

mixins.ListModelMixin,
mixins.CreateModelMixin,
mixins.RetrieveModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,
viewsets.GenericViewSet

今回は以下を採用
GET系は今回はいらないかなあ　画面表示用で扱うかなあとも思うけど
強いていうならmemberが多い時に問題にはなるのでLISTは実装するか
こういうのは仕様、画面に依存する
memberの一覧を出すのかfacebook,insta見たいにpopupとかで無限スクロールするか
mixins.ListModelMixin,
mixins.CreateModelMixin,
mixins.DestroyModelMixin,
viewsets.GenericViewSet

filter実装
django_filtersをinstall
simple だったので
https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
こちらで対応。commentでsearchかな　部分一致とか

permission
以下を実装する
create：ownerだけができる　ただし、重複はなしにしとくかなあ
read：threadmember（もちろんownerも） はみることができる
Update:実装なし
Delete：ownerだけ

OwnerPermissionは使えない　ownerというカラムを追加して無理やり統一してもいいけど
ここでは完全に0からやってみる
それと忘れそうだったけどownerは自分をmemberから外すことはできないも追加した方がいい
ownerの変更はしてもいいけどmemberから外すとややこしくなる
＋ownerはthread作ったタイミングでthreadmemberになる必要あり。
それはthreadのcreateのviewをいじる必要あり。

->perform_createをthread の方に追加
---- -> thread のtestにもtest_user_can_read_private_threadを追加 ----
thread のreadはいらないな

11. test

13. comment
検索に使われるのが左の方がいい？
TESTは以下の観点
ほぼowner permission だけど
自分が参加していないThreadにはComment不可も必要
全てのcommentをみるのはだめ
?thread=1 とかの時だけ　かつ、そのthreadに自分が参加していること
上記の　二つを実装する

仕様によってtestは変わる
例えば　自分のcommentを自分がthread から追い出された後に編集できるのかどうかとか
今回は面倒なのでしないけどその辺は結構細かくなりがち

結構同じコードを書くようになってきた
if (not thread.is_public) and \
                (not models.ThreadMember.objects.filter(
                    thread=thread, user_id=userId).exists()):
                raise PermissionDenied("you cannot see this data")
→
def has_permission(self, userId):
        return (self.is_public) or \
                (ThreadMember.objects.filter(
                    thread=self, user_id=userId).exists())

test ではsort とpagingも入れてみた
後PATCHでownerとthreadは変えたらだめも入れた
http://blog.qax.io/write-once-fields-with-django-rest-framework/
mixin 使ってもいいけど単純なpermissionでやっとく

14. page用のGET
自分のthread一覧
一番上のthreadのコメントを10個
そのthreadのmemberを表示

違うthreadをclickしたら commentとthread member のgetを投げる感じで

15. Vue.js 、Nuxt でbiningする


10. coverage
 docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && coverage run manage.py test chats"
 docker exec -it djangorestframework-docker-heroku-chat_web_1 /bin/bash -c "cd api && coverage html"

 .coveragerc file 作ってからもう一回実行

11. perofrmance
 silk install
 settings.py
 installed app & middleware
 migrate
 http://localhost:8000/silk/request

 しまった、public thread の場合には自分でjoinする機能が必要
 つまり、thread member のpermission,testで変更が必要
 やっぱ設計だいじ