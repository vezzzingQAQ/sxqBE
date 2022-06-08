from django.urls import path
from zvoice import views

urlpatterns = [
    path('getStudent', views.getStudentView),
    path('setVoice', views.setVoiceView),
    path('getVoiceByClass', views.getVoiceByClassView),
    path('riseErr',views.testErr),
]
