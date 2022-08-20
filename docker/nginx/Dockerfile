FROM nginx:alpine
ARG project_env
# nginx conf
ADD ./docker/nginx/$project_env/django.conf /etc/nginx/sites-enabled/default
ADD ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./backend/ /app/backend
EXPOSE 80 443

