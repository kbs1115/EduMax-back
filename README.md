# EduMax-back

EduMax 학원 사이트의 백엔드 코드입니다.
사이트 방문을 원하시면 [여기](https://edumax-kr.com/)를 클릭해주세요.

### 사이트 화면
<img src="https://github.com/user-attachments/assets/d495be50-c65b-46e6-acbe-bb77f3bf5172" alt="image" width="600">
<img src="https://github.com/user-attachments/assets/9ad9ad76-ae4d-4bf3-8463-16649a31ddad" alt="image" width="600">
<img src="https://github.com/user-attachments/assets/beaed14d-80c8-4641-b7ca-f3d73ec4fbb3" alt="image" width="600">
<img src="https://github.com/user-attachments/assets/2771e08d-0afb-4f33-8b15-5bf1cabac016" alt="image" width="500">


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
