import json
class ExpertSystem:
 def __init__(self,p): self.kb=json.load(open(p,encoding="utf-8"))
 def infer(self,f):
  h=[(r["weight"],len(r["conditions"]),r) for r in self.kb["rules"] if all(f.get(k)==v for k,v in r["conditions"].items())]
  if not h:return {"diagnosis":"Однозначный диагноз не определён","recommendation":"Проверьте условия содержания повторно.","explanation":"Ни одно правило не выполнилось полностью.","rule":"—"}
  r=sorted(h,reverse=True,key=lambda x:(x[0],x[1]))[0][2];d=self.kb["diagnoses"][r["diagnosis"]]
  return {"diagnosis":d["name"],"recommendation":d["recommendation"],"explanation":r["explanation"],"rule":r["id"]}
