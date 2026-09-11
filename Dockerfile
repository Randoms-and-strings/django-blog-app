FROM python:3.14-alpine
WORKDIR /blog-app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m pip uninstall -y elastic-transport elasticsearch || true && python -m pip install --no-cache-dir "elasticsearch==7.17.13" "urllib3==1.26.16"
COPY . .
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
