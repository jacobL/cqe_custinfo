from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from collections import OrderedDict
from werkzeug.serving import run_simple
import pymysql
import datetime
import time
import json
#from calendar import monthrange
import dbconfig
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)
 
@app.route("/getWordCloud", methods=['GET'])
def getWordCloud():
    conn = pymysql.connect( host = host , port=port , user = user , passwd = passwd , db = db ) 
    cur = conn.cursor()    
   
    #web = 'all' if request.args.get('web') is None else request.args.get('web');
    #app = 'all' if request.args.get('app') is None else request.args.get('app');
    company = 'huawei' if request.args.get('company') is None else request.args.get('company').lower();
    cur.execute("select cloud from custinfo.wordcloud where company=%s",(company)) 
    
    #cur.execute("select wordcloud from custinfo.wordcloud where web=%s and app=%s and company=%s and keyword=%s",(web,app,company,keyword)) 
    returnData = OrderedDict();
    if cur.rowcount > 0 :    
        returnData[0] = cur.fetchone()[0]
    else :
        returnData[0] = 0
    response = jsonify(returnData)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response  

@app.route("/getNews", methods=['GET'])
def getNews():
    conn = pymysql.connect( host = host , port=port , user = user , passwd = passwd , db = db ) 
    cur = conn.cursor() 
    
    fromdate = request.args.get('fromdate') 
    todate = request.args.get('todate')
    company = 'huawei' if request.args.get('company') is None else request.args.get('company').lower();
    print(fromdate,' ',todate)
    if fromdate is not None and todate is not None :                
        cur.execute("SELECT id,web,app,model,company,title2,content,publishdate,url,creationdate,keywordlist,keywordCount FROM products where status=0 and DATE_FORMAT(creationdate, '%%Y%%m%%d') between %s and %s and company = %s ORDER BY id",(fromdate,todate,company))
    elif fromdate is not None :
        cur.execute("SELECT id,web,app,model,company,title2,content,publishdate,url,creationdate,keywordlist,keywordCount FROM products where status=0 and DATE_FORMAT(creationdate, '%%Y%%m%%d') > %s and company = %s ORDER BY id",(fromdate,company))
    elif todate is not None :
        cur.execute("SELECT id,web,app,model,company,title2,content,publishdate,url,creationdate,keywordlist,keywordCount FROM products where status=0 and DATE_FORMAT(creationdate, '%%Y%%m%%d') < %s and company = %s ORDER BY id",(todate,company))       
           
    returnData = OrderedDict();  
    print('count:',cur.rowcount)
    if cur.rowcount > 0 :    
        c = 0
        for r in cur :        
            tmp = OrderedDict();        
            tmp['id'] = r[0]
            tmp['web'] = r[1]
            tmp['app'] = r[2]
            tmp['model'] = r[3]
            tmp['company'] = r[4]
            tmp['title2'] = r[5]
            tmp['content'] = r[6]
            tmp['publishdate'] = r[7]
            tmp['url'] = r[8]
            tmp['creationdate'] = r[9]
            tmp['keywordlist'] = r[10]
            tmp['keywordCount'] = r[11]
            returnData[c] = tmp
            c = c + 1 
    else :
        returnData[0] = 0
    
    response = jsonify(returnData)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route("/getNews_old", methods=['GET'])
def getNews_old():
    conn = pymysql.connect( host = host , port=port , user = user , passwd = passwd , db = db ) 
    cur = conn.cursor() 
    
    columnList = []
    whereList = []
    
    if request.args.get('web') is not None :        
        columnList.append('web')
        web = request.args.get('web');
        whereList.append(web)
    if request.args.get('app') is not None :        
        columnList.append('app')
        app = request.args.get('app');
        whereList.append(app)
    if request.args.get('company') is not None :        
        columnList.append('company')
        company = request.args.get('company');
        whereList.append(company)
    if request.args.get('keyword') is not None :        
        columnList.append('keyword')
        keyword = request.args.get('keyword');
        whereList.append(keyword)     
    
    returnData = OrderedDict(); 
    sql = "SELECT id,web,app,model,company,title2,content,publishdate,url FROM products where "
    for i in range(0,len(columnList)) :
        if i == 0 :
            sql = sql + columnList[i] + "=%s"
        else :    
            sql = sql + " and " + columnList[i] + "=%s"
    sql = sql + " ORDER BY id"
    print('sql:'+sql)
    c = 0
    cur.execute(sql, whereList)
    for r in cur :        
        tmp = OrderedDict();        
        tmp['id'] = r[0]
        tmp['web'] = r[1]
        tmp['app'] = r[2]
        tmp['model'] = r[3]
        tmp['company'] = r[4]
        tmp['title2'] = r[5]
        tmp['content'] = r[6]
        tmp['publishdate'] = r[7]
        tmp['url'] = r[8]
        returnData[c] = tmp
        c = c + 1 
    
    response = jsonify(returnData)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route("/getUrlByKeywordHuaweiClub", methods=['GET'])
def getUrlByKeywordHuaweiClub():
    conn = pymysql.connect( host = host , port=port , user = user , passwd = passwd , db = db ) 
    cur = conn.cursor() 
     
    keyword = request.args.get('keyword');
    returnData = OrderedDict();
    sql = "select id,url,title2,publishdate,keywordlist,app,model from products where web='花粉論壇' and jiebalist like '%"+keyword+"%' and status<>1 and content is not null order by publishdate desc" 
    
    #print('sql: ',sql)
    cur.execute(sql) 
    c = 0
    for r in cur :
        tmp = OrderedDict();        
        tmp['id'] = r[0]
        tmp['url'] = r[1]
        tmp['title2'] = r[2]
        tmp['publishdate'] = r[3]
        tmp['keywordlist'] = r[4]
        tmp['app'] = r[5]
        tmp['model'] = r[6]
        returnData[c] = tmp
        c = c + 1
    response = jsonify(returnData)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route("/getUrlByKeyword", methods=['GET'])
def getUrlByKeyword():
    conn = pymysql.connect( host = host , port=port , user = user , passwd = passwd , db = db ) 
    cur = conn.cursor() 
    
    company = request.args.get('company');
    keyword = request.args.get('keyword');
    #print('company:',company,' , keyword:',keyword)
    returnData = OrderedDict();
    #cur.execute("select id,url,title2,publishdate,keywordlist from news where web=%s and jiebalist like '%華為%' order by id desc",(app)) 
    if company != 'all' :
        sql = "select id,url,title,publishdate,keywordlist,app from news where company='"+company+"' and jiebalist like '%"+keyword+"%' order by id"
    else :    
        sql = "select id,url,title,publishdate,keywordlist,app from news where jiebalist like '%"+keyword+"%' order by id"
    
    cur.execute(sql) 
    c = 0
    for r in cur :
        tmp = OrderedDict();        
        tmp['id'] = r[0]
        tmp['url'] = r[1]
        tmp['title'] = r[2]
        tmp['publishdate'] = r[3]
        tmp['keywordlist'] = r[4]
        tmp['app'] = r[5]
        returnData[c] = tmp
        c = c + 1
    response = jsonify(returnData)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response        

@app.route("/getUrlByKeywordCompany", methods=['GET'])
def getUrlByKeywordCompany():
    conn = pymysql.connect( host = host , port=port , user = user , passwd = passwd , db = db ) 
    cur = conn.cursor() 
    
    company = request.args.get('company');
    keyword = request.args.get('keyword');
    
    #print('company:',company,' , keyword:',keyword)
    returnData = OrderedDict();
    
    sql = "select id,url,title2,publishdate,keywordlist from news where company='"+company+"' and jiebalist like '%"+keyword+"%' and status=0 order by id"
    
    #print('sql: ',sql)
    cur.execute(sql) 
    c = 0
    for r in cur :
        tmp = OrderedDict();        
        tmp['id'] = r[0]
        tmp['url'] = r[1]
        tmp['title2'] = r[2]
        tmp['publishdate'] = r[3]
        tmp['keywordlist'] = r[4]
        returnData[c] = tmp
        c = c + 1
    response = jsonify(returnData)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':     

    """
    host = '127.0.0.1' 
    port=3306 
    user = 'root' 
    passwd = "1234"
    """
    db='custinfo'
    app.run(host='0.0.0.0', port=84)
    #run_simple('127.0.0.1', 81, app)