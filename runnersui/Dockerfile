ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache nodejs npm

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY package.json /usr/src/app

RUN npm install

COPY . /usr/src/app

EXPOSE 4200

CMD ["npm", "start"]

