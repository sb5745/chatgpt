from django import forms
from .models import ConversationRoom

class ConversationRoomForm(forms.ModelForm):
    class Meta:
        model = ConversationRoom
        fields = ['title', 'role', 'attached_file']  # 파일 필드를 포함한 폼
