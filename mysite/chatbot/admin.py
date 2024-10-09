from django.contrib import admin
from .models import ConversationRoom, Conversation

class ConversationRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at')  # ID와 함께 다른 필드도 표시 가능

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'role', 'content', 'timestamp')  # ID와 함께 다른 필드도 표시 가능

admin.site.register(ConversationRoom, ConversationRoomAdmin)
admin.site.register(Conversation, ConversationAdmin)

