FROM python
COPY chatbot.py /
COPY requirements.txt /
RUN pip install pip update
RUN pip install -r requirements.txt
ENV DOCKER_USER = 21415315
ENV DOCKER_PASSWORD = 19940823Hrj_
CMD [ "python", "./chatbot.py" ]
