from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('uploadfile/', views.uploadfile, name='uploadfile'),
    path('Essays/', views.essay_list, name='essay_list'),
    path('Essay/upload/', views.upload_essay, name='upload_essay'),
    path('Topics/', views.topic_list, name='topic_list'),
    path('Topics/generate', views.generate_topic, name='generate_topic'),
    path('BagOfWords/', views.bow_list, name='bow_list'),
    path('BagOfWords/generate', views.generate_bow, name='generate_bow'),
]
