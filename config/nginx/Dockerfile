# Use the official Nginx image from Docker Hub
FROM nginx:1.23.3

# Copy the custom Nginx configuration file into the image
COPY config/nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
