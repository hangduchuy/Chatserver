# Chat Server 

    Using Django & sql3 | Chat Server

# Description

    Ứng dụng Chat Server bằng Python

# Cách tải các framework và thư viên

    pip install -r requirements.txt

    pip install --upgrade -r requirements.txt

    
# Resource SQL:
- Nếu sử dụng sqlite:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

- Nếu sử dụng mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost', 
        '
    }
}
- Nếu sử dụng sql server
DATABASES = {
'default': {
    'NAME': 'my_database',
    'ENGINE': 'sqlserver_ado',   # Không thay đổi trường này
    'HOST': 'dbserver\\ss2012',
    'USER': '',
    'PASSWORD': '',
 }
}

   python manager.py makemigrations chat
   python manager.py migrate


#Redis
   Tải redis đã đính kèm với tệp

#Chạy server
   python manage.py runsever (trong thư mục src)
   

	
    