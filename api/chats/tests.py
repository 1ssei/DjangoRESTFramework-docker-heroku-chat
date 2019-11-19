from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from chats.models import Thread, ThreadMember
from django.test import Client
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
import json


class ThreadTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(
            username='user1',
            password='user1',
            email='1@isseisuzuki.com',
        )
        self.user2 = User.objects.create_superuser(
            username='user2',
            password='user2',
            email='2@isseisuzuki.com',
        )
        self.user3 = User.objects.create_superuser(
            username='user3',
            password='user3',
            email='3@isseisuzuki.com',
        )
        self.c1 = Client()
        self.c1.login(username='user1', password='user1')
        self.c2 = Client()
        self.c2.login(username='user2', password='user2')
        self.c3 = Client()
        self.c3.login(username='user3', password='user3')
        self.c4 = Client()
        self.post_data = {
            'title': 'test',
            'owner': 1,
            'is_public': True}

    # CREATE test
    def test_user_can_create(self):
        response = self.c1.post("/v1/threads/", self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.count(), 1)

    def test_user1_cannot_create_user2_data(self):
        with self.assertRaises(PermissionDenied):
            self.c1.post("/v1/threads/",
                         {'title': 'test',
                          'owner': 2,
                          'is_public': True})
        self.assertEquals(Thread.objects.count(), 0)

    def test_nologin_user_cannot_create(self):
        response = self.c4.post("/v1/threads/", self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_create_too_long_title(self):
        response = self.c1.post("/v1/threads/",
                                {'title': 'a'*201,
                                 'owner': 1,
                                 'is_public': True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Thread.objects.count(), 0)

    # READ TEST
    def test_user_can_read(self):
        self.c1.post("/v1/threads/", self.post_data)
        response = self.c1.get("/v1/threads/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 1)

    def test_user_cannot_retrieve(self):
        self.c1.post("/v1/threads/", self.post_data)
        with self.assertRaises(MethodNotAllowed):
            self.c1.get("/v1/threads/1/")

    def test_user_cannot_read_private_thread(self):
        self.c1.post("/v1/threads/",
                     {'title': 'test',
                      'owner': 1,
                      'is_public': False})
        response = self.c1.get("/v1/threads/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 0)

    # UPDATE test
    def test_owner_can_update(self):
        self.c1.post("/v1/threads/", self.post_data)
        self.c1.patch('/v1/threads/1/',
                      json.dumps({"title": "updated title"}),
                      content_type='application/json')
        thread = Thread.objects.get(id=1)
        self.assertEquals(thread.title, 'updated title')

    def test_user_cannot_update(self):
        self.c1.post("/v1/threads/", self.post_data)
        with self.assertRaises(PermissionDenied):
            self.c2.patch('/v1/threads/1/',
                          json.dumps({"title": "updated title"}),
                          content_type='application/json')
        thread = Thread.objects.get(id=1)
        self.assertEquals(thread.title, self.post_data['title'])

    # DELETE test
    def test_owner_can_delete(self):
        self.c1.post("/v1/threads/", self.post_data)
        response = self.c1.delete("/v1/threads/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Thread.objects.count(), 0)

    def test_user_cannot_delete(self):
        self.c1.post("/v1/threads/", self.post_data)
        with self.assertRaises(PermissionDenied):
            self.c2.delete("/v1/threads/1/")
        self.assertEquals(Thread.objects.count(), 1)


class ThreadMemberTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(
            username='user1',
            password='user1',
            email='1@isseisuzuki.com',
        )
        self.user2 = User.objects.create_superuser(
            username='user2',
            password='user2',
            email='2@isseisuzuki.com',
        )
        self.user3 = User.objects.create_superuser(
            username='user3',
            password='user3',
            email='3@isseisuzuki.com',
        )
        self.c1 = Client()
        self.c1.login(username='user1', password='user1')
        self.c2 = Client()
        self.c2.login(username='user2', password='user2')
        self.c3 = Client()
        self.c3.login(username='user3', password='user3')
        self.c4 = Client()
        Thread(title='test', owner_id=1, is_public=False).save()
        ThreadMember(thread_id=1, user_id=1).save()

    def test_thread_owner_data_created_after_thread_made(self):
        self.assertEqual(ThreadMember.objects.count(), 1)
        post_data = {
            'title': 'test',
            'owner': 1,
            'is_public': True}
        self.c1.post("/v1/threads/", post_data)
        self.assertEqual(ThreadMember.objects.count(), 2)

    # CREATE test
    def test_owner_can_create(self):
        response = self.c1.post("/v1/thread_members/",
                                {'thread': 1, 'user': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ThreadMember.objects.count(), 2)

    def test_user_cannot_create(self):
        with self.assertRaises(PermissionDenied):
            self.c2.post("/v1/thread_members/",
                         {'thread': 1, 'user': 2})
        self.assertEquals(ThreadMember.objects.count(), 1)

    def test_owner_cannot_create_same_data(self):
        self.c1.post("/v1/thread_members/",
                     {'thread': 1, 'user': 2})
        with self.assertRaises(PermissionDenied):
            self.c1.post("/v1/thread_members/",
                         {'thread': 1, 'user': 2})
        self.assertEqual(ThreadMember.objects.count(), 2)

    # READ TEST
    def test_user_cannot_read_list(self):
        self.c1.post("/v1/thread_members/",
                     {'thread': 1, 'user': 2})
        with self.assertRaises(PermissionDenied):
            self.c1.get("/v1/thread_members/")

    def test_user_can_read_public_thread(self):
        post_data = {
            'title': 'test',
            'owner': 1,
            'is_public': True}
        self.c1.post("/v1/threads/", post_data)
        response = self.c2.get("/v1/thread_members/?thread=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 1)

    def test_user_can_read_private_thread(self):
        self.c1.post("/v1/thread_members/",
                     {'thread': 1, 'user': 2})
        response = self.c2.get("/v1/thread_members/?thread=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 2)

    def test_user_cannot_read_private_thread(self):
        post_data = {
            'title': 'test',
            'owner': 2,
            'is_public': False}
        self.c2.post("/v1/threads/", post_data)
        with self.assertRaises(PermissionDenied):
            self.c1.get("/v1/thread_members/?thread=2")

    def test_nologin_user_cannot_read_thread(self):
        response = self.c4.get("/v1/thread_members/?thread=1")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE test
    def test_owner_can_delete(self):
        self.c1.post("/v1/thread_members/",
                     {'thread': 1, 'user': 2})
        response = self.c1.delete("/v1/thread_members/2/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(ThreadMember.objects.count(), 1)

    def test_user_cannot_delete(self):
        self.c1.post("/v1/thread_members/",
                     {'thread': 1, 'user': 2})
        with self.assertRaises(PermissionDenied):
            self.c2.delete("/v1/thread_members/2/")
        self.assertEquals(ThreadMember.objects.count(), 2)

    def test_owner_cannot_delete_owner_data(self):
        with self.assertRaises(PermissionDenied):
            self.c1.delete("/v1/thread_members/1/")
        self.assertEquals(ThreadMember.objects.count(), 1)
