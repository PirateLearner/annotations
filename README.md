PirateLearner Annotations App
=====================================

A per-paragraph commenting app that enables you to:

- Create annotations (like those in medium.com) on per-paragraph basis
- Delete annotations

This app is designed to work with the PirateLearner Blogging App, which powers the unique ID generation for each content paragraph.

**Requirements**

- [Python]<https://www.python.org/> 2.7.
- [Django]<https://www.djangoproject.com/> 1.6.x.
- [Django Rest Framework]<http://www.django-rest-framework.org/> 3.1.0
- [pi-blogging]<http://blogging.readthedocs.org/en/latest/> 0.1.0b1

**Installation**

Use pip for installing the app:

    `pip install pi-annotations --pre`

or download zip file from github [here]<https://github.com/PirateLearner/annotations/archive/master.zip>

after installation, add rest_framework and annotations to your installed apps and also make sure that requirements are also installed -

      |  INSTALLED_APPS = (
      |  ...
      |  'reversion',
      |  'crispy_forms',
      |  'blogging',
      |  'taggit',
      |  'ckeditor',
      |  'django_select2',
      |  'annotations',
      |  'rest_framework',
      |  ...
      |  )

Also add blogging urls in your projects urls.py -

      |  urlpatterns = i18n_patterns('',
      |  ...
      |  url(r'^annotations/', include('annotations.urls', namespace='annotations')),
      |  ...
      |  )

after this just run ``python manage.py syncdb`` for creation of database tables.

NOTE: For setting up blogging app, refer to its [documentation]<http://blogging.readthedocs.org/en/latest/>.