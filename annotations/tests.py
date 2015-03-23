from django.test import TestCase
from django.core.urlresolvers import resolve
#from annotations.views import home

from annotations.models import Annotation, AnnotationShareMap

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.http.request import HttpRequest

from unittest import skip
#from django.http import request

from blogging.models import BlogContent

import json

from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient

# Create your tests here.
class TestAnnotations(TestCase):
    
    fixtures = ['fixtures.json',]
    
    def setUp(self):
        self.user = User.objects.get(username="craft")
        token = Token.objects.create(user=self.user)
        token.save()
        self.factory = APIRequestFactory()
        self.client = APIClient()
        
    def tearDown(self):
        pass
    
    def create_annotation(self, body='', paragraph=None):
        annotation = Annotation()
        annotation.content_type=ContentType.objects.get(model='blogcontent', app_label="blogging")
        annotation.object_id= str(1)
        annotation.body=body
        annotation.paragraph=paragraph
        annotation.author= User.objects.get(id=1)
                
        annotation.save()
    
    def _require_login(self):
        self.client.login(username='craft', password='craft')

class TestBasicAnnotations(TestAnnotations):
    
    @skip("Not required in DRF")    
    def test_can_resolve_app_url(self):
        obj = resolve('/annotations/')
        self.assertEqual(obj.func, home)
        
    def test_create_annotation(self):
        self.create_annotation(body='This is a test annotation', paragraph=1)
    
    def test_empty_annotation_is_disallowed(self):
        pass
        
    @skip("Not used with DRF")    
    def test_POST_annotation(self):
        #use test client to POST a request
        string_data = {
                    'content_type': '9',
                    'object_id':'1',
                    'paragraph':'1',
                    'body':'Dreaming is good, day dreaming, not so good.',
                    'author':str(self.user.id),
                    'privacy':'3',
                    'privacy_override': '0',
                    'shared_with': ['1'],
                    }
        json_data = json.dumps(string_data)
        response = self.client.post(
            '/annotations/',
            content_type='application/json',
            data = json_data,
         )
        
        #the result must redirect to the same page but not reload the same page (for now)
        #self.assertRedirects(response, '/blogging/articles/i-have-a-dream-by-martin-luther-king/1/')
        
        #Expect a JSON object in response
        
        #Try to get all the annotations. Count should be 1, and it must be ours.
               
        self.assertEqual(Annotation.objects.all().count(), 1)
        annotation = Annotation.objects.all()[0]
        self.assertEqual(annotation.body, 'Dreaming is good, day dreaming, not so good.')
        self.assertEqual(annotation.paragraph, 1)
            
        #check if the redirected page is the same as previous one        
        #the response MUST contain the annotation we just posted
    @skip("Not used with DRF")     
    def test_retrieve_annotations_for_post(self):
        #use test client to visit the page
        #create a few annotations first
        string_data = {
                    'content_type': '9',
                    'object_id':'1',
                    'paragraph':'1',
                    'body':'Dreaming is good, day dreaming, not so good.',
                    'author':str(self.user.id),
                    'privacy':'3',
                    'privacy_override': '0',
                    'shared_with': ['1'],
                    }
        json_data = json.dumps(string_data)
        response = self.client.post(
            '/annotations/',
            content_type='application/json',
            data = json_data,
         )
        
        response = self.client.get('/annotations/?content_type=blogcontent&object_id=1')
        #get must return annotations in an HttpResponse object.
        self.assertContains(response, 'Dreaming is good, day dreaming, not so good.')
    
    def test_retrieve_annotations_for_current_user(self):
        
        pass
    
    def test_delete_annotation(self):
        pass
    
    def test_retrieve_public_annotations_by_user(self):
        pass
    
    def test_edit_annotation(self):
        pass
    
    def test_change_privacy_of_annotation(self):
        pass


from annotations.forms import AnnotationForm 
class TestForm(TestAnnotations):
    
    @skip("Skipping test")
    def test_form_instance(self):
        #Create an instance with form data
        form_instance = AnnotationForm()
        #print(str(form_instance))
        
        #Must have certain mandatory attributes
        
        #object_id
        self.assertTrue(hasattr(form_instance, 'object_id'))
        #content_type
        self.assertTrue(hasattr(form_instance, 'content_type'))
        #body
        self.assertTrue(hasattr(form_instance, 'body'))
        #author
        self.assertTrue(hasattr(form_instance, 'author'))
        

from annotations.serializers import AnnotationSerializer

from rest_framework.renderers import JSONRenderer 

class TestSerializers(TestAnnotations):
    
    def test_create_serializer_class(self):
        annotation = Annotation()
        annotation.content_type=ContentType.objects.get(model='blogcontent', app_label="blogging")
        annotation.object_id= str(1)
        annotation.body="This is a test annotation"
        annotation.paragraph="1"
        annotation.author= User.objects.get(id=1)
                
        annotation.save()
        obj = AnnotationSerializer(annotation)
        #print(obj.data)
        
        json = JSONRenderer().render(obj.data)
        #print json
        
    @skip('skipping')
    #This is just for exploratory purpose
    def test_create_serializer_instance(self):
        obj = AnnotationSerializer()
        print(obj)
    
    def test_view_annotations(self):
        self.create_annotation(body='This is a test annotation 1', paragraph=1)
        response = self.client.get('/annotations/annotations/')
        #print 'response'
        #print response.content.decode()
    
    def _create_annotation(self, content=None):
        #use test client to POST a request
        self._require_login()
        print(self.user.is_authenticated()) # returns True
        string_data = {
                    'content_type': content['content_type'],
                    'object_id':content['object_id'],
                    'paragraph':content['paragraph'],
                    'body': content['body'],
                    #'author':content['author'],
                    'privacy':content['privacy'],
                    'privacy_override': content['privacy_override'],
                    'shared_with': content['shared_with'],
                    }
        json_data = json.dumps(string_data)
        return self.client.post(
            '/annotations/annotations/',
            content_type='application/json',
            data = json_data,
         )
        
    def test_POST_annotation(self):
        response = self._create_annotation(content={
                    'content_type': '9',
                    'object_id':'1',
                    'paragraph':'1',
                    'body':'Dreaming is good, day dreaming, not so good.',
                    'author':str(self.user.id),
                    'privacy':'3',
                    'privacy_override': '0',
                    'shared_with': ['1'],
                    })
        
        #the result must redirect to the same page but not reload the same page (for now)
        #self.assertRedirects(response, '/blogging/articles/i-have-a-dream-by-martin-luther-king/1/')
        
        #Expect a JSON object in response
        
        #Try to get all the annotations. Count should be 1, and it must be ours.
        print "Response"
        print response.content.decode()       
        self.assertEqual(Annotation.objects.all().count(), 1)
        annotation = Annotation.objects.all()[0]
        #print 'Annotation content_object'
        #print annotation.content_object
        self.assertEqual(annotation.body, 'Dreaming is good, day dreaming, not so good.')
        self.assertEqual(annotation.paragraph, 1)
        
        map = AnnotationShareMap.objects.all()
        for share in map:
            print str(share)
        #check if the redirected page is the same as previous one        
        #the response MUST contain the annotation we just posted

    def test_PUT_annotation(self):
        self._create_annotation(content={
                    'content_type': '9',
                    'object_id':'1',
                    'paragraph':'1',
                    'body':'Dreaming is good, day dreaming, not so good.',
                    'author':str(self.user.id),
                    'privacy':'3',
                    'privacy_override': '0',
                    'shared_with': ['1'],
                    })
        #Update the annotation    
        annotation = Annotation.objects.all()[0]
        string_data = {
                    'content_type': '9',
                    'object_id':'1',
                    'paragraph':'1',
                    'body':'This is the updated annotation',
                    'author':str(self.user.id),
                    'privacy':'3',
                    'privacy_override': '0',
                    'shared_with': ['1'],
                    }
        json_data = json.dumps(string_data)
        url = '/annotations/annotations/'+ str(annotation.id)+'/'
        response = self.client.put(
            url,
            content_type='application/json',
            data = json_data,
         )
        
        print "Response"
        print response.content.decode()       
        self.assertEqual(Annotation.objects.all().count(), 1)
        annotation = Annotation.objects.all()[0]
        #print 'Annotation content_object'
        #print annotation.content_object

        self.assertEqual(annotation.body, 'This is the updated annotation')
        self.assertEqual(annotation.paragraph, 1)
    
    def test_DELETE_annotation(self):
        self._create_annotation(content={
                    'content_type': '9',
                    'object_id':'1',
                    'paragraph':'1',
                    'body':'Dreaming is good, day dreaming, not so good.',
                    'author':str(self.user.id),
                    'privacy':'3',
                    'privacy_override': '0',
                    'shared_with': ['1'],
                    })
        annotation = Annotation.objects.all()[0]
        url = '/annotations/annotations/'+ str(annotation.id)+'/'
        response = self.client.delete(url, content_type='application/json', data={})
        #print "Response"
        #print response.content.decode()       
        self.assertEqual(Annotation.objects.all().count(), 0)
 
 
    
#This test demonstates gow to login in testCases 
#http://stackoverflow.com/questions/20528798/testing-authentication-in-django-rest-framework-views-cannot-authenticate-whe



"""
class TestAPIViews(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', email='testuser@test.com', password='testing')
        self.user.save()
        token = Token.objects.create(user=self.user)
        token.save()

    def _require_login(self):
        self.client.login(username='testuser', password='testing')

    def test_ListAccounts_not_authenticated(self):
        request = self.factory.get('/accounts/')
        view = views.ListAccounts.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 401,
            'Expected Response Code 401, received {0} instead.'.format(response.status_code))

    def test_ListAccounts_authenticated(self):
        self.client._require_login()
        print(self.user.is_authenticated()) # returns True
        request = self.factory.get('/accounts/')
        view = views.ListAccounts.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200,
            'Expected Response Code 200, received {0} instead.'.format(response.status_code))    
"""            