FROM node:22-bookworm-slim AS build
WORKDIR /app/web
ENV HUSKY=0 NEXT_TELEMETRY_DISABLED=1

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY . .
RUN BUILD_STANDALONE=1 pnpm build

FROM node:22-bookworm-slim AS runtime
WORKDIR /app/web
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1 HOSTNAME=0.0.0.0 PORT=3000

COPY --from=build --chown=node:node /app/web/.next/standalone ./
COPY --from=build --chown=node:node /app/web/.next/static ./.next/static
COPY --from=build --chown=node:node /app/web/public ./public

USER node
EXPOSE 3000
CMD ["node", "server.js"]
