# 1. Используем официальный образ Node.js
FROM node:18-alpine

# 2. Рабочая директория
WORKDIR /app

# 3. Копируем зависимости
COPY package*.json ./

# 4. Устанавливаем зависимости
RUN npm install

# 5. Копируем весь проект
COPY . .

# 6. Сборка проекта
RUN npm run build

# 7. Запуск Nuxt в режиме production
EXPOSE 3000
CMD ["npm", "run", "start"]
