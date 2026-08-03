FROM python:3.11-slim

WORKDIR /app

# Copy the entire project
COPY . .

# Install API dependencies
RUN pip install --no-cache-dir -r api/requirements.txt

# Install the project as a package
RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]