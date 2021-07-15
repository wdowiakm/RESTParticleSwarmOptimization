FROM python:3

RUN pip install Flask
RUN pip install requests

WORKDIR ./app

ENV SYS_APP_HOST 0.0.0.0
ENV SYS_APP_PORT 35100

COPY ./templates ./templates
COPY ./Model ./Model
COPY ./app_pso_stateless.py ./app_pso_stateless.py

ENTRYPOINT ["python3", "app_pso_stateless.py"]