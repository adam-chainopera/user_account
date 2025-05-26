FROM python:3.10-slim

# set workdir
WORKDIR /app

# set env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# copy requirements
COPY requirements.txt .

# install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY . .

# create wallets dir
RUN mkdir -p wallets

# expose port
EXPOSE 8000

# use gunicorn to start app
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"] 