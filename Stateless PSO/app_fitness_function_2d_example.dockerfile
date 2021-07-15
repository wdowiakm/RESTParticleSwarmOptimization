FROM python:3

RUN pip install Flask
RUN pip install requests

WORKDIR ./app

ENV SYS_APP_HOST 0.0.0.0
ENV SYS_APP_PORT 35200
ENV PSO_MAIN_URL="http://host.docker.internal:35100/fitnessFunctionResult"
ENV FLASK_ENV=production

COPY ./Model/Particle.py ./Model/Particle.py
COPY ./app_fitness_function_2d_example.py ./app_fitness_function_2d_example.py

ENTRYPOINT ["python3", "app_fitness_function_2d_example.py"]