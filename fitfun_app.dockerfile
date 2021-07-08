FROM python:3

RUN pip install Flask
RUN pip install requests

WORKDIR ./app

ENV SYS_APP_HOST 0.0.0.0
ENV SYS_APP_PORT 35200
ENV PSO_MAIN_URL="http://host.docker.internal:35100/fitFunRes"
ENV FLASK_ENV=production

COPY ./PsoParticle.py ./PsoParticle.py

COPY ./fitfun_app.py ./fitfun_app.py

ENTRYPOINT ["python3", "fitfun_app.py"]