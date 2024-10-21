from django.urls import path
#from .templates.chatbot import views
from .import views

urlpatterns = [
    path('create_topic/', views.create_topic, name='create_topic'),
    path('', views.chat_view, name='chat'),  # 기본 경로로 요청이 들어오면 chat_view가 호출됩니다.
    path('create_room/', views.create_room, name='create_room'),  # 대화방 생성 경로 추가
    path('upload/', views.upload_file, name='upload_file'),  # 파일 업로드를 위한 URL 추가

    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('edit_topic/<int:topic_id>/delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    
    path('get_topic_info/<int:topic_id>/', views.get_topic_info, name='get_topic_info'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),

    path('get_room_info/<int:room_id>/', views.get_room_info, name='get_room_info'),
]
