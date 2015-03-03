from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from annotations.forms import AnnotationForm
from annotations.models import Annotation_share_map, Annotation

import json
from django.core import serializers

# Create your views here.
def home(request):
    if request.method == 'POST':
        #Handle the post request
        json_data = json.loads(request.body)

        annotation_form = AnnotationForm(json_data)
        #validate form
        if annotation_form.is_valid() is False:
            #Parse and debug error
            print 'Did not validate'
            print annotation_form.errors            
        else:            
            #save the annotation
            #Can't save a M2M field when using a custom table using 'through'
            mapping = annotation_form.save(commit=False)
            mapping.save()
            for user in annotation_form.cleaned_data.get('shared_with'):
                sharing = Annotation_share_map(annotation=mapping, user=user)
                sharing.save()
        #Find the reverse URL of the object where this annotation was posted
        '''
        #Get an instance of the object on which the annotation was posted.
        content_type = annotation_form.cleaned_data['content_type'];
        object_id = annotation_form.cleaned_data['object_id'];
        #Get row from contentType which has content_type
        content_object = ContentType.objects.get_for_id(content_type.id)
        #Get row from parent table whose parameters are stored in the object we fetched
        #object_instance = content_object.get_object_for_this_type(pk=object_id)
        object_instance = content_object.model_class().objects.get(id=object_id) 
        #get a reverse URL now
        reverse_url = object_instance.get_absolute_url()      
        return(HttpResponseRedirect(reverse_url))
        '''
        annotation_json = {
                           'body': annotation_form.cleaned_data['body'],
                           'paragraph':annotation_form.cleaned_data['paragraph'],
                           'id': mapping.id                           
                           }
        return HttpResponse(
                           json.dumps(annotation_json),
                           content_type='application/json'
                           )
    elif request.method == 'GET':
        #Handle the GET request
        content_type = ContentType.objects.get(model=request.GET.get('content_type', None))
        object_id = request.GET.get('object_id', None)
        
        annotation = Annotation.objects.filter(content_type=content_type.id, object_id=object_id)
        annotation_json =serializers.serialize('json', annotation)
        return HttpResponse(
                            annotation_json,
                           content_type='application/json'
                           )
    #Homepage has nothing to do
    
def update(request, id):
    pass

from rest_framework import viewsets
from annotations.serializers import *
from rest_framework import permissions
from utils import IsOwnerOrReadOnly, AnnotationIsOwnerOrReadOnly

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from blogging.models import BlogContent

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class BlogContentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = BlogContent.objects.all()
    serializer_class = BlogContentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.author_id = self.request.user
        

class AnnotationViewSet(viewsets.ModelViewSet):
    
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, AnnotationIsOwnerOrReadOnly,)
    
    def pre_save(self, obj):
        obj.user = self.request.user

# From hence, all models are representation of things that don't actually exist

from rest_framework.views import APIView

class BlogContentCommentView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        #First, get the model instance of BlogContent
        obj = BlogContent.objects.get(pk=pk)
        #Then, get the content type instance
        content_type = ContentType.objects.get_for_model(obj)
        annotations = Annotation.objects.filter(content_type= content_type.id, object_pk=obj.id)
        print annotations
        
        #Now, put them into a serializer
        serializer = AnnotationSerializer(annotations, many=True)
        return Response(serializer.data)
        

class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        user_obj = self.request.user
        if(user_obj.id != None):
            serializer = UserSerializer(user_obj)
        else:
            serializer = AnonymousUserSerializer(user_obj)
            print(serializer.data)
             
        return Response(serializer.data)                