from django.urls import path
#from .templates.chatbot import views
from .import views

urlpatterns = [
    path('', views.chat_view, name='chat'),  # 기본 경로로 요청이 들어오면 chat_view가 호출됩니다.
    path('create_room/', views.create_room, name='create_room'),  # 대화방 생성 경로 추가
]
