FROM mongo:latest
ENV MONGO_INITDB_ROOT_USERNAME root
ENV MONGO_INITDB_ROOT_PASSWORD pass
ENV MONGO_INITDB_DATABASE admin

# such a script could be used to modify db when first initialized
#ADD mongo-init.js /docker-entrypoint-initdb.d/
COPY seed.js /docker-entrypoint-initdb.d
