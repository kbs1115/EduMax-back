# EduMax-back

EduMax 학원 사이트의 백엔드 코드입니다.
사이트 방문을 원하시면 [여기](https://edumax-kr.com/)를 클릭해주세요.

### 사이트 화면


![image](https://github.com/user-attachments/assets/d756ffe1-b4e9-43af-a04f-534b5ba36bc3)
![image](https://github.com/user-attachments/assets/61c3f621-707b-45a6-b0d3-3de63e08387d)
![image](https://github.com/user-attachments/assets/42fdbb04-1f7d-4255-91b8-dabc07d3fead)
![image](https://github.com/user-attachments/assets/111e9f6c-4a9b-4ffd-a6b1-e64a5aa9ae2a)
![image](https://github.com/user-attachments/assets/19af700c-bb98-4404-9db9-7b25503f5efa)

### 로컬 서버 구동 순서

1. **Redis를 다운로드 받지 않았다면 다음 사이트에서 다운로드 받습니다.**

    - [Redis 다운로드](https://github.com/microsoftarchive/redis/releases)


2. **Redis 설치 후 관리자 모드로 Shell 실행 후 다음 명령어 입력**

   ```sh
   cd "C:\Program Files\Redis"  # (다운받은 위치가 다르다면 조정)
   redis-server.exe redis.windows.conf

3. **셀러리 worker 등록(Windows)**

   ```sh
   cd [프로젝트 루트 디렉토리]
   celery -A config worker -P solo -l INFO

4. **Django 로컬 서버 실행**

   ```sh
   python manage.py runserver --settings=config.settings.local
