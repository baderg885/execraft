import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI(title="ExeCraft Local Server")

# 1. تشغيل الصفحة الرئيسية وقراءة ملف index.html بشكل سليم
@app.get("/", response_class=HTMLResponse)
async def read_root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>خطأ: لم يتم العثور على ملف index.html في المجلد!</h1>"

# 2. مسارات احتياطية لضمان عدم حدوث خطأ إذا حاول المتصفح الاتصال بالباكيند
@app.post("/forge")
@app.post("/api/forge")
@app.post("/compile")
@app.post("/api/compile")
async def mock_forge(request: Request):
    try:
        body = await request.json()
    except:
        body = {}
    return {
        "status": "success",
        "message": "Compilation started successfully (Simulated)",
        "task_id": "execraft-task-123",
        "data": body
    }

# 3. مسار لتجهيز ملف التحميل عند اكتمال العداد
@app.get("/download")
@app.get("/api/download")
async def mock_download():
    dummy_file = "execraft_app.exe"
    if not os.path.exists(dummy_file):
        with open(dummy_file, "wb") as f:
            f.write(b"EXE Simulation Content")
    return FileResponse(dummy_file, filename=dummy_file, media_type="application/octet-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)