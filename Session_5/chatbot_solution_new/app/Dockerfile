# Stage 1: Build stage
FROM python:3.11-slim AS build-stage

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 libsqlite3-dev \
    curl \
    && apt-get clean

# Copy the requirements file
COPY requirements.lock /app/

# Install Python dependencies in the build stage
RUN pip install --no-cache-dir -r requirements.lock

# Copy the application code to the build stage
COPY . /app

# Stage 2: Final stage (runtime environment)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 libsqlite3-dev \
    curl \
    && apt-get clean

# Copy the installed Python packages from the build stage to the final image
COPY --from=build-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build-stage /usr/local/bin /usr/local/bin

# Copy the application code from the build stage
COPY --from=build-stage /app /app

# Install uvicorn in the final stage
RUN pip install --no-cache-dir uvicorn

# Expose the FastAPI default port
EXPOSE 8501

# # Start the FastAPI application using uvicorn with autoreload
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
