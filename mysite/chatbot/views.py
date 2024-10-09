from django.shortcuts import render, redirect
from django.http import HttpResponse
from openai import OpenAI
from django.contrib.auth.decorators import login_required
from .models import ConversationRoom, Conversation  # Conversation 모델 임포트 추가
from config import OPENAI_API_KEY, DEFAULT_MODEL
from .forms import ConversationRoomForm

# OpenAI API 설정
client = OpenAI(api_key=OPENAI_API_KEY)

# 새로운 대화방 생성 뷰
@login_required
def create_room(request):
    if request.method == 'POST':
        form = ConversationRoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)  # 저장은 잠시 보류
            room.user = request.user  # 현재 로그인한 사용자와 연결
            room.save()  # user 값이 설정된 후에 저장
            return redirect('chat')  # 대화 페이지로 리다이렉트
    else:
        form = ConversationRoomForm()

    return render(request, 'chatbot/create_room.html', {'form': form})

@login_required
def chat_view(request):
    user = request.user  # 로그인된 사용자만 접근
    
    rooms = ConversationRoom.objects.filter(user=user)
    # 사용자가 선택한 방 ID
    selected_room_id = request.GET.get('room_id')
    selected_room = None
    conversations = []

    if selected_room_id:
        # 사용자가 선택한 방이 있을 경우 해당 방의 대화를 가져옴
        try:
            selected_room = ConversationRoom.objects.get(id=selected_room_id, user=user)
            conversations = Conversation.objects.filter(room=selected_room).order_by('timestamp')
        
            file_content = ""
            if selected_room.attached_file:
                file_path = selected_room.attached_file.path
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
        
        except ConversationRoom.DoesNotExist:
            return redirect('chat')  # 방이 없을 경우 기본 대화 페이지로 리다이렉트

    if request.method == 'POST':
        # 사용자가 입력한 메시지 가져오기
        user_message = request.POST.get('user_message')
        model = request.POST.get('model', DEFAULT_MODEL)  # 기본값은 'gpt-4-turbo'

      # 대화방이 선택되지 않은 경우 처리
        if not selected_room:
            return HttpResponse("대화방을 선택해주세요.", status=400)
  
        # OpenAI API에 사용자 메시지 전달 및 응답 받기
        response = client.chat.completions.create(
            model= model,
            messages=[
                {"role": "system", "content": file_content},  # 파일 내용 추가
                {"role": "user", "content": user_message}
            ]
        )
        assistant_message = response.choices[0].message.content.strip()
        
        # 대화 내용을 데이터베이스에 저장
        Conversation.objects.create(room=selected_room, user=user, role='user', content=user_message)
        Conversation.objects.create(room=selected_room, user=user, role='assistant', content=assistant_message)

        # 최신 대화 내용 다시 불러오기
        conversations = Conversation.objects.filter(room=selected_room).order_by('timestamp')

    # 템플릿으로 대화 기록 전달
    return render(request, 'chatbot/chat.html', {
        'rooms': rooms,
        'selected_room': selected_room,
        'conversations': conversations,
    })
