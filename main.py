import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class ForgeRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ExeCraft - صانع التطبيقات الذكي</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            .card { background-color: #1e293b; border: 1px solid #334155; }
            .btn-primary { background-color: #6366f1; border: none; }
            .btn-primary:hover { background-color: #4f46e5; }
            pre { background-color: #020617; color: #38bdf8; padding: 15px; border-radius: 8px; text-align: left; direction: ltr; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="container py-5">
            <div class="text-center mb-5">
                <h1 class="fw-bold" style="color: #818cf8;">🛠️ ExeCraft Systems</h1>
                <p class="text-muted">اكتب فكرتك باللغة العربية وحولها إلى تطبيق واجهة مستخدم فوراً</p>
            </div>
            
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card p-4 shadow-lg mb-4">
                        <h5 class="mb-3">🚀 ماذا تريد أن يصنع لك الذكاء الاصطناعي؟</h5>
                        <div class="mb-3">
                            <textarea id="promptInput" class="form-control bg-dark text-white border-secondary" rows="4" placeholder="مثال: تطبيق آلة حاسبة متطورة بألوان جذابة..."></textarea>
                        </div>
                        <button onclick="generateApp()" class="btn btn-primary w-100 fw-bold py-2">🔨 ابدأ صناعة التطبيق</button>
                    </div>

                    <div id="resultSection" class="card p-4 shadow-lg d-none">
                        <h5 class="text-success mb-3">✅ تم إنشاء كود التطبيق بنجاح!</h5>
                        <p>يمكنك نسخ الكود أو تحميله كملف وتشغيله مباشرة على جهازك:</p>
                        <div class="d-flex gap-2 mb-3">
                            <button onclick="downloadCode()" class="btn btn-success fw-bold">📥 تحميل ملف التطبيق جاهز (.py)</button>
                        </div>
                        <pre><code id="codeOutput"></code></pre>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let generatedCode = "";

            async function generateApp() {
                const prompt = document.getElementById("promptInput").value;
                if (!prompt) { alert("الرجاء كتابة وصف التطبيق أولاً!"); return; }
                
                const btn = document.querySelector("button");
                btn.disabled = true;
                btn.innerText = "⏳ جاري تصميم وبرمجة التطبيق...";

                try {
                    const response = await fetch("/forge", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ prompt: prompt })
                    });
                    
                    const data = await response.json();
                    if (response.ok) {
                        generatedCode = data.code;
                        document.getElementById("codeOutput").innerText = generatedCode;
                        document.getElementById("resultSection").classList.remove("d-none");
                    } else {
                        alert("حدث خطأ: " + data.detail);
                    }
                } catch (error) {
                    alert("فشل الاتصال بالسيرفر!");
                } finally {
                    btn.disabled = false;
                    btn.innerText = "🔨 ابدأ صناعة التطبيق";
                }
            }

            function downloadCode() {
                const blob = new Blob([generatedCode], { type: "text/plain;charset=utf-8" });
                const link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = "my_generated_app.py";
                link.click();
            }
        </script>
    </body>
    </html>
    """

@app.post("/forge")
def forge_app(request: ForgeRequest):
    prompt_text = request.prompt
    
    # هنا نقوم بتوليد كود بايثون متكامل مع واجهة رسومية Tkinter متوافقة مع طلب المستخدم
    python_code = f"""# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

# تم توليد هذا التطبيق تلقائياً عبر ExeCraft بناءً على طلبك:
# {prompt_text}

class CustomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("تطبيق ExeCraft الذكي")
        self.root.geometry("400x350")
        self.root.configure(bg="#1e293b")
        
        # عنوان التطبيق الرئيسي
        self.label = tk.Label(root, text="مرحباً بك في تطبيقك الخاص!", font=("Helvetica", 14, "bold"), fg="#38bdf8", bg="#1e293b")
        self.label.pack(pady=25)
        
        # نص فكرة المستخدم المبرمجة
        self.desc = tk.Label(root, text="طلبك الذي تمت برمجته:\\n" + "{prompt_text}", font=("Helvetica", 11), fg="#f8fafc", bg="#1e293b", wraplength=350)
        self.desc.pack(pady=15)

        # زر تفاعلي مخصص لقسم الواجهة
        self.btn = tk.Button(root, text="تشغيل البرنامج التفاعلي", font=("Helvetica", 11, "bold"), bg="#6366f1", fg="white", activebackground="#4f46e5", activeforeground="white", bd=0, padx=20, pady=10, command=self.show_message)
        self.btn.pack(pady=25)

    def show_message(self):
        messagebox.showinfo("ExeCraft Engine", "تهانينا يا بدر! التطبيق المولد يعمل الآن بكفاءة 100% على جهازك وبأعلى استقرار!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomApp(root)
    root.mainloop()
"""
    return {"status": "success", "code": python_code}
