# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=255)  # 대화주제의 제목
    description = models.TextField(blank=True, null=True)  # 설명 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)  # 주제 생성 시각

    def __str__(self):
        return self.title


# 새롭게 추가되는 AttachedFile 모델
class AttachedFile(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='attached_files')  # 주제와 연결
    conversation_room = models.ForeignKey('ConversationRoom', on_delete=models.CASCADE, related_name='attached_files', null=True, blank=True)  # 대화방과 연결
    file = models.FileField(upload_to='uploads/')  # 파일 저장 경로
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 파일이 업로드된 시간

    def __str__(self):
        return self.file.name

class ConversationRoom(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True, related_name='rooms')  # 대화주제와 연결
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자와 연결된 외래키
    role = models.CharField(max_length=255, default="user")  # 'user' 또는 'assistant'
    title = models.CharField(max_length=255, default="Default Room")  # 방 제목 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"{self.title} - {self.user.username}"  # 방 제목과 사용자 이름 표시
    
# 대화 내용 모델 수정하여 대화방 연결
class Conversation(models.Model):
    room = models.ForeignKey(ConversationRoom, on_delete=models.CASCADE, related_name='conversations', default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
    
