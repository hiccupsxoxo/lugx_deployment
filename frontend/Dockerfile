# Use the official Nginx image
FROM nginx:alpine

# Remove the default Nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy your Lugx website into Nginx folder
COPY . /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80
