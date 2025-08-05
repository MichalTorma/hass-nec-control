# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install required packages
RUN apk add --no-cache \
    python3 \
    py3-pip

# Copy root filesystem
COPY rootfs /

# Make Python service executable
RUN chmod +x /usr/bin/nec_tv_service.py

# Ensure service scripts are executable
RUN chmod +x /etc/services.d/hass-nec-control/run \
    && chmod +x /etc/services.d/hass-nec-control/finish
