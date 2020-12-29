FROM node:15-alpine as node
RUN mkdir -p /frontend/angular
WORKDIR /frontend/angular
COPY ./angular/package*.json ./
RUN npm install
COPY ./angular .
