from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()

# Инициализация Jinja2 шаблонов
templates = Jinja2Templates(directory="app/templates")

# Главная страница с формой для загрузки файлов
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# Обработка загруженных файлов
@app.post("/uploadfiles/")
async def upload_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # Чтение данных из файлов
    json1 = await file1.read()
    json2 = await file2.read()

    # Преобразование в JSON
    try:
        data1 = json.loads(json1)
        data2 = json.loads(json2)
    except json.JSONDecodeError:
        return JSONResponse(status_code=400, content={"message": "Ошибка в формате JSON"})

    # Пример обработки: заменяем объект features в первом JSON данными из второго
    if 'features' in data2:
        data1['features'] = data2['features']

    # Возвращаем объединённый результат
    return JSONResponse(content=data1)
