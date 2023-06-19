FROM python:3.9.16-bullseye

COPY app_main/ /app
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ADD common /app
WORKDIR /app
# ENV PATH="/home/ai/.local/bin:${PATH}"
EXPOSE 4999
CMD ["gunicorn", "app_main:app", "--bind", "0.0.0.0:4999", "--workers", "3", "--threads", "2", "--timeout", "120", "--reload"]
# CMD ["python", "-u", "app_main.py"]