FROM node:lts-alpine AS build
WORKDIR /app
COPY . .
RUN npm i
RUN npm run build

FROM node:lts AS dev
WORKDIR /app
COPY . .
RUN npm i
EXPOSE 4321
CMD npm run dev -- --host

FROM httpd:2-alpine AS runtime
COPY --from=build /app/dist /usr/local/apache2/htdocs/
RUN sed -i 's/Listen 80/Listen 4321/g' /usr/local/apache2/conf/httpd.conf
EXPOSE 4321
