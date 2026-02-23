(
echo FROM python:3.11-slim
echo.
echo WORKDIR /app
echo.
echo COPY requirements.txt .
echo RUN pip install --no-cache-dir -r requirements.txt
echo.
echo COPY app ./app
echo.
echo ENV PORT=8080
echo CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
) > Dockerfile