from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

class Annotation(models.Model):
    PRIVACY_PUBLIC = 0
    PRIVACY_AUTHOR = 1
    PRIVACY_GROUP = 2
    PRIVACY_PRIVATE = 3
    PRIVACY_OPTIONS = (
                       (PRIVACY_PUBLIC, 'public'),
                       (PRIVACY_AUTHOR, 'author'),
                       (PRIVACY_GROUP, 'group'),
                       (PRIVACY_PRIVATE, 'private'),
                      )
    #Relations with other objects
    content_type = models.ForeignKey(ContentType, 
                                     verbose_name=_("Content Type"), 
                                     related_name="content_type_set_for_annotations")
    object_id = models.TextField(_("object ID"))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    #User relevant stuff
    body = models.TextField()
    paragraph = models.PositiveIntegerField(null=False)
    '''
    Annotations can be written only by logged in users. If the user cannot afford 
    to make himself and his interest in reading known, alas, we cannot help him in
    case of making annotations. It is also to prevent hit and run comments by people
    under anonymity.
    '''
    author = models.ForeignKey(User, related_name="annotations", null=False, blank=False, verbose_name=_("Annotation author"))
    #Privacy settings
    privacy= models.PositiveSmallIntegerField(choices=PRIVACY_OPTIONS, default=PRIVACY_PRIVATE)
    #Privacy reset for Spam protection, if annotation has been shared (and marked as offensive)
    privacy_override = models.BooleanField(default=False)
    #Shared with these users.
    shared_with = models.ManyToManyField(User, through="AnnotationShareMap", null=True, blank=True)
    
    #Statistics related stuff
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.body
    
    def __str__(self):
        return self.body
    
    class Meta:
        app_label = 'annotations'


class AnnotationShareManager(models.Manager):
    
    def get_query_set(self):
        qs = super(AnnotationShareManager, self).get_query_set()
        return qs
    

class AnnotationShareMap(models.Model):
    '''@class Annotation_share_map
    Maintains a map of which annotation has been shared by the user with which of his friends, if applicable.
    Notification about the sharing should be sent to each person only once, even if the user edits the 
    comment later
    '''
    user = models.ForeignKey(User, related_name="annotation_shared_with")
    annotation = models.ForeignKey(Annotation)
    notified_flag = models.BooleanField(default = False)
    objects = AnnotationShareManager()
    
    def __unicode__(self):
        return str(self.annotation) + ' shared with ' + str(self.user)
    
    def __str__(self):
        return str(self.annotation) + ' shared with ' + str(self.user)
    
    class Meta:
        app_label = 'annotations'   