# Use an official slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

## Install PyTorch CPU only version
RUN pip3 install --no-cache-dir torch~=2.5.1 --index-url https://download.pytorch.org/whl/cpu

# Copy and install only requirements
COPY requirements.txt .

## Install Rest of the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Expose Prometheus metrics port
EXPOSE 8001

# Run the Streamlit app
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
