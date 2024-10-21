
// 대화주제를 수정할 수 있는 폼을 표시하는 함수
function showEditForm() {
    if (selectedTopicId) {
        console.log("수정할 Topic ID: ", selectedTopicId);
        window.location.href = `/chat/edit_topic/${selectedTopicId}/`;
    } else {
        console.error('Topic ID가 유효하지 않습니다.');
    }
}

// 파일을 제거하는 함수
function removeFile(topicId, fileId) {
    //fetch('/remove_file/', {
    fetch(`/chat/edit_topic/${topicId}/delete_file/${fileId}/`, { 

        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,  // CSRF 토큰 가져오기
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ file_id: fileId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('file-' + fileId).remove();  // UI에서 파일 항목을 제거
        } else {
            alert('파일 제거 실패: ' + data.error);
        }
    })
    .catch(error => {
        console.error('파일 제거 중 오류 발생:', error);
    });
}


// 파일 첨부 후 리스트에 동적으로 추가하는 함수
function addFileToList(file) {
    const fileList = document.getElementById('file-list');
    const newFileItem = document.createElement('li');

    newFileItem.id = 'file-' + file.id;
    newFileItem.innerHTML = `
        ${file.name}
        <button type="button" onclick="removeFile(${selectedTopicId}, ${file.id})">삭제</button>
    `;
    fileList.appendChild(newFileItem);
}

// 파일을 업로드하고 서버에서 응답을 받는 함수
function uploadFile(formData, topicId) {
    fetch(`/chat/edit_topic/${topicId}/upload_file/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value, // CSRF 토큰 포함
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 서버에서 성공적으로 파일이 업로드되었을 때, 파일을 리스트에 추가
            data.files.forEach(file => {
                addFileToList({
                    id: file.id,       // 서버에서 받은 파일 ID
                    name: file.name    // 서버에서 받은 파일 이름
                });
            });
          } else {
            alert('파일 업로드 실패: ' + data.error);
        }
    })
    .catch(error => {
        console.error('파일 업로드 중 오류 발생:', error);
    });
}

//document.getElementById('submit_button').addEventListener('click', function(event) {
// submit_button이 존재하는지 확인한 후 addEventListener 추가
const submitButton = document.getElementById('submit_button');
if (submitButton) {
    submitButton.addEventListener('click', function(event) {


        event.preventDefault();  // 기본 폼 제출 동작 막기

        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const fileInput = document.getElementById('attached_file');
        const formData = new FormData();

        // 주제명과 설명을 formData에 추가
        formData.append('title', title);
        formData.append('description', description);

        // 파일이 있으면 파일도 추가
        if (fileInput.files.length > 0) {
            for (let i = 0; i < fileInput.files.length; i++) {
                formData.append('attached_file', fileInput.files[i]);
            }
        }

        // 주제 생성 API 호출
        fetch('/chat/create_topic/', {  // 주제 생성 엔드포인트
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 주제 생성이 성공하면 주제 ID를 받아서 selectedTopicId에 저장
                selectedTopicId = data.topic_id;
                alert("주제가 성공적으로 생성되었습니다.");
                
                // 필요한 경우 추가적인 작업 수행 (예: 페이지 이동 또는 목록 업데이트)
            } else {
                alert("주제 생성 실패: " + data.error);
            }
        })
        .catch(error => {
            console.error("주제 생성 중 오류 발생:", error);
        });
    });
}

const deleteButton = document.getElementById('delete-topic-btn');
if (deleteButton) {
    deleteButton.addEventListener('click', function() {
    console.log("삭제 버튼 클릭됨. Selected Topic ID: ", selectedTopicId);        
        if (!selectedTopicId) {
            alert("주제 ID가 없습니다.");
            return;
        }
        
        //if (confirm("deleteButton 정말로 이 주제를 삭제하시겠습니까?")) {
        deleteTopic();  // 주제 삭제 요청
        //}
    });
}

let selectedTopicId = null;  // 선택된 주제 ID를 저장하는 전역 변수

function showTopicInfo(topicId) {  // 주제 정보를 오른쪽 패널에 표시하는 함수
    console.log("Selected Topic ID: ", topicId);
    selectedTopicId = topicId;// 선택된 Topic ID를 전역 변수에 저장

    // Ajax 또는 fetch로 주제 정보를 가져와서 오른쪽 패널에 표시
    fetch(`/get_topic_info/${topicId}/`)
        .then(response => response.json())
        .then(data => {
            // 주제 정보를 HTML 요소에 반영
            document.getElementById("topic-title-display").textContent = data.title;
            document.getElementById("topic-description-display").textContent = data.description;

            // 파일 리스트 업데이트
            const fileList = document.getElementById("file-list");
            fileList.innerHTML = '';  // 기존 파일 리스트 초기화
            data.files.forEach(file => {
                const li = document.createElement("li");
                li.textContent = file.name;
                fileList.appendChild(li);
            });
            // 주제 정보 패널 보이기
            document.getElementById("show-topic-form").style.display = "block";
            document.getElementById("no-selection-message").style.display = "none"; // 메시지 숨기기
        })
        .catch(error => {
            console.error('주제 정보를 가져오는 중 오류 발생:', error);
        });
}

let selectedRoomId = null;  // 선택된 대화방 ID를 저장하는 전역 변수

function showRoomInfo(roomId) {
    console.log("Selected Room ID: ", roomId);
    selectedRoomId = roomId;  // 선택된 Room ID를 전역 변수에 저장

    fetch(`/get_room_info/${roomId}/`)
        .then(response => response.json())
        .then(data => {
            // 대화방 정보 표시
            
            document.getElementById('room-title-display').textContent = data.title;
            document.getElementById('room-created-by').textContent = data.created_by ;
            document.getElementById('room-created-at').textContent = data.created_at;

            // 파일 리스트 업데이트
            const fileList = document.getElementById('room-file-list');
            fileList.innerHTML = '';  // 기존 파일 리스트 초기화
            if (data.files.length > 0) {    
                data.files.forEach(file => {
                    const li = document.createElement('li');
                    const a = document.createElement('a');
                    a.href = file.file_url;
                    a.textContent = file.file_name;
                    li.appendChild(a);
                    fileList.appendChild(li);
                });
            } else {
                const p = document.createElement('p');
                p.textContent = '업로드된 파일이 없습니다.';
                fileList.appendChild(p);
            }

           // 대화 내용 업데이트
           const conversationDiv = document.getElementById('conversation');
           conversationDiv.innerHTML = '';  // 기존 대화 내용 초기화
           if (data.conversations.length > 0) {
               data.conversations.forEach(message => {
                   const p = document.createElement('p');
                   p.innerHTML = `<strong>${message.role}:</strong> ${message.content}`;
                   conversationDiv.appendChild(p);
               });
           } else {
               const p = document.createElement('p');
               p.textContent = '대화를 시작해 주세요.';
               conversationDiv.appendChild(p);
           }

            // 대화방 정보 패널 보이기
            document.getElementById('show-room-form').style.display = 'block';
            document.getElementById('no-selection-message').style.display = 'none';  // 기본 메시지 숨기기
            document.getElementById('show-topic-form').style.display = 'none';
        })
        .catch(error => {
            console.error('대화방 정보를 가져오는 중 오류 발생:', error);
        });
}


let isDeleting = false;

function deleteTopic() {  // 주제를 삭제하는 함수
    if (isDeleting) {      // 삭제 중인지 확인
        return;  // 삭제 요청이 이미 진행 중이면 추가 요청 방지
    }
    isDeleting = true;  // 삭제 요청이 시작되면 플래그를 true로 설정

    console.log("delete Selected Topic ID  : ", selectedTopicId);
    if (!selectedTopicId) {
        alert("주제 ID가 없습니다.");
        return;
    }

    if (confirm("deleteTopic 함수 , 정말로 이 주제를 삭제하시겠습니까?")) {
        fetch(`/delete_topic/${selectedTopicId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,  // CSRF 토큰을 가져와 DELETE 요청에 포함
            }
        })
        .then(response => {
            if (response.ok) {
                alert("deleteTopic 함수 , 주제가 삭제되었습니다.");
                window.location.reload();  // 삭제 후 페이지 새로고침
            } else {
                alert("deleteTopic 함수 , 주제 삭제에 실패했습니다.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("오류가 발생했습니다.");
        })

        .finally(() => {
            isDeleting = false;  // 요청이 완료되면 플래그를 다시 false로 설정
        });
    } else {
        isDeleting = false;  // 사용자가 삭제를 취소한 경우 플래그 리셋
    }
    
}

// 대화방 리스트 펼치기/접기 함수
function toggleRoomList(topicId) {
    const roomList = document.getElementById(`${topicId}-rooms`);
    const toggleIcon = document.getElementById(`${topicId}-toggle`);

    // 대화방 리스트가 숨겨져 있으면 펼치고, 아니면 접기
    if (roomList && toggleIcon) {  // 요소가 존재하는지 확인
        if (roomList.style.display === "none") {
            roomList.style.display = "block";
            toggleIcon.innerText = "[접기]";
        } else {
            roomList.style.display = "none";
            toggleIcon.innerText = "[펼치기]";
        }
    } else {
        console.error(`요소를 찾을 수 없습니다: ${topicId}-rooms 또는 ${topicId}-toggle`);
    }            
}

// 선택한 파일을 저장하는 배열
let selectedFiles = [];  // 전역 배열로 선언하여 여러 파일을 저장

// 파일 선택 이벤트 처리
document.getElementById('attached_file').addEventListener('change', function(event) {
    console.log("파일 선택 이벤트 발생");
    console.log("현재 selectedFiles 배열 상태:", selectedFiles);

    const fileInput = document.getElementById('attached_file');
    const files = event.target.files;  // 선택된 파일들
    // 선택한 파일을 배열에 추가
    for (let i = 0; i < files.length; i++) {
        if (!selectedFiles.some(existingFile => existingFile.name === files[i].name)) {
            selectedFiles.push(files[i]);  // 파일 배열에 저장
        }
    }

    // 현재 선택된 파일들 출력
    console.log("현재 선택된 파일 갯수:", selectedFiles.length);
    selectedFiles.forEach((file, index) => {
        console.log(`파일 ${index + 1}: ${file.name}`);
    });
    
    const fileListElement = document.getElementById('file-list');  // 파일 리스트를 표시할 <ul> 요소
    fileListElement.innerHTML = '';  // 이전 파일 목록을 초기화
    

    // 파일이 없을 경우 "첨부된 파일이 없습니다" 메시지 표시
        // 선택한 파일들을 리스트에 추가
        selectedFiles.forEach((file, index) => {
            const listItem = document.createElement('li');  // <li> 요소 생성
            listItem.textContent = `${index + 1}. ${file.name}`;  // 파일 이름 표시
            fileListElement.appendChild(listItem);  // <ul>에 <li> 추가
        });

            // 파일 선택 초기화
    //fileInput.value = "";  // 다시 파일을 선택할 수 있도록 input을 초기화

});

// 주제 생성 시 선택된 파일들을 폼 데이터로 전송
// 주석 처리해서 submit이 동작하는지 확인

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();  // 기본 폼 제출 동작 막기
    const formData = new FormData(this);  // 기존 폼 데이터를 가져와 서버에 전송gkq니다.
    //const formData = new FormData();

    // 선택된 파일들을 FormData에 추가
    if (selectedFiles.length > 0) {  
        //selectedFiles.forEach((file, index) => {
        selectedFiles.forEach((file) => {
            formData.append('attached_file', file);  // 파일을 FormData에 추가
        });
    }

    // 파일을 추가하지 않도록 기존 input 요소를 초기화
    document.getElementById('attached_file').value = "";  // 파일 input 초기화

    // 폼 데이터를 서버로 전송하는 fetch 요청
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'  // CSRF 토큰 추가
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("주제가 성공적으로 생성되었습니다.");
            window.location.href = '/chat';  // /chat 페이지로 리다이렉트
        } else {
            alert("주제 생성 중 오류가 발생했습니다.");
        }
    })
    .catch(error => {
        console.error("주제 생성 오류 발생:", error);
    });
    // 파일 전송이 잘 되는지 콘솔에 확인해볼 수 있습니다.
    console.log(formData.getAll('attached_file'));
});


