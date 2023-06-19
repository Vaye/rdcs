FROM python:3.9.16-bullseye

COPY app_rd/ /app
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# ADD common /app
WORKDIR /app
# ENV PATH="/home/ai/.local/bin:${PATH}"
EXPOSE 5001
CMD ["gunicorn", "app_rd:app", "--bind", "0.0.0.0:5001", "--workers", "3", "--threads", "2", "--timeout", "120", "--reload"]