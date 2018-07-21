FROM node

WORKDIR /var/lib/hypothesis-client

# ENV NODE_ENV production

EXPOSE 3001

ENV SIDEBAR_APP_URL http://localhost:5000/app.html

COPY . .

# ENV PATH /var/lib/hypothesis-client/bin:$PATH

RUN npm install -g gulp-cli

RUN npm install gulp-cli

RUN make

ENTRYPOINT ["gulp", "watch"]
