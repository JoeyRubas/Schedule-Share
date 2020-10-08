from flask import Flask, json, render_template, request, redirect, url_for, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
import os
from flask_pymongo import PyMongo
from flask_dance.contrib.google import make_google_blueprint, google
import sys
from flask_sslify import SSLify
#from flask_talisman import Talisman



os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#Initize App
app = Flask(__name__)

#IDK what this does some tutorial told me to do it
app.config["SECRET_KEY"] = os.environ.get("SECRET")
#Talisman(app)
app.config["MONGO_URI"]= os.environ.get("MONGO_URI")
mongo = PyMongo(app)

#SSLify(app)

app.secret_key = os.urandom(24)
blueprint = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_SECRET"),
    authorized_url= "/",
    scope = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile", "openid"])
app.register_blueprint(blueprint, url_prefix="/login")


                           
class SignUpForm(FlaskForm):
    """This class is for the primary form on the site. It creats all of the buttons for the acccount creation form"""
    school = SelectField("school", choices = [('NCHS', 'NCHS'), ('NNHS', 'NNHS')])
    p1 = StringField("p1")
    p2 = StringField("p2")
    p3 = StringField("p3")
    p4 = StringField("p4")
    p5 = StringField("p5")
    p6 = StringField("p6")
    p7 = StringField("p7")
    p8 = StringField("p8")
    submit1 = SubmitField("submit")

class Search(FlaskForm):
    """This class is for the search in the nav."""
    fname = StringField("fname")
    search = StringField("search")
    submit = SubmitField("search")


def search_results(text):
    """The function runs whenever a search is submitted it runs the search and renders the HTML"""
    #We still need to initialize the seach class so that it works on a search results page
    if not "id" in session:
        return redirect("/")
    search = Search()
    
    #initialize the list of results
    if "<" in text or ">" in text:
        results = ["Search cannot include < or >"]
    else:
        results =[]
        query_results = mongo.db.users.find({"name":{"$regex" : ".*"+text.title()+".*"}})
        query_results1 = mongo.db.clas.find({"name":{"$regex" : ".*"+text.title()+".*"}})
        for person in query_results:
        #Checks if the search is in the person's name; if it is they are added to the list of results
            results.append(("/person/"+person["id"], person["name"]))#Here he add a tuple containing the persons name and id; This is because we need to display the name and need the id to genorate URLS
        for clas in query_results1:
        #Checks if the search is in the person's name; if it is they are added to the list of results
            results.append(("/class/"+clas["id"], clas["name"]))#Here he add a tuple containing the class name and id; This is because we need to display the name and need the id to genorate URL
        if results == []:
            results = [(session["id"], "No results")]
    return render_template("search.html", search = search, results = results)#Renders the HTML, passing in the search results and the instance of the search class 







@app.route("/", methods=["get", "post"])
def index():
    """Very simple function for providing the home page html; only code other than the return is the search bar code"""
    #Search bar code
    search = Search()
    if search.is_submitted():
        results = request.form
        return search_results(results["search"])
    try:
        if google.authorized:
                resp = google.get("/oauth2/v1/userinfo").json()
                if "id" not in session:
                    session["id"] = resp["email"][:resp["email"].index("@")]
                    session["email"] = resp["email"]
                    session["name"] = resp["given_name"]+" "+resp["family_name"]
                    print('Cookie Left', file=sys.stderr)
    except:
        pass

    if "id" in session:
        print('Not index', file=sys.stderr)
        c = mongo.db.users.find_one({'id': session["id"]})
        if c:
            l = "person/"+session["email"][:session["email"].index("@")]
            return redirect("person/"+session["email"][:session["email"].index("@")])
        else:
            return redirect("entry")
    

    #Renders home page HTML, passing in the search bar class instance
    return render_template("index.html", search = search)


@app.route("/signin")
def signin():
    if not google.authorized:
        return redirect(url_for("google.login"))
    else:
        return redirect("/")


@app.route("/about", methods=["get", "post"])
def about():
    """Basically same as home function"""
    #Search Bar Code
    search = Search()
    if search.is_submitted():
        results = request.form
        return search_results(results["search"])
    #Renders home page HTML, passing in the search bar class instance
    return render_template("about.html", search = search)

@app.route("/how", methods=["get", "post"])
def how():
    """Basically same as home function"""
    #Search Bar Code
    search = Search()
    if search.is_submitted():
        results = request.form
        return search_results(results["search"])
    #Renders home page HTML, passing in the search bar class instance
    return render_template("how.html", search = search)
@app.route("/changelog", methods=["get", "post"])
def change():
    """Basically same as home function"""
    #Search Bar Code
    search = Search()
    if search.is_submitted():
        results = request.form
        return search_results(results["search"])
    #Renders home page HTML, passing in the search bar class instance
    return render_template("changelog.html", search = search)


@app.route("/privacy", methods=["get", "post"])
def privacy():
    #Search Bar Code
    search = Search()
    #Initialize form class
    form = SignUpForm()
    return render_template("privacy.html", search = search)


@app.route("/entry/", methods=["get", "post"])
def entry():
    """Very long function; gets data from the primary form and used it to create a user json, add user to all their classes' jsons and the site directory"""
    if not google.authorized:
        redirect("/")
    resp = google.get("/oauth2/v1/userinfo")
    json1 = resp.json()
    try:
        json1["email"].index("@stu.naperville203.org")
    except:
        return "ERROR: Please use district 203 email"

    #Search Bar Code
    search = Search()
    #Initialize form class
    form = SignUpForm()

    try:
        if request.form["search"] and search.is_submitted():
            print(request.form["search"])
            results = request.form
            return search_results(results["search"])
    except:
        pass


    #this if statement funs when the form is submitted
    if form.submit1.data and form.is_submitted():
        
        c = mongo.db.users.find_one({'id': session["id"]})
        if c:
            return redirect("/")

        
        result = request.form#Gets data from form in a dictionary data format
        errors = []
        schedule_names = []
        
        for num in range(8):
            try:
                schedule_names.append(convert[ result["p"+str(num+1)][:result["p"+str(num+1)].index("-")].replace(" ", "") ])
            except:
                errors.append("Issue with code for period #"+str(num+1))
            if ">" in result["p"+str(num+1)] or "<" in result["p"+str(num+1)]:
                errors.append("Class codes cannot include < or > charaters")
        if errors:
            errors.append('If any of these errors are incorrect, please enter "A-" in the cooresponding field and contact us at scheduleshare203@gmail.com')
            return render_template("entry_errors.html", form = form, search = search, errors = errors, results = result)
        
                
            

        
        #Creates the majority of the JSON just by directly refrencing the form data
        data = {"id":json1["email"][:json1["email"].index("@")],
                "email":json1["email"],
                 "school":result["school"],
                 "name":session["name"].title(),
                 "schedule_ids":[result["school"][1:2]+result["p"+str(num+1)].replace(" ", "") for num in range(8)],
                 "schedule_names":schedule_names}
        mongo.db.users.insert(data)
        
        for clas1 in data["schedule_ids"]:
            if mongo.db.clas.find({'id': clas1.replace(" ", "")}).count() > 0:
                before = mongo.db.clas.find_one_or_404({"id":clas1.replace(" ", "")})
                before["students_id"].append(data["id"])
                before["students_name"].append(data["name"])
                mongo.db.clas.update_one({"id":clas1.replace(" ", "")}, {"$set":before})
                       
            else:
                num = data["schedule_ids"].index(clas1)
                data1 = {"id":clas1.replace(" ", ""),
                          "name":convert[result["p"+str(num+1)][:result["p"+str(num+1)].index("-")]],
                          "students_id":[data["id"]],
                          "students_name":[data["name"]]}
                mongo.db.clas.insert(data1)
        return render_template("person.html",person = mongo.db.users.find_one_or_404({"id":data["id"]}), search = search)
    return render_template("entry.html", form=form, search = search)




@app.route("/edit/", methods=["get", "post"])
def edit():
    if not "id" in session:
        return redirect("/")
    try:
        session["email"].index("@stu.naperville203.org")
    except:
        return redirect("/")
    
    id1 = session["id"]
    form = SignUpForm()
    start = mongo.db.users.find_one_or_404({"id":id1})
    search = Search()
    try:
        if request.form["search"] and search.is_submitted():     
            results = request.form
            return search_results(results["search"])
    except:
        pass
    
    
    if form.submit1.data and form.is_submitted():
        result = request.form
        
        errors = []
        schedule_ids = []
        schedule_names = []
        for num in range(8):
            try:
                schedule_names.append(convert[result["p"+str(num+1)][:result["p"+str(num+1)].index("-")]])
            except:
                errors.append("Issue with code for period #"+str(num+1))
            if ">" in result["p"+str(num+1)] or "<" in result["p"+str(num+1)]:
                errors.append("Class codes cannot include < or > charaters")
        if errors:
            errors.append("If any of these errors are incorrect, please enter A and contact us at scheduleshare203@gmail.com")
            return render_template("entry_errors.html", form = form, search = search, errors = errors, results = result)

        
        data = {"id":start["id"],
                "email":start["email"],
                "school":result["school"],
                "name":start["name"],
                "schedule_ids":[result["school"][1:2]+result["p"+str(num+1)] for num in range(8)],
                "schedule_names":schedule_names}
        mongo.db.users.update({"id":id1}, {"$set":data})

        for clas1 in data["schedule_ids"]:
            if mongo.db.clas.find({'id': clas1}).count() > 0:
                before = mongo.db.clas.find_one_or_404({"id":clas1})
                before["students_id"].append(data["id"])
                before["students_name"].append(data["name"])
                mongo.db.clas.update_one({"id":clas1}, {"$set":before})
                       
            else:
                data1 = {"id":clas1,
                          "name":convert[result["p"+str(num+1)][:result["p"+str(num+1)].index("-")]],
                          "students_id":[data["id"]],
                          "students_name":[data["name"]]}
                mongo.db.clas.insert(data1)
        return render_template("person.html",person = mongo.db.users.find_one_or_404({"id":data["id"]}), search = search)
        return render_template("person.html",person = mongo.db.users.find_one_or_404({"id":data["id"]}), search = search)

    return render_template("edit.html", person =start, form=form, search = search)



@app.route("/person/<string:id1>", methods=["get", "post"])
def person(id1):
    if not "id" in session:
        return redirect("/")
    try:
        session["email"].index("@stu.naperville203.org")
    except:
        return redirect("/")
    search = Search()
    if search.is_submitted():
        results = request.form
        return search_results(results["search"])
    if "<" in id1 or ">" in id1:
        return "ERROR, ids cannot inculde < or > charaters"
                                
    return render_template("person.html",person = mongo.db.users.find_one_or_404({"id":id1}), search = search)

@app.route("/class/<string:id1>", methods=["get", "post"])
def clas(id1):
    try:
        session["email"].index("@stu.naperville203.org")
    except:
        return redirect("/")
    if not "id" in session:
        return redirect("/")
    search = Search()
    if search.is_submitted():
        results = request.form
        return search_results(results["search"])
    if "<" in id1 or ">" in id1:
        return "ERROR, ids cannot inculde < or > charaters"
    return render_template("clas.html", clas=mongo.db.clas.find_one_or_404({"id":id1}), search = search)

#

if __name__ == "__main__":
    app.run()
   
          

