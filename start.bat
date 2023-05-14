pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
cd design
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000