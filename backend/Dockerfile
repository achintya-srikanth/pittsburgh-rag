# 1. Use a lightweight Python base image
FROM python:3.10-slim

# 2. Prevent Python from writing .pyc files to disc (good for containers)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy the requirements file into the container
COPY requirements.txt .

# 5. Install dependencies
# --no-cache-dir keeps the image small by removing installation cache
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your application code
COPY . .

# 7. Command to run the app
# host 0.0.0.0 is crucial! It allows access from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]