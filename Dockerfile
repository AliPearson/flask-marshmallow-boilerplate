# creates alpine linux sandbox
FROM alpine:3.14
# "brew upgrade" for alpine linux, updates all the packages in alpine
RUN apk update && apk upgrade
# "brew install sqlite" for alpine linux
RUN apk add --no-cache sqlite
FROM python:3.11 as python-base
RUN mkdir /app 
RUN mkdir /app/tests
WORKDIR /app
COPY pyproject.toml /app 
COPY app.py /app
COPY wrapsql.py /app
COPY calculation.py /app
COPY computations.db /app
COPY tests /app
COPY README.md /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
# RUN poetry init
# RUN poetry add flask
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN poetry run python -m pytest
EXPOSE 8080
CMD ["poetry", "run", "python", "app.py", "--host=0.0.0.0", "--port=8080"]
#CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8080"]



# COPY /app /app
