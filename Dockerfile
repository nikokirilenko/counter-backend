FROM python:3.9
RUN mkdir -p /opt/counter-backend
WORKDIR /opt/counter-backend
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]