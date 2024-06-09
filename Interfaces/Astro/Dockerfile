FROM node:lts-alpine AS build
WORKDIR /app
COPY . .
RUN npm i
RUN npm run build

FROM httpd:2-alpine AS runtime
COPY --from=build /app/dist /usr/local/apache2/htdocs/
EXPOSE 80