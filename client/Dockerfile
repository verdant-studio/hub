FROM node:20

RUN npm install -g serve

WORKDIR /app

COPY ./package*.json ./

RUN npm install

COPY . .

# Accept build-time argument
ARG VITE_API_URL

# Make it available as an env var
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]