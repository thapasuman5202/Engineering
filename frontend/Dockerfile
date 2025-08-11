FROM node:18-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY frontend ./frontend
RUN corepack enable && pnpm install --frozen-lockfile
RUN pnpm --filter frontend build
EXPOSE 5173
CMD ["pnpm", "--filter", "frontend", "dev", "--", "--host"]
