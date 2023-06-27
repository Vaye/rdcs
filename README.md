# rdcs
## Features
This is a service used to reduce the dimensionality of a series of network elements' Key Performance Indicators (KPIs) and perform anomaly detection. It outputs records of anomalous network elements and some related graphs to provide a more intuitive assessment of specific abnormal KPIs.<br>
## Directory Structure
app_main: Service Entry and Sub-Service Invocation Logic<br>
app_rd: Dimensionality reduction service<br>
app_cl: Clustering and Outlier Identification Service<br>
app_plot: Service for drawing dimensionality reduction diagrams and abnormal KPI diagrams<br>
common: common functions<br>
models: Scaler and Autoencoder model<br>
compose: docker compose files<br>
test: files for service testing<br>
## Installation
build 4images for each service:  
    docker build -t app_main:0.8 -f app_main/Dockerfile .<br>
    '   docker build -t app_rd:0.8 -f app_rd/Dockerfile .'<br>
    '   docker build -t app_cl:0.5 -f app_cl/Dockerfile .'<br>
    '   docker build -t app_plot:0.5 -f app_plot/Dockerfile .  '<br>

