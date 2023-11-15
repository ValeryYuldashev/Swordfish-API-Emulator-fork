FROM ubuntu:latest AS SetupFiles

# For healthcheck
RUN apt-get update && apt-get install bash git openssl -y

RUN git clone https://github.com/xenob8/demo-Swordfish-API-Emulator


FROM python:3-slim

# For healthcheck
RUN apt-get update && apt-get install curl -y

# Copy server files
COPY --from=SetupFiles /demo-Swordfish-API-Emulator /usr/src/app/.

# Install python requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt

# Env settings
EXPOSE 5000
HEALTHCHECK CMD curl --fail http://127.0.0.1:5000/redfish/v1/ || exit 1
WORKDIR /usr/src/app
ENTRYPOINT ["python", "emulator.py"]
