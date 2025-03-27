### 확인해야 할 사항
client.py만 웹캠 컴퓨터에서 돌아가고, 나머지는 서버 컴퓨터에서 돌아감.<br>
client.py 실행 컴퓨터(클라이언트)는 웹캠이 필요함.<br>
client.py 코드의 B_IP에는 실제 서버 컴퓨터의 IP를 입력할 것.<br>
<br><br>
서버 컴퓨터에는 8000 포트가 열려있어야 함. ->cmd를 관리자 권한으로 실행하고 아래 명령어 입력하기.
```
netsh advfirewall firewall add rule name="FastAPI 8000" dir=in action=allow protocol=TCP localport=8000
```
서버 컴퓨터에는 mysql이 설치되어 있어야 함. 테스트로 사용한 방법은 아래와 같음.
```
CREATE DATABASE yolo_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE yolo_project;
CREATE TABLE captures (
    filename VARCHAR(255) PRIMARY KEY,
    path VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
DB 연결 시
```
# db.py
DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/yolo_project"
```
root: 사용자명<br>
1234: 비밀번호<br>
localhost: MySQL 서버 주소 (현재 로컬)<br>
3306: 기본 포트<br>
yolo_project: 사용할 DB 이름<br>
<br><br>
yolo 모델은 yolo.py로 만들어서 사용.<br>
<br><br>
images/ 폴더 생성하기
<br><br>
실행 방법<br>
컴퓨터 2대 사용 시<br>
카메라 역할만 하는 컴퓨터에서 
```
python client.py
```
서버 역할하는 컴퓨터에서
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
<br><br>
컴퓨터 1대만 사용 시
```
python webcam_main.py
```
