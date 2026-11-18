# The project's frontend image: builds this app and serves it from nginx,
# which also proxies /api/ to the backend container (nginx.conf, the same
# file the platform's frontend image uses). Build context is frontend/.
#
# The build installs platform-common from GitHub (package.json pins the
# platform release tag), so the build machine needs read access to the
# Savic-Platform repository. VITE_API_BASE_URL stays empty: the browser
# calls /api/... on the address it loaded the page from.

FROM --platform=$BUILDPLATFORM node:22.23.4-alpine3.24 AS build
RUN apk add --no-cache git && npm install -g pnpm@11.24.0
WORKDIR /app
COPY package.json pnpm-lock.yaml* pnpm-workspace.yaml ./
RUN pnpm install
COPY . .
ENV VITE_API_BASE_URL=""
RUN pnpm build


FROM nginxinc/nginx-unprivileged:1.30.6-alpine3.24 AS prod
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
