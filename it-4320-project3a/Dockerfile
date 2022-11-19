FROM python:3.7-alpine
WORKDIR /project
COPY requirements.txt requirements.txt
RUN apk --no-cache add musl-dev linux-headers g++
RUN pip install --upgrade pip
RUN pip install numpy && \
    pip install pandas
RUN pip install -r requirements.txt
CMD ["python","-u","wsgi.py"]
