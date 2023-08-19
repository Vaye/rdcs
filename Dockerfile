FROM python:3.9.16-bullseye

# Set work directory
WORKDIR /app

# Install supervisord
RUN apt-get update && apt-get install -y supervisor vim nano curl wget netcat traceroute iputils-ping net-tools

# Copy all the apps to the container
COPY app_main/ /app/app_main
COPY app_rd/ /app/app_rd
COPY app_cl/ /app/app_cl
COPY app_plot/ /app/app_plot

# Combine the requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy common files to each app directory
ADD common /app/app_main
ADD common /app/app_rd
ADD common /app/app_cl
ADD common /app/app_plot

# Copy supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the port the app_main runs on
EXPOSE 4999

# Run supervisord
CMD ["/usr/bin/supervisord"]
