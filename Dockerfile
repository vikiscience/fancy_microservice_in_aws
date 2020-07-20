FROM python:3.7.3-stretch

ENV app_name=fancy_app
ENV port=8080

## Step 1:
# Create a working directory
RUN mkdir /home/$app_name
WORKDIR /home/$app_name

## Step 2:
# Copy source code to working directory
COPY . /home/$app_name

## Step 3:
# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

## Step 4:
# Expose the port
EXPOSE $port

## Step 5:
# Run app.py at container launch
CMD ["python", "app.py"]
