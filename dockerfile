FROM python:3.7

COPY /yolov5 /app
WORKDIR /app
RUN python print(os.listdir())