FROM python:3.10-alpine
RUN mkdir /app 
COPY pyproject.toml /app 
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . /app
ENTRYPOINT ["poetry", "run", "python3", "PoGoDnIk.py"]
