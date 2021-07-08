FROM python:3

RUN pip install Flask
RUN pip install requests

WORKDIR ./app

ENV SYS_APP_HOST 0.0.0.0
ENV SYS_APP_PORT 35100
ENV FITFUN_URL 'http://host.docker.internal:35200/calcFitFun'
ENV NOVARIABLES 2
ENV NOPARTICLE 25
ENV MAXITERATION 50
ENV FITFUNTOLERANCE 1e-6
ENV MAXSTALLITERATIONS 20
ENV WEIGHTSELF 1.49
ENV WEIGHTSOCIAL 1.49
ENV WEIGHTINERTIA 0.99
ENV LEARNINGRATE 0.1
ENV FLASK_ENV=production

COPY ./templates ./templates
COPY ./Pso.py ./Pso.py
COPY ./PsoConfig.py ./PsoConfig.py
COPY ./PsoParticle.py ./PsoParticle.py
COPY ./PsoState.py ./PsoState.py

COPY ./pso_app.py ./pso_app.py

ENTRYPOINT ["python3", "pso_app.py"]