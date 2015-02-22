from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from annotations.forms import AnnotationForm
from annotations.models import Annotation_share_map, Annotation

# Create your views here.
def home(request):
    if request.method == 'POST':
        #Handle the post request
        annotation_form = AnnotationForm(request.POST)
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
        
    elif request.method == 'GET':
        #Handle the GET request
        content_type = ContentType.objects.get(model=request.GET.get('content_type', None))
        object_id = request.GET.get('object_id', None)
        
        annotation = Annotation.objects.filter(content_type=content_type.id, object_id=object_id)[0]
        return HttpResponse(annotation.body)
    #Homepage has nothing to do
    
def update(request, id):
    pass