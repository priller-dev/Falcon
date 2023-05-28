FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV MYPATH=/home/app/code
RUN apk add --update py-pip
RUN apk add gcc python3-dev

WORKDIR $MYPATH
COPY requirements.txt $MYPATH
RUN pip install -r requirements.txt
COPY . $MYPATH
#RUN python manage.py collectstatic --noinput