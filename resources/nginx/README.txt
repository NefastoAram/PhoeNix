
# Nginx Installation and Configuration Instructions for System Monitor

## 1. Install Nginx
sudo apt update
sudo apt install nginx

## 2. Start and Enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

## 3. Configure Reverse Proxy and Static Files
Create or edit the configuration file:

sudo nano /etc/nginx/sites-available/phoenix

Insert:

server {
    listen 80;
    server_name _;

    # Serve the web directory as static files
    location / {
        root /.../phoenix;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Reverse proxy for Flask API
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

## 4. Enable the Configuration
sudo ln -s /etc/nginx/sites-available/phoenix /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

## Notes
- Access http://<server-ip>/ for the web page
- Requests to /api/status are forwarded to the Flask backend
- Edit the paths if you change the directory structure
