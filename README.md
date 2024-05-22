# EduMax-back

EduMax 학원 사이트의 백엔드 코드입니다.

========================================================

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