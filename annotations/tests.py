from django.test import TestCase
from django.core.urlresolvers import resolve
from annotations.views import home

from annotations.models import Annotation

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.http.request import HttpRequest

from unittest import skip
#from django.http import request

from blogging.models import BlogContent
# Create your tests here.
class TestAnnotations(TestCase):
    
    fixtures = ['fixtures.json',]
    
    def setUp(self):
        self.user = User.objects.get(username="craft")
        
    def tearDown(self):
        pass
    
    def test_can_resolve_app_url(self):
        obj = resolve('/annotations/')
        self.assertEqual(obj.func, home)
        
    def test_create_annotation(self):
        annotation = Annotation()
        annotation.content_type=ContentType.objects.get(model='blogcontent', app_label="blogging")
        annotation.object_id= str(1)
        annotation.body="This is a test annotation"
        annotation.paragraph="1"
        annotation.author= User.objects.get(id=1)
                
        annotation.save()
        
    def test_POST_annotation(self):
        #use test client to POST a request
        response = self.client.post(
            '/annotations/',
            data = {
                    'content_type': '9',
                    'object_id':'1',
                    'paragraph':'1',
                    'body':'Dreaming is good, day dreaming, not so good.',
                    'author':str(self.user.id),
                    'privacy':'3',
                    'privacy_override': '0',
                    'shared_with':'1',
                    },
         )
        
        #the result must redirect to the same page but not reload the same page (for now)
        self.assertRedirects(response, '/blogging/articles/i-have-a-dream-by-martin-luther-king/1/')
        
        #Try to get all the annotations. Count should be 1, and it must be ours.
               
        self.assertEqual(Annotation.objects.all().count(), 1)
        annotation = Annotation.objects.all()[0]
        self.assertEqual(annotation.body, 'Dreaming is good, day dreaming, not so good.')
        self.assertEqual(annotation.paragraph, 1)
            
        #check if the redirected page is the same as previous one        
        #the response MUST contain the annotation we just posted
    
    def test_retrieve_annotations_for_post(self):
        #use test client to visit the page
        #create a few annotations first
        self.client.post(
            '/annotations/',
            data = {
                    'content_type': '9',
                    'object_id':'1',
                    'paragraph':'1',
                    'body':'Dreaming is good, day dreaming, not so good.',
                    'author':str(self.user.id),
                    'privacy':'3',
                    'privacy_override': '0',
                    'shared_with':'1',
                    },
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
class TestForm(TestCase):
    
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
        
    