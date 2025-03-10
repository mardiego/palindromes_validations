# Use Python 3.11 as a base image
FROM python:3.11-slim

# Install SQLite3 system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set up environment variables to ensure the virtual environment is used
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install the Python virtual environment package
RUN python3 -m venv /env

# Activate the virtual environment and install dependencies
RUN /env/bin/pip install fastapi==0.95.0
RUN /env/bin/pip install uvicorn==0.22.0
RUN /env/bin/pip install requests

# Create the SQLite database file and the 'jobs' table using SQLite commands
RUN sqlite3 /app/palindromes.db "CREATE TABLE IF NOT EXISTS jobs (string TEXT, language TEXT);"

# Expose port 8080
EXPOSE 8080

# Set environment variable to use the virtual environment
ENV VIRTUAL_ENV=/env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Run your FastAPI app using uvicorn (for example, if your app is in 'app.py')
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
