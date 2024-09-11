import json
from dicttoxml import dicttoxml
import xmltodict
import re

class Request:
    def __init__(self,url,headers=[],body=""):
        self.url = url
        self.headers = self.unSerializeHeaders(headers)
        self.body = body
        self.baseParams = {"url":{},"urlparams":[],"body":{},"headers":{}}
        self.ctype = self.getHeaderValue(self.headers,"Content-Type")
        self.xmlroot = False
        self.jsonbody = False
        self.xmlbody = False
        self.multipartbody = False
        self.jsonbodylist = False
        self.getParams()
            
    def parseMultipart(self):
        params = {}
        boundary = self.ctype
        boundary = boundary.split("oundary=")[-1]
        bodyparts = self.body.strip().rstrip('--').split("--"+boundary)
        parts = []
        for part in bodyparts:
            if part != '':
                parts.append(part.strip('--').strip())
        for item in parts:
            value = item.split('\n\n',1)[1]
            chunks = item.split()
            name = chunks[2].split('=')[1].strip('";\'')
            if chunks[3].startswith("filename="):
                filename = chunks[3].split('=')[1].strip('";\'')
            params.update({name:value})
        return params
        
    def getHeaderValue(self,headers,headername):
        for header in headers:
            if header.lower() == headername.lower():
                return headers[header]
        return ""
        
    def getParams(self):
        frags = self.url.split('?')[0].split("/")
        if not "FUZZ" in self.url:
            for i in range(len(frags)):
                if re.match(r"^[a-z0-9]{32}$",frags[i]) or re.match(r"^[0-9]+$",frags[i]) or re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",frags[i]):
                    self.baseParams["urlparams"].append(frags[i])
        else:
            for i in range(len(frags)):
                if "FUZZ" in frags[i]:
                    self.baseParams["urlparams"].append(frags[i].replace("FUZZ",""))
            f1 = self.url.split("?")[0].replace("FUZZ","")
            f2 = ""
            try:
                f2 = self.url.split("?")[1]
                self.url = f1+"?"+f2
            except:
                self.url = f1
            
        if "FUZZ" in json.dumps(self.headers):
            for header in self.headers:
                if "FUZZ" in self.headers[header]:
                    self.headers[header] = self.headers[header].replace("FUZZ","")
                    self.baseParams["headers"].update({header:self.headers[header]})
        query = ""
        if '?' in self.url and not self.url.endswith('?'):
            query = self.url.split('?',1)[1]
        if query != "":
            paramchunks = query.split('&')
            for chunk in paramchunks:
                minichunk = chunk.split('=')
                if len(minichunk)>1:
                    self.baseParams["url"].update({minichunk[0]:minichunk[1]})
                else:
                    self.baseParams["url"].update({minichunk[0]:""})
        if self.body!="":         
            if "boundary" in self.ctype.lower():
                self.multipartbody = True
                self.baseParams["body"].update(self.parseMultipart())
            elif "/json" in self.ctype.lower():
                try:
                    jsonload = json.loads(self.body)
                    if type(jsonload)==list:
                        self.jsonbodylist = True
                        self.baseParams["body"].update(jsonload[0])
                    else:
                        self.baseParams["body"].update(jsonload)
                    self.jsonbody = True
                except:
                    pass
            
            elif "/xml" in self.ctype.lower():
                try:
                    params = xmltodict.parse(self.body)
                    self.xmlbody = True
                    if len(params) == 1 and params["root"]:
                        self.baseParams["body"].update(params["root"])
                        self.xmlroot = True
                    else:
                        self.baseParams["body"].update(params)
                        self.xmlroot = False
                except:
                    pass
            else:
                paramchunks = self.body.split('&')
                for chunk in paramchunks:
                    minichunk = chunk.split('=')
                    if len(minichunk)>1:
                        self.baseParams["body"].update({minichunk[0]:minichunk[1]})
                    else:
                        self.baseParams["body"].update({minichunk[0]:""})
                        
    def serializeHeaders(self,headersdict):
        headers = []
        for header in headersdict:
            headers.append(header+": "+headersdict[header])
        return headers
        
    def unSerializeHeaders(self,headerslist):
        headers = {}
        for header in headerslist:
            hh = header.split(":",1)
            headers.update({hh[0].strip():hh[1].strip()})
        return headers
        
    def reBuild(self,fuzzparam,pos,payloadpos="append"):
       url = self.url.split('?')[0]+"?"
       body = ""
       headers = []
       if pos=="url":
           for param in self.baseParams["url"]:
               if param == fuzzparam:
                   if payloadpos=="append":
                       url = url+param+"="+self.baseParams["url"][param]+"FUZZ"+"&"
                   else:
                       url = url+param+"=FUZZ&"
               else:
                   url = url+param+"="+self.baseParams["url"][param]+"&"
           url = url.strip('&')
           url = url.strip('?')
           body = self.body
           headers = self.serializeHeaders(self.headers)
       elif pos=="body":
           if self.jsonbody:
               if self.jsonbodylist:
                   temp = json.loads(self.body)[0]
                   if payloadpos=="append":
                       temp[fuzzparam] = temp[fuzzparam]+"FUZZ"
                   else:
                       temp[fuzzparam] = "FUZZ"
                   body = json.dumps([temp])
               else:
                   temp = json.loads(self.body)
                   if payloadpos=="append":
                       temp[fuzzparam] = temp[fuzzparam]+"FUZZ"
                   else:
                       temp[fuzzparam] = "FUZZ"
                   body = json.dumps(temp)
           elif self.xmlbody:
               temp = {}
               for ttemp in self.baseParams["body"]:
                   temp[ttemp] = self.baseParams["body"][ttemp]
               if payloadpos=="append":
                   temp[fuzzparam] = temp[fuzzparam]+"FUZZ"
               else:
                   temp[fuzzparam] = "FUZZ"
               body = dicttoxml(temp, root=self.xmlroot, attr_type=False).decode()
           elif self.multipartbody:
               body = self.body.replace("\n"+self.baseParams["body"][fuzzparam],"\n"+self.baseParams["body"][fuzzparam]+"FUZZ")
           else:
               for param in self.baseParams["body"]:
                   if param == fuzzparam:
                       if payloadpos=="append":
                           body = body+"&"+param+"="+self.baseParams["body"][param]+"FUZZ"
                       else:
                           body = body+"&"+param+"=FUZZ"
                   else:
                       body = body+"&"+param+"="+self.baseParams["body"][param]
           body = body.strip('&')
           url = self.url
           headers = self.serializeHeaders(self.headers)
       elif pos == "urlparams":
           if payloadpos=="append":
               url = self.url.replace(fuzzparam,fuzzparam+"FUZZ")
           else:
               url = self.url.replace(fuzzparam,"FUZZ")
           body = self.body
           headers = self.serializeHeaders(self.headers)
       else:
           for header in self.headers:
               if header == fuzzparam:
                   if payloadpos=="append":
                       headers.append(header+": "+self.headers[header]+"FUZZ")
                   else:
                       headers.append(header+": FUZZ")
               else:
                   headers.append(header+": "+self.headers[header])
           url = self.url
           body = self.body
       return (url,headers,body)
    def reBuildAll(self,payloadpos="append"):
       variations = []
       for param in self.baseParams["url"]:
           variations.append(self.reBuild(param,"url",payloadpos))
       for param in self.baseParams["body"]:
           variations.append(self.reBuild(param,"body",payloadpos))
       for header in self.baseParams["headers"]:
           variations.append(self.reBuild(header,"headers",payloadpos))
       for up in self.baseParams["urlparams"]:
           variations.append(self.reBuild(up,"urlparams",payloadpos))
       return variations
