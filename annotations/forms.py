from django import forms
from annotations.models import Annotation

class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ['id', 'content_type', 'object_id', 'body', 'author', 'privacy',
                  'paragraph','privacy_override', 'shared_with']
