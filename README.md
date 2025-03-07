# Server

## 실행 방법

1. 프로젝트 루트 디렉토리에 `.env` 파일을 생성한다.
   ```
   # .env
   # Database
   MYSQL_ROOT_PASSWORD=your_root_password
   MYSQL_DATABASE=finflow
   DB_URL=mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@db:3306/${MYSQL_DATABASE}

   # JWT Settings
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
2. 프로젝트 루트 디렉토리에서 다음 명령어를 실행하여 컨테이너를 빌드하고 실행한다.
   ```
   docker-compose up -d
   ```
3. 컨테이너의 로그를 확인하려면 다음 명령어를 치면 된다.
   ```
   docker-compose logs -f
   ```
4. 모든 컨테이너를 종료하려면, 루트 디렉토리에서 다음 명령어를 치면 된다.
   ```
   docker-compose down
   ```