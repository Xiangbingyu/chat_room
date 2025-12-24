# 配置环境
```bash
conda create -n chat_room_django python=3.10
conda activate chat_room_django
cd backend/Python/chat_room_backend_django
pip install -r requirements.txt
```

# 启动项目
```bash
python manage.py runserver
```

# 创建项目/应用
```bash
django-admin startproject myproject
python manage.py startapp hallo_world
```

# 迁移应用数据库
```bash
python manage.py makemigrations
python manage.py migrate
```

# 数据库操作
```bash
sqlite3 db.sqlite3

.tables
.schema admin_analysis_records
.schema short_term_memories
.schema conversation_histories
.schema long_term_memories

SELECT * FROM admin_analysis_records;
SELECT * FROM short_term_memories;
SELECT * FROM conversation_histories;
SELECT * FROM long_term_memories;
```