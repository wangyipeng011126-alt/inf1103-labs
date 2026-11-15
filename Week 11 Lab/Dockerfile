FROM python:3.11-slim

WORKDIR /usr/src/app

# Copy EVERYTHING from your local folder (main.py, product.py, test_lab8.py, etc.)
COPY . .

# Install pytest so you can run your tests inside Docker
RUN pip install pytest

# Default command runs your main program
CMD ["python", "main.py"]