from flask import Flask, request, jsonify
import openai
import os
import PyPDF2
import random
import string
from google.cloud import storage
from io import BytesIO
import requests
import firebase_admin
#from firebase_admin import firestore
from google.cloud import firestore
from fpdf import FPDF
class PDF(FPDF):
    def header(self):
        # This can be used to set header content. It's empty for this example.
        pass

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def text_to_pdf(text, filename):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(0, 10, txt=text)
    print(type(pdf))
    pdf.output(filename)

def testarray():
    db = firestore.Client()
    username = "testarray@test.com"
    doc_ref = db.collection('dev-users').document(username)
    
    # Set the fields you want in the document
    doc_ref.set({
       'email': username,
       'demands':[]
    })

def addarray():
    db = firestore.Client()
    username = "testarray@test.com"
    doc_ref = db.collection('dev-users').document(username)
    doc_ref.update({"demands":firestore.ArrayUnion(["dos"])})

def getarrayinfo():
    db = firestore.Client()
    username = "testarray@test.com"
    doc_ref = db.collection('dev-users').document(username)
    doc=doc_ref.get().to_dict()
    final_response={}
    for demands in doc["demands"]:
        doc_demand= db.collection('demands').document(demands)
        doc_text=doc_demand.get().to_dict()
        final_response[demands]={"text":doc_text["text"]} 
    print(final_response)

def returnuserdata():
    db = firestore.Client()
    username = "sergio.pena@madcloudconsulting.com"
    doc_ref = db.collection('dev-users').document(username)
    doc=doc_ref.get().to_dict()
    userdata ={
            "userinfo":{    
            	"username": doc.get("username"),
	            "email": doc.get("email"),
	            "numberofcases": len(doc.get("demands"))
    }}
    print(userdata)

def updatealldemands():
    db = firestore.Client()
    username = "testdos@gmail.com"
    demandas= db.collection('dev-users').document(username)
    doc=demandas.get().to_dict()
    demandasfinales=doc["demands"]
    #docs= db.collection('demands').stream()
    cases=[]
    for doc in demandasfinales:
        cases.append(db.collection('demands').document(doc).get().to_dict())
    print(cases)
        #print(f"{doc.id} ")
#        db.collection('demands').document(doc).update({
#           'id':f'{doc.id}', 
#            'name': '',
#            'type': '',
#            'lawbranch': '',
#            'analysisgpt': '',
#            'scope': '',
#            'court': '',
#            'tribunal':'',
#            'accused': '',
#            'causetype': '',
#            'startway': '',
#            'felony': '',
#            'felonynumber': '',
#            'litigants':[]
#            })

def getallcases():
    db = firestore.Client()
    docs= db.collection('demands').stream()
    cases=[]
    for doc in docs:
        cases.append(db.collection('demands').document(doc.id).get().to_dict())
    print(cases)

def getonecase():
    db = firestore.Client()
    demand=db.collection('demands').document("PDiHDvDkdz").get().to_dict()
    print(demand)

def validatedemandonarray():
    db = firestore.Client()
    username = "tipo@example.com"
    doc_ref = db.collection('dev-users').document(username)
    doc=doc_ref.get().to_dict()
    final_response={}
    if not "PDiHDvDkdz" in doc["demands"]:
        print("no esta el documento")
    else:
        print("Documento encontrado")

def creatingpdf():
    db = firestore.Client()
    doc_ref = db.collection('demands').document('qALAxIsjtI')
    doc=doc_ref.get().to_dict()
    text = doc['text']
    text_to_pdf(text,"test1.pdf")

def errorupdate():
    db = firestore.Client()
    doc_ref = db.collection('deverrorlog').document('testone')
    #doc_ref.update({"isfail":True})
    doc_ref.update({"numbererroes":firestore.Increment(1)})
    doc_ref.update({"isfail":False})


if __name__ == "__main__":
    #testarray()
    #addarray()
    #getarrayinfo()
    #returnuserdata()
    #updatealldemands()
    #getallcases()
    #getonecase()
    #validatedemandonarray()
    #creatingpdf()
    errorupdate()
