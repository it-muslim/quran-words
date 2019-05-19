FROM node:11-alpine as node
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./angular/package*.json ./
RUN npm install
COPY ./angular .
