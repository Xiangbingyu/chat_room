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