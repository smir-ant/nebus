# Запуск

1) `docker build -t nebus_image .`

2) `docker run -d -p 8000:8000 --name nebus nebus_image`

3) http://localhost:8000/docs

---
Да, можно было прикрутить uv, podman и нормальную геодезическую механику расчёта по прямоугольникам и координатам, но как mvp-продукт, а по факту тестовое - более чем, имхо