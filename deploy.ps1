# Остановка и удаление существующих контейнеров
Write-Host "Stopping and removing existing containers..."
docker-compose down

# Сборка и запуск контейнеров
Write-Host "Building and starting containers..."
docker-compose up --build -d

# Вывод сообщения об успешном запуске
Write-Host "Application is running! Open http://localhost:5000"
