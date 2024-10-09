# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User

class ConversationRoom(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자와 연결된 외래키
    role = models.CharField(max_length=255, default="user")  # 'user' 또는 'assistant'
    title = models.CharField(max_length=255, default="Default Room")  # 방 제목 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)

    # 새롭게 추가: 대화방에 파일을 첨부
    attached_file = models.FileField(upload_to='uploads/', blank=True, null=True)


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
