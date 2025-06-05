# Fetching the latest nginx image
FROM nginx:1.27.0-alpine

# Removing default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Copying our nginx.conf
COPY nginx.conf /etc/nginx/conf.d