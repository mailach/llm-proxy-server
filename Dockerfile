FROM python:3.9
RUN mkdir /app
WORKDIR /app
ADD . /app
RUN  pip install -r core/requirements.txt  
EXPOSE 5000
RUN chmod +x /app/init/init_app.sh /app/init/init_app_dev.sh


ENTRYPOINT ["/app/init/init_app.sh"]