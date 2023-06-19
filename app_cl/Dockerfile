FROM python:3.9.16-bullseye

COPY app_cl/ /app
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ADD common /app
WORKDIR /app
# ENV PATH="/home/ai/.local/bin:${PATH}"
EXPOSE 5002
CMD ["gunicorn", "app_cl:app", "--bind", "0.0.0.0:5002", "--workers", "3", "--threads", "2", "--timeout", "120", "--reload"]