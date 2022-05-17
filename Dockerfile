FROM ubuntu:latest

# Install packages
RUN apt-get update && apt-get install -y build-essential openjdk-18-jdk git-core python3-dev python3-pip

# Copy contents of repository to container
COPY . /src

# Set work directory in container
WORKDIR /src

# Install Python dependencies
RUN pip install -e .

ENTRYPOINT ["/bin/bash"]
