FROM python:3.13-slim

WORKDIR /app
RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* /app/
RUN uv pip install --system -e .

COPY . /app

EXPOSE 8081
CMD ["chainlit", "run", "/app/app.py", "--host", "0.0.0.0", "--port", "8081"]
