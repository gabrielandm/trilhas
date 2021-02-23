FROM python:3.9.1

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     unixodbc-dev \
#     unixodbc \
#     libpq-dev 

# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
#     curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
#     apt-get update && \
#     ACCEPT_EULA=Y apt-get install msodbcsql17 && \
#     ACCEPT_EULA=Y apt-get install mssql-tools && \
#     echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile && \
#     echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
#     # /bin/bash source ~/.bashrc && \
#     apt-get install -y unixodbc-dev

RUN pip install sqlalchemy Flask PyMySQL

COPY projeto-04-crud-py-docker.py .

CMD [ "python", "./projeto-04-crud-py-docker.py" ]
