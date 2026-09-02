FROM nginx:alpine

ARG SSL_DAYS=365
ARG BASE_SUBJECT="/C=JP/ST=Origami/L=Layer/O=ValleyMountain/OU=StackGeometry"

RUN apk add --no-cache openssl

COPY nginx/rebuild-certs.sh /usr/local/bin/rebuild-certs.sh
RUN chmod +x /usr/local/bin/rebuild-certs.sh

# Generate certificates at build time
RUN SSL_DAYS=${SSL_DAYS} SSL_SUBJECT=${SSL_SUBJECT} /usr/local/bin/rebuild-certs.sh

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
