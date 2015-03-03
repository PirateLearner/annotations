from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from annotations.models import Annotation

from blogging.models import BlogContent
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        
        
class AnonymousUserSerializer(serializers.Serializer):
    username = serializers.CharField();


class BlogContentGenericField(serializers.RelatedField):
    
    def to_representation(self, value):
        if isinstance(value, Annotation):
            return AnnotationSerializer(value).data 


class BlogContentSerializer(serializers.ModelSerializer):
    #Tell BlogContent that it has a relation on Annotations    
    #annotation = BlogContentGenericField()
    #annotation = serializers.RelatedField(many=True, queryset=Annotation.objects.all())
    
    class Meta:
        model = BlogContent
        fields =('id', 'title', 'create_date', 'data', 'url_path', 
                 'author_id', 'published_flag', 'section', 'content_type',
                 'tags',)
        
class SerializeReadOnlyField(ReadOnlyField):
    
    def to_representation(self, value):
        if isinstance(value, BlogContent):
            return value.get_absolute_url()
    

class AnnotationSerializer(serializers.ModelSerializer):
    content_object = SerializeReadOnlyField() 
    
    class Meta:
        model = Annotation
        fields = ('content_type', 'object_id', 'id',  'date_created', 'date_modified','content_object',
                  'body', 'paragraph', 
                  'author', 'shared_with',
                  'privacy', 'privacy_override', )   