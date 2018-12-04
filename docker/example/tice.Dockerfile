FROM tice.env:1.0
WORKDIR /usr/local/tice
COPY tice ./
RUN mkdir logs \
    && chmod 777 logs \
    && ln -s /usr/local/tice/tice.conf /usr/local/nginx/conf/include/tice.conf \
    && rm -rf /usr/local/nginx/conf/nginx.conf \
    && mv nginx.conf /usr/local/nginx/conf/ \
    && chmod 777 /usr/local/nginx/conf/nginx.conf
EXPOSE 8081
ENTRYPOINT [ "sh", "bootstrap.sh" ]