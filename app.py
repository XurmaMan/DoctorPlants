from flask import Flask, render_template, request, session, redirect, url_for
from pathlib import Path
import json, os

BASE=Path(__file__).resolve().parent
app=Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY","doctor-plants-educational-v3")
KB=json.loads((BASE/"knowledge_base.json").read_text(encoding="utf-8"))

@app.get("/")
def home():
    session.clear()
    return render_template("home.html")

@app.get("/consult")
def consult():
    qid=session.get("current",KB["start"])
    q=KB["questions"][qid]
    history=session.get("history",[])
    return render_template("question.html",q=q,qid=qid,step=len(history)+1)

@app.post("/answer")
def answer():
    qid=request.form.get("qid"); value=request.form.get("answer")
    if qid not in KB["questions"] or value not in KB["questions"][qid]["options"]:
        return redirect(url_for("consult"))
    opt=KB["questions"][qid]["options"][value]
    hist=session.get("history",[])
    hist.append({"qid":qid,"question":KB["questions"][qid]["text"],"value":value,"answer":opt["label"]})
    session["history"]=hist
    if "result" in opt:
        session["result"]={"code":opt["result"],"confidence":opt["confidence"],"rule":opt["rule"]}
        return redirect(url_for("result"))
    session["current"]=opt["next"]
    return redirect(url_for("consult"))

@app.get("/back")
def back():
    hist=session.get("history",[])
    if not hist: return redirect(url_for("home"))
    hist.pop()
    session["history"]=hist
    session.pop("result",None)
    session["current"]=hist[-1]["qid"] if hist else KB["start"]
    if hist:
        # Recalculate next node after the previous retained answer.
        prev=hist[-1]
        opt=KB["questions"][prev["qid"]]["options"][prev["value"]]
        if "next" in opt: session["current"]=opt["next"]
    return redirect(url_for("consult"))

@app.get("/result")
def result():
    r=session.get("result")
    if not r:return redirect(url_for("consult"))
    d=KB["diagnoses"][r["code"]]
    return render_template("result.html",diagnosis=d,confidence=r["confidence"],rule=r["rule"],history=session.get("history",[]))

if __name__=="__main__":
    app.run(host="127.0.0.1",port=5000,debug=False)
