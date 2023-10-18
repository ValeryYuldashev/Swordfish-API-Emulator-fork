FROM ubuntu:latest AS SetupFiles

# For healthcheck
RUN apt-get update && apt-get install bash git openssl -y

RUN git clone https://github.com/ValeryYuldashev/Swordfish-API-Emulator-fork



RUN /bin/bash -c 'openssl genrsa -out Swordfish-API-Emulator-fork/server.key 2048'

RUN /bin/bash -c 'openssl req -new -key Swordfish-API-Emulator-fork/server.key -out Swordfish-API-Emulator-fork/server.csr -config Swordfish-API-Emulator-fork/certificate_config.cnf'

RUN /bin/bash -c 'openssl x509 -in Swordfish-API-Emulator-fork/server.csr -out Swordfish-API-Emulator-fork/server.crt -req -signkey Swordfish-API-Emulator-fork/server.key -days 365 -extfile Swordfish-API-Emulator-fork/v3.ext'

FROM python:3-slim

# For healthcheck
RUN apt-get update && apt-get install curl -y

# Copy server files
COPY --from=SetupFiles /Swordfish-API-Emulator-fork /usr/src/app/.

# Install python requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt

# Env settings
EXPOSE 5000
HEALTHCHECK CMD curl --fail http://127.0.0.1:5000/redfish/v1/ || exit 1
WORKDIR /usr/src/app
ENTRYPOINT ["python", "emulator.py"]
