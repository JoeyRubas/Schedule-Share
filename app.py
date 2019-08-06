from flask import Flask, json, render_template, request, redirect, url_for, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
import os
from flask_pymongo import PyMongo
from flask_dance.contrib.google import make_google_blueprint, google
import sys
from flask_sslify import SSLify
#from flask_talisman import Talisman



#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#Initize App
app = Flask(__name__)

#IDK what this does some tutorial told me to do it
app.config["SECRET_KEY"] = os.environ.get("SECRET")
#Talisman(app)
app.config["MONGO_URI"]= os.environ.get("MONGO_URI")
mongo = PyMongo(app)

SSLify(app)
convert = {"T360A1":"AP Gov", "S560A1":"AP Chemistry", "930811":"AP Chemistry Lunch","925611":"Link Lunch", "926611":"Link Leader Lunch", "A":"Missing Class", "923011":"Link Lunch","910011":"Lunch","910012":"Lunch","C60031": "Academic Reading", "C61031": "Sophomore Reading Seminar", "C62031": "Junior/Senior Reading Seminar", "B10011": "Introduction to Business", "B120B1": "Tech Edge", "B160B2": "Tech Edge +", "B240B1": "Accounting 1", "B260C1": "Honors College Accounting", "B30011": "Marketing", "B32012": "Advanced Marketing (NNHS only)", "B320N2": "Blended Advanced Marketing (NCHS only)", "B34012": "Advertising", "B37011": "Business INCubator", "B38011": "Business Law", "B380M1": " Online Business Law", "B40011": "International Business", "B44011": "Computer Programming 1", "B440N1": "Blended Computer Programming 1 (NCHS only)", "B46012": "Computer Programming 2", "B48012": "Game Design", "B480M1": "Online Game Design", "B52011": "Web Page Design", "B520M1": "Online Web Page Design", "B54012": "Advanced Web Page Design", "B560A1": "AP Computer Science A", "B580W1": "Software Engineering 1", "B590W2": "Software Engineering 2", "B60011": "Yearbook Production (NNHS only)", "B62011": "Digital Publishing & Design", "B64012": "Animation & Multimedia", "B70011": "Consumer Economics", "B700N1": "Blended Consumer Economics (NNHS only)", "B700M1": " Online Consumer Economics", "B87011": "CTE Internship", "B980N1": "Blended STEM  Inquiry and Research Capstone", "F100D2": "Fashion Merchandising", "F140D1": "Fashion Design", "F18011": "Food Science", "F22011": "Culinary Arts & Nutrition 1", "F26011": "Culinary Arts & Nutrition 2", "F27011": "Culinary Arts & Nutrition 3", "F30011": "Senior Foods", "F34011": "Interior Design", "F42011": "Human Growth & Development", "F460B1": "Early Childhood Education 1", "F500B2": "Early Childhood Education 2", "F54011": "Adult Living/Personal Relationships (at NNHS only)", "F580D1": "Intro to Teaching 1", "F620D2": "Intro to Teaching 2", "F66011": "Intro to Health Occupations", "F700D2": "Health Occupations", "F87011": "CTE Internship", "F980N1": "Blended STEM  Inquiry and Research Capstone", "J100B1": "Introduction to Horticulture", "J140D1": "Floral Design", "J160D2": "Advanced Floral Design", "J18012": "Greenhouse Crop Production", "J20011": "Companion Animal Biology", "J22012": "Advanced Companion Animal Biology", "J280J1": "Supervised Agriscience Experience ", "J30011": "Graphics 1", "J32012": "Graphics 2", "J34012": "Graphics 3", "J400D2": "Basic Electricity", "J420D1": "Electronics", "J460D1": "Computer Repair/A+ Cert", "J480D1": "LANWAN/Network+Cert", "J50011": "Woodworking 1 / Workmanship", "J52011": "Woodworking 2 / Craftmanship", "J54011": "Woodworking 3 / Cabinetry", "J56011": "Drafting 1  AutoCad 2D", "J580D2": "Drafting 2  AutoCad 3D", "J60011": "Pre-Engineering Drafting", "J62011": "Architectural Drafting", "J64011": "Research & Design", "J70011": "Automotive Maintenance", "J72012": "Automotive Mechanics", "J74011": "Automotive Servicing", "J87011": "CTE Internship", "J980N1": "Blended STEM Inquiry & Research Capstone", "J760D1": "Autobody Repair & Refinishing", "J780D1": "Construction Trades", "F780D1": "Cosmetology", "J820D1": "Criminal Justice", "F860D1": "Professional Cooking, Baking & Service", "J800D1": "Fire Science", "F800D1": "Medical & Health Careers", "J790D1": "HVAC & Refrigeration", "F820D1": "Nursing Assistant Training Program", "C12011": "English 1", "C120H1": "Honors English 1", "C17011": "English 2", "C170H1": "Honors English 2", "C19011": "English 2 : Journalism", "C190H1": "Honors English 2: Journalism", "C20011": "Speech Communication", "C25011": "English 3", "C250H1": "Honors English 3", "C27011": "American Studies", "C280A1": "AP Language & Composition", "C280N1": "Blended AP Language & Composition (NCHS only)", "C34011": "Writing Styles & Forms", "C37011": "Senior Rhetoric", "C370H1": "Honors Senior Rhetoric", "C39011": "Creative Writing", "C40011": "20th Century Literature", "C410W1": "English Literature", "C42011": "Traditions in Communication", "C435W1": "Themes in Western Literature & Art", "C45011": "World Literature", "C455M1": "Online African American Literature", "C46011": "Literary Themes", "C480A1": "AP Literature & Composition", "C49011": "Yearbook Production", "C50511": "Advanced Media Lab", "C53012": "Advanced Speech", "C56011": "Mass Media", "C57011": "Film as Literature", "C58012": "Film Production", "C59011": "Newspaper Production (NCHS only)", "C980N1": "Humanities Capstone-Blended Learning", "A16011": "Drawing 1", "A19011": "Drawing 2", "A20011": "Drawing 3", "A21011": "Drawing 4", "A22011": "Painting 1", "A23011": "Painting 2", "A27011": "Painting 3", "A28011": "Painting 4", "A37011": "Ceramics 1", "A38011": "Ceramics 2", "A39011": "Ceramics 3", "A40011": "Ceramics 4", "A43011": "Jewelry/Metals 1", "A44011": "Jewelry/Metals 2", "A45011": "Jewelry/Metals 3", "A46011": "Jewelry/Metals 4", "A63011": "Sculpture 1", "A64011": "Sculpture 2", "A50011": "Photography 1 (Traditional)", "A51011": "Photography 2 (Traditional)", "A52011": "Photography 3", "A53011": "Photography 4", "A54011": "Photography 2 (Digital)", "A55511": "Film & Video Arts", "A57011": "Digital Art 1", "A58011": "Digital Art 2", "A59011": "Digital Art 3", "A60011": "Digital Art 4", "A910A1": "AP Art History", "A930A1": "AP Studio Art 2D", "A935A1": "AP Studio Art 2D Design", "A940A1": "AP Studio Art 3D", "A95011": "Adapted Art & Design Leaders", "N10011": "Introduction to Band", "N12011": "Intermediate Band", "N15011": "Intermediate/Advanced Band (NCHS Only)", "N17011": "Advanced Band", "N30011": "Introduction to Orchestra", "N31011": "Intermediate Orchestra (NNHS Only)", "N32011": "Intermediate/Advanced Orchestra", "N34011": "Advanced Orchestra", "N38011": "Introduction to Female Choir", "N46011": "Advanced Female Choir (NNHS Only)", "N50011": "Introduction to Male Choir", "N58011": "Intermediate Mixed Choir (NCHS Only)", "N62011": "Advanced Mixed Choir", "N66011": "Music Theory 1", "N660M1": "Online Music Theory 1", "N700A1": "AP Music Theory", "N74011": "Music Appreciation", "N980W1": "Music Capstone", "E10011": "Acting", "E13011": "Advanced Acting", "E16011": "Play Production", "M10011": "Introduction to Algebra", "M16011": "Survey of Math Topics", "M19011": "Algebra 1", "M190N1": "Blended Algebra 1 ", "M25011": "Algebra 1 Support", "M28011": "Algebra 1 w/Geometry", "M31011": "Geometry Core", "M34011": "Geometry", "M340N1": "Blended Geometry (NCHS only)", "M340M1": "Online Geometry", "M340H1": "Honors Geometry", "M40011": "Algebra 2 Core", "M43011": "Algebra 2", "M430M1": "Online Algebra 2", "M430H1": "Honors Algebra 2", "M50011": "Discrete Math", "M51012": "Statistics", "M52011": "Business Precalculus", "M520N1": "Blended Business Precalculus", "M53011": "Precalculus", "M530H1": "Honors Precalculus", "M600A1": "AP Calculus AB", "M610A1": "AP Calculus BC", "M640W1": "Multivariable Calculus (NCHS Only)", "M650E1": "Multivariable Calculus w/Lin Algebra (NNHS Only)", "M680A1": "AP Statistics", "M980N1": "Blended STEM Capstone ", "S25011": "Principles of Biology & Chemistry", "S50011": "Chemistry", "S500H1": "Honors Chemistry", "S31011": "Biology", "S370H1": "Honors Biology", "S59011": "Physics", "S600A1": "AP Physics 1", "S530W1": "Advanced Chemistry", "S430W1": "Anatomy & Physiology", "S430N1": "Blended Anatomy & Physiology (NNHS only)", "S19011": "Astronomy", "S460W2": "Biotechnology", "S16012": "Physical Geology", "S13011": "Weather & Environment", "S400A1": "AP Biology", "T280A1": "AP Chemistry", "S220A1": "AP Environmental Science", "S630A1": "AP Physics 2", "S680A1": "AP Physics C", "S65011": "Research & Design", "S980N1": "Blended STEM Capstone ", "S200M1": "Online Sustainable Energy", "T10011": "World Cultures", "T79011": "Comparative Religions", "T81011": "Cultural Anthropology", "T150A1": "AP Human Geography", "T150M1": "Online AP Human Geography", "T20011": "World History 1 Ancient History", "T22012": "World History 2 Medieval History", "T24011": "World History 3 Modern History", "T26012": "World History 4  20th Century", "T280A1": "AP World History", "T290A1": "AP European History", "T830W1": "Humanities 1", "T840W2": "Humanities 2", "T510W2": "Military History", "T40011": "US History", "T400M1": "Online US History", "T460A1": "AP US History", "T48011": "American Studies", "T530W2": "Modern American Social History", "T72012": "Minorities in American Society", "T520W1": "Urban History", "T30011": "American Government", "T300N1": "Blended American Government (NNHS Only)", "T300M1": "Online American Government", "T360A2": "AP US Government & Politics", "T380A1": "AP Comparative Government & Politics", "T65011": "Legal Issues in American Society", "T59012": "Peace & Conflict Studies", "T60011": "Economics", "T630A1": "AP Micro Economics", "T620A2": "AP Macro Economics", "T74011": "Sociology", "T76011": "Intro to Psychology", "T760N1": "Blended Intro to Psychology (NCHS Only)", "T760M1": "Online Psychology", "T770A1": "AP Psychology", "T980N1": "Humanities Capstone  Blended Learning ", "D10011": "Driver Education", "H10011": "Health", "H100N1": "Blended Health (NCHS Only)", "H100M1": "Online Health", "H50011": "Advanced Health", "P10011": "PE 1", "P20011": "PE 2", "P24011": "PE 2  Leadership", "P40011": "PE 3/4", "P75011": "Lifeguard Training", "P50011": "PE Fitness", "P63011": "Sports Medicine 1", "P63511": "Sports Medicine 2", "P42011": "Adventure 1", "P42512": "Adventure 2", "P44011": "Strength & Performance", "P47012": "Senior Wellness", "P87011": "Adapted PE Leaders", "P88511": "Sensory PE Leaders (NCHS Only)", "P61011": "Junior PE Leaders", "P62011": "Senior PE Leaders", "W21011": "Chinese-Mandarin 1", "W22011": "Chinese-Mandarin 2", "W23011": "Chinese-Mandarin 3", "W240W1": "Chinese-Mandarin 4", "W250A1": "AP Chinese Lang & Cult", "W270W1": "Modern Chinese Literature", "W31011": "French 1", "W32011": "French 2", "W33011": "French 3", "W340W1": "French 4", "W360A1": "AP French Language and Culture", "W41011": "German 1", "W42011": "German 2", "W43011": "German 3", "W440W1": "German 4", "W450E1": "German 5", "W61011": "Latin 1", "W62011": "Latin 2", "W630W1": "Honors Latin 3/4", "W81011": "Spanish 1", "W82011": "Spanish 2", "W83011": "Spanish 3", "W840W1": "Spanish 4", "W850E1": "Spanish 5", "W85511": "Spanish Language & Culture for Spanish Speaker", "W860A1": "AP Spanish Language & Culture", "W870A1": "AP Spanish Literature", "W90011": "Spanish Language & Culture 1", "W91011": "Spanish Language & Culture 2", "W92011": "Spanish Language & Culture 3", "W980N1": "Humanities Capstone-Blended Learning", "C80091": "EL Beginning", "C81091": "EL Intermediate", "C81591": "EL Advanced Intermediate", "C82091": "EL Advanced", "C83091": "EL Tutorial", "C830V1": "Bilingual Tutorial", "B12091": "Tech Edge", "B70091": "Consumer Economics", "C12091": "English 1", "H10091": "Health", "M19091": "Algebra 1", "M34091": "Geometry", "S25091": "Principles of Biology & Chemistry", "S31091": "Biology", "S50091": "Chemistry", "T10091": "World Cultures", "T30091": "American Government", "T40091": "US History"}



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
        for person in query_results:
        #Checks if the search is in the person's name; if it is they are added to the list of results
            results.append((person["id"], person["name"]))#Here he add a tuple containing the persons name and id; This is because we need to display the name and need the id to genorate URLS
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
                schedule_names.append(convert[result["p"+str(num+1)][:result["p"+str(num+1)].index("-")]])
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
                 "schedule_ids":[result["school"][1:2]+result["p"+str(num+1)] for num in range(8)],
                 "schedule_names":schedule_names}
        mongo.db.users.insert(data)
        
        for clas1 in data["schedule_ids"]:
            if mongo.db.clas.find({'id': clas1}).count() > 0:
                before = mongo.db.clas.find_one_or_404({"id":clas1})
                before["students_id"].append(data["id"])
                before["students_name"].append(data["name"])
                mongo.db.clas.update_one({"id":clas1}, {"$set":before})
                       
            else:
                num = data["schedule_ids"].index(clas1)
                data1 = {"id":clas1,
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
   
          

