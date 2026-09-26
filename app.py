from flask import Flask,render_template,request
from pathlib import Path
import json,webbrowser
from threading import Timer
from inference_engine import ExpertSystem
B=Path(__file__).parent;app=Flask(__name__);KB=json.loads((B/"knowledge_base.json").read_text(encoding="utf-8"));ES=ExpertSystem(B/"knowledge_base.json")
@app.get("/")
def home():return render_template("index.html",questions=KB["questions"])
@app.post("/diagnose")
def diagnose():
 f={q["id"]:request.form.get(q["id"]) for q in KB["questions"]}
 return render_template("result.html",result=ES.infer(f)) if all(f.values()) else render_template("index.html",questions=KB["questions"],error="Ответьте на все вопросы.")
if __name__=="__main__":
 Timer(1,lambda:webbrowser.open("http://127.0.0.1:5000")).start();app.run(host="127.0.0.1",port=5000)
