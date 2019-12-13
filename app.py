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
convert = {"M40022":"Algebra 2 Core","C25022":"English 3","J23012":"Vetinary Science","T40022":"US History","S31022":"Biology","T23012":"World History","915212":"Link Lunch","N54012":"Intro to Mixed Choir","CJ23012":"Veterinary Science","CS31022":"Biology","936012":"Study Hall", "M430N2":"Blended Algebra 2", "T360A2":"AP Gov", "S560A2":"AP Chemistry", "930812":"AP Chemistry Lunch","925612":"Link Lunch", "926612":"Link Leader Lunch", "A":"Missing Class", "923012":"Link Lunch","910012":"Lunch","910012":"Lunch","C60032": "Academic Reading", "C61032": "Sophomore Reading Seminar", "C62032": "Junior/Senior Reading Seminar", "B10012": "Introduction to Business", "B120B2": "Tech Edge", "B160B2": "Tech Edge +", "B240B2": "Accounting 1", "B260C2": "Honors College Accounting", "B30012": "Marketing", "B32012": "Advanced Marketing (NNHS only)", "B320N2": "Blended Advanced Marketing (NCHS only)", "B34012": "Advertising", "B37012": "Business INCubator", "B38012": "Business Law", "B380M2": " Online Business Law", "B40012": "International Business", "B44012": "Computer Programming 1", "B440N2": "Blended Computer Programming 1 (NCHS only)", "B46012": "Computer Programming 2", "B48012": "Game Design", "B480M2": "Online Game Design", "B52012": "Web Page Design", "B520M2": "Online Web Page Design", "B54012": "Advanced Web Page Design", "B560A2": "AP Computer Science A", "B580W2": "Software Engineering 1", "B590W2": "Software Engineering 2", "B60012": "Yearbook Production (NNHS only)", "B62012": "Digital Publishing & Design", "B64012": "Animation & Multimedia", "B70012": "Consumer Economics", "B700N2": "Blended Consumer Economics (NNHS only)", "B700M2": " Online Consumer Economics", "B87012": "CTE Internship", "B980N2": "Blended STEM  Inquiry and Research Capstone", "F100D2": "Fashion Merchandising", "F140D2": "Fashion Design", "F18012": "Food Science", "F22012": "Culinary Arts & Nutrition 1", "F26012": "Culinary Arts & Nutrition 2", "F27012": "Culinary Arts & Nutrition 3", "F30012": "Senior Foods", "F34012": "Interior Design", "F42012": "Human Growth & Development", "F460B2": "Early Childhood Education 1", "F500B2": "Early Childhood Education 2", "F54012": "Adult Living/Personal Relationships (at NNHS only)", "F580D2": "Intro to Teaching 1", "F620D2": "Intro to Teaching 2", "F66012": "Intro to Health Occupations", "F700D2": "Health Occupations", "F87012": "CTE Internship", "F980N2": "Blended STEM  Inquiry and Research Capstone", "J100B2": "Introduction to Horticulture", "J140D2": "Floral Design", "J160D2": "Advanced Floral Design", "J18012": "Greenhouse Crop Production", "J20012": "Companion Animal Biology", "J22012": "Advanced Companion Animal Biology", "J280J2": "Supervised Agriscience Experience ", "J30012": "Graphics 1", "J32012": "Graphics 2", "J34012": "Graphics 3", "J400D2": "Basic Electricity", "J420D2": "Electronics", "J460D2": "Computer Repair/A+ Cert", "J480D2": "LANWAN/Network+Cert", "J50012": "Woodworking 1 / Workmanship", "J52012": "Woodworking 2 / Craftmanship", "J54012": "Woodworking 3 / Cabinetry", "J56012": "Drafting 1  AutoCad 2D", "J580D2": "Drafting 2  AutoCad 3D", "J60012": "Pre-Engineering Drafting", "J62012": "Architectural Drafting", "J64012": "Research & Design", "J70012": "Automotive Maintenance", "J72012": "Automotive Mechanics", "J74012": "Automotive Servicing", "J87012": "CTE Internship", "J980N2": "Blended STEM Inquiry & Research Capstone", "J760D2": "Autobody Repair & Refinishing", "J780D2": "Construction Trades", "F780D2": "Cosmetology", "J820D2": "Criminal Justice", "F860D2": "Professional Cooking, Baking & Service", "J800D2": "Fire Science", "F800D2": "Medical & Health Careers", "J790D2": "HVAC & Refrigeration", "F820D2": "Nursing Assistant Training Program", "C12012": "English 1", "C120H2": "Honors English 1", "C17012": "English 2", "C170H2": "Honors English 2", "C19012": "English 2 : Journalism", "C190H2": "Honors English 2: Journalism", "C20012": "Speech Communication", "C25012": "English 3", "C250H2": "Honors English 3", "C27012": "American Studies", "C280A2": "AP Language & Composition", "C280N2": "Blended AP Language & Composition (NCHS only)", "C34012": "Writing Styles & Forms", "C37012": "Senior Rhetoric", "C370H2": "Honors Senior Rhetoric", "C39012": "Creative Writing", "C40012": "20th Century Literature", "C410W2": "English Literature", "C42012": "Traditions in Communication", "C435W2": "Themes in Western Literature & Art", "C45012": "World Literature", "C455M2": "Online African American Literature", "C46012": "Literary Themes", "C480A2": "AP Literature & Composition", "C49012": "Yearbook Production", "C50512": "Advanced Media Lab", "C53012": "Advanced Speech", "C56012": "Mass Media", "C57012": "Film as Literature", "C58012": "Film Production", "C59012": "Newspaper Production (NCHS only)", "C980N2": "Humanities Capstone-Blended Learning", "A16012": "Drawing 1", "A19012": "Drawing 2", "A20012": "Drawing 3", "A21012": "Drawing 4", "A22012": "Painting 1", "A23012": "Painting 2", "A27012": "Painting 3", "A28012": "Painting 4", "A37012": "Ceramics 1", "A38012": "Ceramics 2", "A39012": "Ceramics 3", "A40012": "Ceramics 4", "A43012": "Jewelry/Metals 1", "A44012": "Jewelry/Metals 2", "A45012": "Jewelry/Metals 3", "A46012": "Jewelry/Metals 4", "A63012": "Sculpture 1", "A64012": "Sculpture 2", "A50012": "Photography 1 (Traditional)", "A51012": "Photography 2 (Traditional)", "A52012": "Photography 3", "A53012": "Photography 4", "A54012": "Photography 2 (Digital)", "A55512": "Film & Video Arts", "A57012": "Digital Art 1", "A58012": "Digital Art 2", "A59012": "Digital Art 3", "A60012": "Digital Art 4", "A910A2": "AP Art History", "A930A2": "AP Studio Art 2D", "A935A2": "AP Studio Art 2D Design", "A940A2": "AP Studio Art 3D", "A95012": "Adapted Art & Design Leaders", "N10012": "Introduction to Band", "N12012": "Intermediate Band", "N15012": "Intermediate/Advanced Band (NCHS Only)", "N17012": "Advanced Band", "N30012": "Introduction to Orchestra", "N31012": "Intermediate Orchestra (NNHS Only)", "N32012": "Intermediate/Advanced Orchestra", "N34012": "Advanced Orchestra", "N38012": "Introduction to Female Choir", "N46012": "Advanced Female Choir (NNHS Only)", "N50012": "Introduction to Male Choir", "N58012": "Intermediate Mixed Choir (NCHS Only)", "N62012": "Advanced Mixed Choir", "N66012": "Music Theory 1", "N660M2": "Online Music Theory 1", "N700A2": "AP Music Theory", "N74012": "Music Appreciation", "N980W2": "Music Capstone", "E10012": "Acting", "E13012": "Advanced Acting", "E16012": "Play Production", "M10012": "Introduction to Algebra", "M16012": "Survey of Math Topics", "M19012": "Algebra 1", "M190N2": "Blended Algebra 1 ", "M25012": "Algebra 1 Support", "M28012": "Algebra 1 w/Geometry", "M31012": "Geometry Core", "M34012": "Geometry", "M340N2": "Blended Geometry (NCHS only)", "M340M2": "Online Geometry", "M340H2": "Honors Geometry", "M40012": "Algebra 2 Core", "M43012": "Algebra 2", "M430M2": "Online Algebra 2", "M430H2": "Honors Algebra 2", "M50012": "Discrete Math", "M51012": "Statistics", "M52012": "Business Precalculus", "M520N2": "Blended Business Precalculus", "M53012": "Precalculus", "M530H2": "Honors Precalculus", "M600A2": "AP Calculus AB", "M610A2": "AP Calculus BC", "M640W2": "Multivariable Calculus (NCHS Only)", "M650E2": "Multivariable Calculus w/Lin Algebra (NNHS Only)", "M680A2": "AP Statistics", "M980N2": "Blended STEM Capstone ", "S25012": "Principles of Biology & Chemistry", "S50012": "Chemistry", "S500H2": "Honors Chemistry", "S31012": "Biology", "S370H2": "Honors Biology", "S59012": "Physics", "S600A2": "AP Physics 1", "S530W2": "Advanced Chemistry", "S430W2": "Anatomy & Physiology", "S430N2": "Blended Anatomy & Physiology (NNHS only)", "S19012": "Astronomy", "S460W2": "Biotechnology", "S16012": "Physical Geology", "S13012": "Weather & Environment", "S400A2": "AP Biology", "T280A2": "AP Chemistry", "S220A2": "AP Environmental Science", "S630A2": "AP Physics 2", "S680A2": "AP Physics C", "S65012": "Research & Design", "S980N2": "Blended STEM Capstone ", "S200M2": "Online Sustainable Energy", "T10012": "World Cultures", "T79012": "Comparative Religions", "T81012": "Cultural Anthropology", "T150A2": "AP Human Geography", "T150M2": "Online AP Human Geography", "T20012": "World History 1 Ancient History", "T22012": "World History 2 Medieval History", "T24012": "World History 3 Modern History", "T26012": "World History 4  20th Century", "T280A2": "AP World History", "T290A2": "AP European History", "T830W2": "Humanities 1", "T840W2": "Humanities 2", "T510W2": "Military History", "T40012": "US History", "T400M2": "Online US History", "T460A2": "AP US History", "T48012": "American Studies", "T530W2": "Modern American Social History", "T72012": "Minorities in American Society", "T520W2": "Urban History", "T30012": "American Government", "T300N2": "Blended American Government (NNHS Only)", "T300M2": "Online American Government", "T360A2": "AP US Government & Politics", "T380A2": "AP Comparative Government & Politics", "T65012": "Legal Issues in American Society", "T59012": "Peace & Conflict Studies", "T60012": "Economics", "T630A2": "AP Micro Economics", "T620A2": "AP Macro Economics", "T74012": "Sociology", "T76012": "Intro to Psychology", "T760N2": "Blended Intro to Psychology (NCHS Only)", "T760M2": "Online Psychology", "T770A2": "AP Psychology", "T980N2": "Humanities Capstone  Blended Learning ", "D10012": "Driver Education", "H10012": "Health", "H100N2": "Blended Health (NCHS Only)", "H100M2": "Online Health", "H50012": "Advanced Health", "P10012": "PE 1", "P20012": "PE 2", "P24012": "PE 2  Leadership", "P40012": "PE 3/4", "P75012": "Lifeguard Training", "P50012": "PE Fitness", "P63012": "Sports Medicine 1", "P63512": "Sports Medicine 2", "P42012": "Adventure 1", "P42512": "Adventure 2", "P44012": "Strength & Performance", "P47012": "Senior Wellness", "P87012": "Adapted PE Leaders", "P88512": "Sensory PE Leaders (NCHS Only)", "P61012": "Junior PE Leaders", "P62012": "Senior PE Leaders", "W21012": "Chinese-Mandarin 1", "W22012": "Chinese-Mandarin 2", "W23012": "Chinese-Mandarin 3", "W240W2": "Chinese-Mandarin 4", "W250A2": "AP Chinese Lang & Cult", "W270W2": "Modern Chinese Literature", "W31012": "French 1", "W32012": "French 2", "W33012": "French 3", "W340W2": "French 4", "W360A2": "AP French Language and Culture", "W41012": "German 1", "W42012": "German 2", "W43012": "German 3", "W440W2": "German 4", "W450E2": "German 5", "W61012": "Latin 1", "W62012": "Latin 2", "W630W2": "Honors Latin 3/4", "W81012": "Spanish 1", "W82012": "Spanish 2", "W83012": "Spanish 3", "W840W2": "Spanish 4", "W850E2": "Spanish 5", "W85512": "Spanish Language & Culture for Spanish Speaker", "W860A2": "AP Spanish Language & Culture", "W870A2": "AP Spanish Literature", "W90012": "Spanish Language & Culture 1", "W91012": "Spanish Language & Culture 2", "W92012": "Spanish Language & Culture 3", "W980N2": "Humanities Capstone-Blended Learning", "C80092": "EL Beginning", "C81092": "EL Intermediate", "C81592": "EL Advanced Intermediate", "C82092": "EL Advanced", "C83092": "EL Tutorial", "C830V2": "Bilingual Tutorial", "B12092": "Tech Edge", "B70092": "Consumer Economics", "C12092": "English 1", "H10092": "Health", "M19092": "Algebra 1", "M34092": "Geometry", "S25092": "Principles of Biology & Chemistry", "S31092": "Biology", "S50092": "Chemistry", "T10092": "World Cultures", "T30092": "American Government", "T40092": "US History"}


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
        for code in data["schedule_ids"]:
            code.replace(" ", "")
        
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
   
          

