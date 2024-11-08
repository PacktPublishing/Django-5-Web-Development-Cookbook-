#!/bin/sh

# Use envsubst to substitute environment variables in the NGINX config template
envsubst '$VIRTUAL_HOST' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Execute NGINX
exec nginx -g 'daemon off;'
