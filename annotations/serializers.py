from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from rest_framework.relations import HyperlinkedRelatedField,PrimaryKeyRelatedField

from annotations.models import Annotation, AnnotationShareMap

from blogging.models import BlogContent
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        
        
class AnonymousUserSerializer(serializers.Serializer):
    username = serializers.CharField();


class BlogContentSerializer(serializers.ModelSerializer):
    #Tell BlogContent that it has a relation on Annotations    
    #annotation = BlogContentGenericField()
    #annotation = serializers.RelatedField(many=True, queryset=Annotation.objects.all())
    
    class Meta:
        model = BlogContent
        fields =('id', 'title', 'create_date', 'data', 'url_path', 
                 'author_id', 'published_flag', 'section', 'content_type',
                 )
        
class SerializeReadOnlyField(ReadOnlyField):
    
    def to_representation(self, value):
        if isinstance(value, BlogContent):
            return value.get_absolute_url()

class AnnotationShareMapSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=AnnotationShareMap
        fields = ('user','annotation', 'notified_flag')    

class AnnotationSerializer(serializers.ModelSerializer):
    content_object = SerializeReadOnlyField() 
    #shared_with = HyperlinkedRelatedField(many=True,read_only=False, view_name='user-detail', queryset=AnnotationShareMap.objects.all())
    #shared_with = AnnotationShareMapSerializer()
    shared_with = PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())
    class Meta:
        model = Annotation
        fields = ('content_type', 'object_id', 'id',  'date_created', 'date_modified','content_object',
                  'body', 'paragraph', 
                  'author', 'shared_with',
                  'privacy', 'privacy_override', )  
    
    def save(self, *args, **kwargs):
        print 'In save'
        #print str(self)
        users = self.validated_data.get('shared_with')
        super(AnnotationSerializer, self).save(commit=False, *args, **kwargs)
        for user in users:
            print user
            sharing = AnnotationShareMap(annotation=self.instance, 
                                                    user=user)
            sharing.save() 