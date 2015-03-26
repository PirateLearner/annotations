from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from annotations.models import Annotation, AnnotationShareMap

from blogging.models import BlogContent
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType

class UserSerializer(serializers.ModelSerializer):
    
    annotations = serializers.PrimaryKeyRelatedField(many=True, 
                                                     queryset=Annotation.objects.all())
    gravatar = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'annotations', 'gravatar', 'url',)
        
    def get_gravatar(self, obj):
        return '#'
    
    def get_url(self, obj):
        return '#'
        
        
        
class AnonymousUserSerializer(serializers.Serializer):
    username = serializers.CharField();

class SerializeReadOnlyField(ReadOnlyField):
    
    def to_representation(self, value):
        if isinstance(value, BlogContent):
            return value.get_absolute_url()

class SerializeAnnotationsField(serializers.SerializerMethodField):
    
    def to_representation(self, value):
        print 'to_repr'
        print type(value)
        if isinstance(value, Annotation):
            return AnnotationSerializer(value)
        if isinstance(value, dict):
            print 'Is annotation'
            return AnnotationSerializer(value, many=True)
        
class BlogContentSerializer(serializers.ModelSerializer):
    #Tell BlogContent that it has a relation on Annotations    
    annotation = serializers.SerializerMethodField()
    #annotation = SerializeAnnotationsField()
    
    class Meta:
        model = BlogContent
        fields =('id', 'title', 'create_date', 'data', 'url_path', 
                 'author_id', 'published_flag', 'section', 'content_type',
                 'annotation',)
     
    def get_annotation(self, obj):
        content_object = ContentType.objects.get_for_model(obj)
        print "In BlogContentSerializer"
        print obj
        annotations =  Annotation.objects.filter(content_type=content_object.id, object_id=obj.id)
        if len(annotations) is not 0:
            print AnnotationSerializer(annotations, many=True).data
            return (AnnotationSerializer(annotations, many=True).data)
        else:
            return None

class AnnotationShareMapSerializer(serializers.ModelSerializer):    
    class Meta:
        model=AnnotationShareMap
        fields = ('user','annotation', 'notified_flag')    



class AnnotationSerializer(serializers.ModelSerializer):
    #I want the content object is a hyperlink to the ContentObject
    content_object = SerializeReadOnlyField()
    
    shared_with = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())
    #author = serializers.ReadOnlyField(source='author.username')
    author = UserSerializer(read_only=True)
    class Meta:
        model = Annotation
        fields = ('content_type', 'object_id', 'id',  'date_created', 'date_modified','content_object',
                  'body', 'paragraph', 
                  'author', 'shared_with',
                  'privacy', 'privacy_override', )  
    
    def create(self, validated_data):
        print "In create"
        print validated_data
        annotation = Annotation()
        annotation.author = validated_data.get('author')
        annotation.body = validated_data.get('body')
        annotation.content_type = validated_data.get('content_type')
        annotation.object_id = validated_data.get('object_id')
        annotation.paragraph = validated_data.get('paragraph')
        
        annotation.privacy = validated_data.get('privacy')
        annotation.privacy_override = validated_data.get('privacy_override', False)

        #Get row from contentType which has content_type
        content_object = ContentType.objects.get_for_id(annotation.content_type.id)
        
        annotation.content_object = content_object.model_class().objects.get(id=annotation.object_id)
        
        print annotation.content_object          
        annotation.save()

        print validated_data.get('shared_with')
        for user in validated_data.get('shared_with'):
            sharing = AnnotationShareMap(annotation=annotation, 
                                                    user=user)
            sharing.save()
        
        return annotation
    
    def update(self, instance, validated_data):
        print "In update"
        annotation = instance
        annotation.author = validated_data.get('author', annotation.author)
        annotation.body = validated_data.get('body', annotation.body)
        annotation.content_type = validated_data.get('content_type',annotation.content_type)
        annotation.object_id = validated_data.get('object_id',annotation.object_id)
        annotation.paragraph = validated_data.get('paragraph',annotation.paragraph)
        
        annotation.privacy = validated_data.get('privacy',annotation.privacy)
        annotation.privacy_override = validated_data.get('privacy_override',annotation.privacy_override)

        #Get row from contentType which has content_type
        content_object = ContentType.objects.get_for_id(annotation.content_type.id)        
        annotation.content_object = content_object.model_class().objects.get(id=annotation.object_id)        
        
        print annotation.content_object     
                
        annotation.save()
        
        print validated_data.get('shared_with')
        for user in validated_data.get('shared_with'):
            sharing = AnnotationShareMap(annotation=annotation, 
                                                    user=user)
            sharing.save()
        return annotation