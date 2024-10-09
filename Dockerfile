# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file into the container at /app
COPY requirements.txt /app/requirements.txt

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . /app

# Step 6: Expose the port that FastAPI will run on
EXPOSE 8500

# Step 7: Set environment variables
ENV MONGO_URI=mongodb://mongo:27017
ENV DB_NAME=mydatabase
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_DB=0

# Step 8: Command to run the application using Uvicorn server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8500", "--reload"]
