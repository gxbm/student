from django.views import View
from django.shortcuts import HttpResponse,redirect,render
from .sqlfenzhung import sql
import json
class types(View):
    def get(self,req):
        db=sql()
        date=db.select("select * from types")
        db.close()
        return render(req,"types.html",{"date":date})
    def post(self):
        pass
class typesadd(View):
    def get(self,req):
        return render(req,"typesadd.html")
    def post(self,req):
        tyid=req.POST.get("tyid")
        tyname=req.POST.get("tyname")
        db = sql()
        db.exec("insert into types (tyid,tyname) values (%s,%s)",[tyid,tyname])
        return redirect('/types/')
class typeshiti(View):
    def get(self,req):
        db = sql()
        date = db.select("select * from types")
        return HttpResponse(json.dumps(date))

