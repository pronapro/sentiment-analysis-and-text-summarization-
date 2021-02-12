# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code
#ADD . /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt
EXPOSE 5000

ADD . /code


# Step 6: Expose the port Flask is running on
EXPOSE 5000

# Step 9: Run Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]