FROM python:3.10.11-alpine
RUN mkdir /app 
COPY pyproject.toml /app 
WORKDIR /app
ENV POETRY_VERSION=1.4.2
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY . /app
ENTRYPOINT ["poetry", "run", "python3", "PoGoDnIk.py"]
