# Stage 1 — Сборка
FROM node:18-alpine AS builder

WORKDIR /app

# Копируем зависимости и устанавливаем
COPY package*.json ./
RUN npm install

# Копируем исходники и билдим
COPY . .
RUN npm run build

# Stage 2 — Продакшн-запуск
FROM node:18-alpine

WORKDIR /app

# Устанавливаем только продакшн-зависимости (если нужно)
COPY --from=builder /app/.output ./.output
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

EXPOSE 3000

# Запуск Nuxt с серверным пререндером
CMD ["node", ".output/server/index.mjs"]
