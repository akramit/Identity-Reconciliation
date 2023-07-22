# Use the official Python image as the base image
FROM python:3.11
COPY . .

# Set the working directory inside the container
# WORKDIR /app

# Copy the current directory contents (including app.py) to the container's working directory
#COPY identity_app /app
#COPY requirements.txt /app
# COPY init.sql /app
#COPY init.sql /docker-entrypoint-initdb.d/
# Install any dependencies your Python app requires (if needed)
# For example, if you have a requirements.txt file, you can use:
#RUN pip3 install -r requirements.txt


# Specify the command to run your Python app
# EXPOSE 5000
RUN pip3 install -r requirements.txt
CMD ["python", "identity_app/app.py"]
