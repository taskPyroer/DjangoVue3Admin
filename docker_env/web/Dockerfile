FROM node:16-buster-slim as frontend-builder
WORKDIR /web/
COPY web/. .
RUN npm install -g pnpm && \
    pnpm install --frozen-lockfile
RUN pnpm run build

# 构建 Nginx 镜像，将前端项目复制到镜像中
FROM nginx:alpine
COPY ./docker_env/nginx/my.conf /etc/nginx/conf.d/my.conf
COPY --from=frontend-builder /web/dist /usr/share/nginx/html