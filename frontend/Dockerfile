FROM node:18-alpine
WORKDIR /app
COPY package.json tsconfig.json vite.config.ts tailwind.config.js postcss.config.js ./
RUN npm install
COPY src ./src
RUN npm run build
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
