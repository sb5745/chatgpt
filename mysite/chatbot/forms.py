from django import forms
from .models import ConversationRoom, Topic, AttachedFile

class ConversationRoomForm(forms.ModelForm):
    class Meta:
        model = ConversationRoom
        fields = ['title', 'role']  # 파일 필드를 포함한 폼

# TopicForm 추가
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']  # 주제명과 설명 필드를 포함

# 파일 첨부 폼 추가 (옵션)
class AttachedFileForm(forms.ModelForm):
    class Meta:
        model = AttachedFile
        fields = ['file']  # 파일 필드만 포함