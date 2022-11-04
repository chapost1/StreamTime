FROM debian:11

SHELL [ "/bin/bash", "-l", "-c" ]

WORKDIR /var/ng/project

RUN apt-get update && apt-get install -y curl
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
RUN source ~/.profile
RUN nvm install 18.12.0
RUN nvm use 18.12.0
RUN npm install -g @angular/cli@14.2.8
ENV NG_CLI_ANALYTICS=false
RUN ng version

COPY /code /var/ng/project

RUN ng build

RUN mv /var/ng/project/dist /var/ng/dist

WORKDIR /var/ng

RUN rm -rf /var/ng/project
RUN mv /var/ng/dist/* /var/ng/
RUN rm -rf /var/ng/dist

CMD tialf /dev/null