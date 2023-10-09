FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app

COPY withpython.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

CMD ["python","/app/withpython.py"]
