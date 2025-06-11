### pgvector를 사용하기 위한 확장 설치 필요!

일단
`https://github.com/andreiramani/pgvector_pgsql_windows?tab=readme-ov-file`
여기서 찾은 걸로 추가했더니 잘 됐음.




### 실행 순서

1. db_manager.py 실행
2. main.py 실행
3. localhost:8000/run-yolo로 실행 확인.




## docker 실행

### 1. image 빌드하기 전
- yolo_door 폴더에 영상 맞게 넣어줘야 함. (이름 맞추는 것 유의)
- video_processor.py 코드 안에 PASSWORD 변수에 앱 비밀번호 넣어줘야 함.

### 2. docker image 빌드하고 실행
실행 명령어
`docker run -d -p 8000:8000`


###
현재 문제
db에 전송이 안 되는 것 같음