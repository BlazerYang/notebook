FROM r.bingo.soft.dummy.mail/library/nodejs-8-el7:latest
RUN npm install -g mock-json-server --registry=http://registry.npm.taobao.org
WORKDIR /home/q/system/json_mock
COPY data.json .
EXPOSE 8082
ENTRYPOINT [ "/usr/local/node/bin/mock-json-server" ,"data.json", "--port=8082"]