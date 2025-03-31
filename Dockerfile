# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container to /backend
WORKDIR /backend

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code into the container
COPY . .

# Command to run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]