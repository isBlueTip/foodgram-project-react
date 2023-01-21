FROM node:15.13.0-alpine

RUN mkdir /app

COPY ./ /app
WORKDIR /app

RUN npm run build



  frontend:
    build:
      context: ./frontend
    volumes:
      - frontend_build:/app/build
    depends_on:
      - backend
    env_file:
      - ./.env