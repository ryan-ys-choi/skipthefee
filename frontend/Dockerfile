FROM node:18-alpine

WORKDIR /app

COPY package*.json .

RUN npm install -g serve

COPY build/ ./build/

ARG REACT_APP_API_URL

ENV REACT_APP_API_URL=$REACT_APP_API_URL

CMD ["serve", "-s", "build", "-l", "3000"]

