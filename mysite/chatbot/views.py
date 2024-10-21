from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from openai import OpenAI
from django.contrib.auth.decorators import login_required
from .models import ConversationRoom, Conversation, Topic, AttachedFile  # Conversation 모델 임포트 추가

from config import  DEFAULT_MODEL, SHA_CODE
from .forms import ConversationRoomForm, TopicForm, AttachedFileForm
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

# OpenAI API 설정
client = OpenAI(api_key=SHA_CODE)

@login_required
def create_topic(request):
    print("주제 생성 중입니다.") 
    if request.method == 'POST':
        print(f"서버에 전송된 파일: {request.FILES}")   # 서버로 전송된 파일들을 출력하여 확인
        # POST 요청에서 폼 데이터를 처리
        topic_form = TopicForm(request.POST)  # TopicForm에서 title과 description 처리
        
        if topic_form.is_valid():  # 폼 유효성 검사
            new_topic = topic_form.save()  # 주제 저장
            
            # 파일이 첨부된 경우에만 처리
            if request.FILES.getlist('attached_file'):
                files = request.FILES.getlist('attached_file')  # 여러 파일을 리스트로 가져옴
                print(f"첨부된 파일 리스트: {files}") 
                
                for file in files:
                    print(f"처리 중인 파일: {file}")  # 로그 추가
                    # 각각의 파일에 대해 폼 생성
                    attached_file_form = AttachedFileForm({'topic': new_topic}, {'file': file})
                    
                    if attached_file_form.is_valid():
                        attached_file = attached_file_form.save(commit=False)
                        attached_file.topic = new_topic  # 주제와 파일을 연결
                        attached_file.save()  # 파일 저장
                    else:
                        print(f"첨부 파일 폼 에러: {attached_file_form.errors}")  # 폼 유효성 오류가 있으면 출력
                        
                # JSON 응답 반환
            return JsonResponse({'success': True, 'redirect_url': '/chat/'})
            #return redirect('chat')  # 생성 후 대화 목록으로 리다이렉트

        return JsonResponse({'success': False, 'error': '잘못된 요청'})  # GET 요청 처리
        
    # GET 요청일 때 빈 폼을 렌더링
    topic_form = TopicForm()
    attached_file_form = AttachedFileForm()

    return render(request, 'chatbot/create_topic.html', {
        'topic_form': topic_form,
        'attached_file_form': attached_file_form
    })

# 주제 정보를 가져오는 View
def get_topic_info(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
        attached_files = [{'name': file.file.name} for file in topic.attached_files.all()]
        data = {
            'title': topic.title,
            'description': topic.description,
            'files': attached_files
        }
        return JsonResponse(data)
    except Topic.DoesNotExist:
        return JsonResponse({'error': 'Topic not found'}, status=404)

def get_room_info(request, room_id):
    try:
        # 대화방 정보 가져오기
        room = ConversationRoom.objects.get(id=room_id)
        # 첨부된 파일들 가져오기
        attached_files = [{'name': file.file.name} for file in room.attached_files.all()]
        
        # 대화방 정보 구성
        data = {
            'title': room.title,
            'created_by': room.user.username,
            'created_at': room.created_at.strftime('%Y-%m-%d %H:%M'),
            'files': attached_files,
            'conversations': [{'role': conv.role, 'content': conv.content} for conv in room.conversations.all()]
             
        }
        
        return JsonResponse(data)
    
    except ConversationRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)


@login_required
def edit_topic(request, topic_id):
    #topic = Topic.objects.get(id=topic_id)
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        # 대화 주제명과 설명 수정
        topic.title = request.POST.get('title')
        topic.description = request.POST.get('description')
        topic.save()

        # 파일 첨부
        if 'attached_file' in request.FILES:
            for file in request.FILES.getlist('attached_file'):
                attached_file = AttachedFile(topic=topic, file=file)
                attached_file.save()
        return redirect('chat')
    attached_files = AttachedFile.objects.filter(topic=topic)

    return render(request, 'chatbot/edit_topic.html', {
        'selected_topic': topic,
        'attached_files': attached_files
    })

@login_required
def delete_topic(request, topic_id):
    if request.method == 'DELETE':
        topic = get_object_or_404(Topic, id=topic_id)
        topic.delete()
        return JsonResponse({'message': '주제가 삭제되었습니다.'}, status=200)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

@login_required
def delete_file(request, topic_id, file_id):
    try:
        topic = get_object_or_404(Topic, id=topic_id)
        file = get_object_or_404(AttachedFile, id=file_id, topic=topic)
        file.delete()  # 파일 삭제
        return JsonResponse({'success': True})  # JSON으로 성공 응답
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})  # 에러 응답
    
@login_required
def create_room(request): # 새로운 대화방 생성 뷰
    if request.method == 'POST':
        conversationRoom_form  = ConversationRoomForm(request.POST, request.FILES)
        if conversationRoom_form .is_valid():
            room = conversationRoom_form .save(commit=False)  # 저장은 잠시 보류
            room.user = request.user  # 현재 로그인한 사용자와 연결
            
            topic_id = request.GET.get('topic_id')  # URL에서 topic_id를 가져옴
            if topic_id:  # 주제 ID가 존재하는 경우에만
                room.topic_id = topic_id  # 대화방에 주제 ID 저장
            room.save()  # user 값이 설정된 후에 저장

            files = request.FILES.getlist('attached_file')  # 'attached_file'로부터 여러 파일 가져오기
            for file in files:
                attached_file = AttachedFile.objects.create(file=file)  # AttachedFile 생성
                room.attached_files.add(attached_file)  # 대화방에 파일 추가

            return redirect('chat')  # 대화 페이지로 리다이렉트
    else:
        conversationRoom_form  = ConversationRoomForm()

    return render(request, 'chatbot/create_room.html', {'form': conversationRoom_form })

@login_required
def upload_file(request):
    if request.method == 'POST' and 'attached_file' in request.FILES:
        attached_file = request.FILES.getlist('attached_file')  # 여러 파일 처리
        topic_id = request.POST.get('topic_id')
        room_id = request.POST.get('room_id')

        # Topic 또는 Room에 해당하는 객체 가져오기
        obj = None
        if topic_id:
            obj = get_object_or_404(Topic, id=topic_id)
        elif room_id:
            obj = get_object_or_404(ConversationRoom, id=room_id)

        # 파일 저장 로직
        uploaded_files = []
        for file in attached_file:
            uploaded_file = AttachedFile(
                file=file,
                topic=obj if isinstance(obj, Topic) else None,
                room=obj if isinstance(obj, ConversationRoom) else None
            )
            uploaded_file.save()
            uploaded_files.append({'id': uploaded_file.id, 'name': file.name})  # 파일 ID와 이름 저장

        # 업로드 성공 메시지 반환 (JSON)
                # 업로드 성공 메시지 반환 (JSON)
        return JsonResponse({'success': True, 'files': uploaded_files})

    return JsonResponse({'success': False, 'error': '파일 업로드 실패'})

@login_required
def chat_view(request):
    user = request.user  # 로그인된 사용자만 접근
    rooms = ConversationRoom.objects.filter(user=user).order_by('-created_at')
    selected_room_id = request.GET.get('room_id')# 사용자가 선택한 방 ID
    selected_topic_id = request.GET.get('topic_id')  # 주제 ID 가져오기
    selected_room = None
    selected_topic = None
    conversations = []
    topic_file_contents = []  # 주제에 첨부된 파일 내용을 저장할 리스트
    room_file_contents = []  # 파일 내용을 저장할 리스트
    topic_attached_files = [] 
    room_attached_files = [] 

    topics = Topic.objects.prefetch_related('rooms').all().order_by('-created_at')  # 대화주제 불러오기

    if request.method == 'POST' and 'attached_file' in request.FILES:   # 주제에 복수의 파일을 첨부할 경우 처리
        print(request.FILES.getlist('attached_file'))  # 파일 리스트 출력
        files = request.FILES.getlist('attached_file')  # 여러 파일을 받아옴
        topic_id = request.POST.get('topic_id')
        selected_topic = Topic.objects.get(id=topic_id)
        
        for file in files:
            attached_file = AttachedFile.objects.create(file=file)
            selected_topic.attached_files.add(attached_file)  # 주제와 파일 연결
        selected_topic.save()

        topic_attached_files = selected_topic.attached_files.all()  if selected_topic else []  # 대화방에 첨부된 파일 리스트 처리 (save() 후 처리)

    if selected_topic_id:
        try:
            selected_topic = Topic.objects.get(id=selected_topic_id)  # 선택된 주제 가져오기
            if selected_topic.attached_files.exists():  # 주제에 첨부된 파일이 있는 경우 파일 내용 읽기

                for attached_file in selected_topic.attached_files.all():
                        file_path = attached_file.file.path
                        with open(file_path, 'r', encoding='utf-8') as f:
                            topic_file_content = f.read()
                            topic_file_contents.append(topic_file_content)  # 파일 내용을 리스트에 추가
                            # 주제 파일 내용 처리 (필요에 따라 추가적인 작업 가능)

        except Topic.DoesNotExist:
            selected_topic = None  # 선택된 주제가 없을 경우 None 처리
 
    if request.method == 'POST' and 'attached_file' in request.FILES:   # 대화방 파일 업로드 처리 (복수 파일 처리)
        files = request.FILES.getlist('attached_file')  # 여러 파일을 받아옴
        room_id = request.POST.get('room_id')
        selected_room = ConversationRoom.objects.get(id=room_id, user=user)
        
        for file in files:  # 파일들을 하나씩 처리하여 대화방에 첨부
            attached_file = AttachedFile.objects.create(file=file)  # 새 파일 객체 생성
            selected_room.attached_files.add(attached_file)  # 대화방과 파일 연결
        selected_room.save()

        room_attached_files = selected_room.attached_files.all() # 대화방에 첨부된 파일 리스트 처리 (save() 후 처리)

    if selected_room_id:
        try:  # 사용자가 선택한 방이 있을 경우 해당 방의 대화를 가져옴
            selected_room = ConversationRoom.objects.get(id=selected_room_id, user=user)
            conversations = Conversation.objects.filter(room=selected_room).order_by('timestamp')
        
            if selected_room.attached_files.exists():     # 파일이 존재함
            #if selected_room.attached_files and selected_room.attached_file.name and selected_room.attached_file.storage.exists(selected_room.attached_file.name):

                for attached_file in selected_room.attached_files.all():
                    file_path = attached_file.file.path
                    with open(file_path, 'r', encoding='utf-8') as f:
                        room_file_content  = f.read()
                        room_file_contents.append(room_file_content )  # 파일 내용을 리스트에 추가
                        #print(f"파일 내용: {file_content}")  # 터미널에 파일 내용을 출력
        
        except ConversationRoom.DoesNotExist:
            return redirect('chat')  # 방이 없을 경우 기본 대화 페이지로 리다이렉트

    if request.method == 'POST': # OpenAI API 요청 및 대화 처리 (생략 가능)
        user_message = request.POST.get('user_message')  # 사용자가 입력한 메시지 가져오기
        model = request.POST.get('model', DEFAULT_MODEL)  # 기본값은 'gpt-4-turbo'

        if not selected_room:  # 대화방이 선택되지 않은 경우 처리
            return HttpResponse("대화방을 선택해주세요.", status=400)
  
        response = client.chat.completions.create(  # OpenAI API에 사용자 메시지 전달 및 응답 받기
            model= model,
            messages=[
                {"role": "system", "content": "\n".join(topic_file_contents)},  # 주제 파일 내용
                {"role": "system", "content": "\n".join(room_file_contents)},   # 대화방 파일 내용
                {"role": "user", "content": user_message}
            ]
        )
        assistant_message = response.choices[0].message.content.strip()
        
        Conversation.objects.create(room=selected_room, user=user, role='user', content=user_message)  # 대화 내용을 데이터베이스에 저장
        Conversation.objects.create(room=selected_room, user=user, role='assistant', content=assistant_message)
        conversations = Conversation.objects.filter(room=selected_room).order_by('timestamp')   # 최신 대화 내용 다시 불러오기
   
    return render(request, 'chatbot/chat.html', {    # 템플릿으로 대화 기록 전달
        'topics': topics,    
        'selected_topic': selected_topic,  # 선택된 주제
        'topic_attached_files': topic_attached_files,  # 대화방에 첨부된 파일 리스트
        'topic_file_contenst': topic_file_contents,  # 주제 파일 내용 추가
        'rooms': rooms,
        'selected_room': selected_room,
        'room_attached_files': room_attached_files,  # 대화방에 첨부된 파일 리스트
        'room_file_contents': room_file_contents,  # 방 파일 내용
        'conversations': conversations,
    })
