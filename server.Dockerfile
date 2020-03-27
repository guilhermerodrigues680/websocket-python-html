FROM python:3.7-slim-buster
# Cria o diretorio da aplicacao
WORKDIR /usr/src/app

# Copia o requirements.txt e instala as dependencias da aplicacao
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copia o projeto backend
COPY ./src/python ./

# Definindo comando padrao do container para iniciar a aplicacao.
CMD python3 main.py