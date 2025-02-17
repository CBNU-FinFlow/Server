# Server

## 폴더 구조

```
.
├── .env                # 환경변수 파일
├── app
│   ├── core
│   │   ├── config.py
│   │   └── security.py
│   ├── db
│   │   └── database.py
│   ├── main.py
│   ├── models
│   │   └── user.py
│   ├── routers
│   │   └── users.py
│   └── schemas
│       └── user.py
└── requirements.txt
```

## 실행 방법

1. 필요한 라이브러리를 설치한다.
   ```
   pip install -r requirements.txt
   ```
2. 서버를 실행한다.
   ```
   uvicorn app.main:app --reload
   ```

```
Server
├─ Dump20250205
│  ├─ finflow_financial_products.sql
│  └─ finflow_sectors.sql
├─ README.md
├─ app
│  ├─ core
│  │  ├─ config.py
│  │  └─ security.py
│  ├─ db
│  │  └─ database.py
│  ├─ main.py
│  ├─ models
│  │  ├─ financial_product.py
│  │  ├─ portfolio.py
│  │  ├─ sector.py
│  │  └─ user.py
│  ├─ routers
│  │  └─ users.py
│  └─ schemas
│     └─ user.py
└─ requirements.txt

```
