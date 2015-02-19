from django.test import TestCase
from django.core.urlresolvers import resolve
from annotations.views import home

from annotations.models import Annotation

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
#from django.http import request

# Create your tests here.
class TestAnnotations(TestCase):
    
    def setup(self):
        self.user = User(username="craft")
        self.user.save()
        
    def teardown(self):
        pass
    
    def test_can_resolve_app_url(self):
        obj = resolve('/annotations/')
        self.assertEqual(obj.func, home)
        
    def test_create_annotation(self):
        annotation = Annotation()
        annotation.content_type=ContentType.objects.get(model='blogcontent', app_label="blogging")
        annotation.object_id= str(1)
        annotation.body="This is a test annotation"
        annotation.author= User.objects.get(id=1)
                
        annotation.save()
        
    def test_POST_annotation(self):
        #use test client to POST a request
        
        #the result must redirect to the same page but not reload the same page (for now)
        
        #check if the redirected page is the same as previous one
        
        #the response MUST contain the annotation we just posted
        pass
    
    def test_retrieve_annotations_for_post(self):
        #use test client to visit the page
        
        #create a few annotations on random paragraphs
        
        #get must return the same amount of annotations
        pass
    
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
    
    
    