FROM node:19.5.0-alpine
# added latest code branch 
# install simple http server for serving static content
RUN npm install -g http-server
# make the 'app' folder the current working directory
#RUN cd ./vertigo/app/client
WORKDIR /app/client
# copy 'package.json' to install dependencies
COPY /app/client/package*.json ./
# install dependencies
RUN npm install 
# copy files and folders to the current working directory (i.e. 'app' folder)
COPY . .
# build app for production with minification
RUN npm run build
EXPOSE 8080
CMD [ "http-server","dist"]

