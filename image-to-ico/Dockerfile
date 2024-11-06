FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY Image-to-ico.py .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir output

EXPOSE 7860

ENV PYTHONUNBUFFERED=1

CMD ["python", "Image-to-ico.py"]