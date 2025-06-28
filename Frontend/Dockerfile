# Используем официальный образ Node.js
FROM node:18-alpine AS builder

WORKDIR /app

# Копируем зависимости и устанавливаем
COPY package*.json ./
RUN npm install

# Копируем весь проект и собираем
COPY . .
RUN npm run build

# Стейдж для запуска приложения
FROM node:18-alpine
WORKDIR /app

# Копируем только собранные файлы и зависимости
COPY --from=builder /app ./

EXPOSE 3000
CMD ["npm", "run", "start"]
