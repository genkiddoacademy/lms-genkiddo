# Dockerfile
FROM frappe/bench:latest

# Install wkhtmltopdf dan dependencies
USER root
RUN apt-get update && apt-get install -y \
    xvfb libfontconfig wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb || apt-get -f install -y \
    && rm wkhtmltox_0.12.6-1.buster_amd64.deb
