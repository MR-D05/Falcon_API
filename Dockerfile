FROM python:3.6.2
RUN apt-get update && apt-get -y install default-jre unzip socat
RUN wget https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/5.0.2/flyway-commandline-5.0.2-linux-x64.tar.gz && tar -xf flyway-commandline-5.0.2-linux-x64.tar.gz -C /opt && chmod a+x /opt/flyway-5.0.2/flyway
ENV PATH $PATH:/opt/flyway-5.0.2
ADD ./sql /opt/flyway-5.0.2/sql/
ADD . /src/
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 5000