from flask import Flask, render_template,make_response, request, jsonify, redirect
from pymongo import MongoClient

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
database = 'test'
db = mongo['test']

@app.route("/")
def index(): 
    list = []
    num = db.test.find({'email': 'pachu@gmail.com'}).limit(1)
    for i in num: 
        list.append(i)    
    return render_template("index.html", num = list ) 

@app.route("/home")
@app.route("/home/<name>")
def home(name=None): 
    if name == None: 
        return render_template("home.html", name=name)
    else:    
        resp = make_response(render_template("home.html", name=name))
        resp.set_cookie(name, 'username')
        return resp   

@app.route("/login", methods=['GET', 'POST'])
def login(): 
    #load page login 
    if request.method == 'GET': 
        return render_template("login.html")
    #check login
    if request.method == 'POST': 
         email_request = request.form['email']
         email_list = ()
         email = db.test.find({'email':email_request}).limit(1)
         for i in email: 
            email_list.append(i)
         
         if len(email_list) != 0 :
             return redirect('/home')
         else:
             return redirect('/login')         
         
@app.route("/about/<name>")
def about(name=None):
    return render_template("about.html", name=name)    

@app.route("/register", methods=['GET', 'POST'])
def register(): 
    if request.method == 'GET': 
        return render_template("register.html")
    
    if request.method == 'POST':
        name = {'username': request.form['username'], 'password': request.form['password'], 'email': request.form['email']}
        db.database.insert(name)
        return redirect('/home') 
    else: 
        return "<h1>bad request</h1>"

       
#page not found
@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404  

app.run(debug=True)