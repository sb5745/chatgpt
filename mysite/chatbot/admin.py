from django.contrib import admin
from .models import ConversationRoom, Conversation, Topic, AttachedFile

class ConversationRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'topic', 'created_at')  # I# 'topic'을 추가하여 주제 표시

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'role', 'content', 'timestamp')  # ID와 함께 다른 필드도 표시 가능

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'get_attached_files')

    def get_attached_files(self, obj):
        return ", ".join([f.file.name for f in obj.attached_files.all()])
    
admin.site.register(Topic, TopicAdmin)
admin.site.register(ConversationRoom, ConversationRoomAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(AttachedFile)
