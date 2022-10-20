ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache nodejs npm

RUN mkdir -p /app

WORKDIR /app

COPY package.json  /app

RUN npm install

COPY . /app

EXPOSE 3000

CMD ["npm", "start"]


