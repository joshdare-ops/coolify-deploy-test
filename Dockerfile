FROM python:3.13-alpine

WORKDIR /app
RUN adduser -D -H app
COPY server.py .
USER app

EXPOSE 8080
CMD ["python", "-u", "server.py"]
