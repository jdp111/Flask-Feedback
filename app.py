
from flask import Flask, session, render_template, redirect, request, flash
from models import db, connect_db, User, Feedback
from forms import Signup, Login, SubmitFeedBack

app = Flask(__name__)
app.config['SECRET_KEY'] = "allcriticismwillbethrowninthetrash"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def redirects():
    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def signupRoute():
    """either registers or shows registration form"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = Signup()

    if form.validate_on_submit():
        UN = form.username.data
        PW = form.password.data
        FN = form.first_name.data
        LN = form.last_name.data
        EM = form.email.data

        newUser = User.register(UN,PW,FN,LN,EM)
        db.session.add(newUser)
        db.session.commit()
        newUser.login(form.password.data)
        
        return redirect(f"/users/{session['username']}")

    return render_template('reg_log.html',form_obj = form, header = "Register")


@app.route('/login', methods = ['POST', 'GET'])
def loginRoute():
    if "username" in session:
        flash('you are already logged in')
        return redirect(f"/users/{session['username']}")

    form = Login()

    if form.validate_on_submit():
        UN = form.username.data
        PW = form.password.data

        user = User.query.get(UN)

        if user:
            successfulLogin = user.login(PW)
            if successfulLogin:
                flash("successfully logged in")
                return redirect (f"/users/{UN}")
            flash("password is incorrect")
            return redirect('/login')
        flash('username does not exist')
        return redirect('/login')
    
    return render_template('reg_log.html',form_obj=form, header = "Login")


@app.route('/logout', methods = ['POST'])
def logoutRoute():
    """logs out (removes username from session)"""
    if "username"in session:
        session.pop("username")
    return redirect('/')


@app.route('/users/<id>')
def get_user(id):
    """gets a user info and displays feedback from a user"""

    if "username" in session:
        if not session['username'] == id:
            return redirect(f"/users/{session['username']}")
        
        currUser = User.query.get(id)
        allFB = currUser.feedback
        return render_template('user_info.html', user = currUser, feedback = allFB, header = "User Information")
    
    return redirect("/login")


@app.route('/users/<id>/delete', methods = ['POST'])
def del_user(id):
    """deletes a user"""

    if "username" in session:
        if not session['username'] == id:
            return redirect(f"/users/{session['username']}")
        
        session.pop("username")
        currUser = User.query.get(id)
        db.session.delete(currUser)
        db.session.commit()

        return redirect("/register")


    return redirect("/login")

@app.route('/users/<UN>/feedback/add', methods = ['POST', 'GET'])
def addFeedback(UN):

    if "username" in session:
        if not session['username'] == UN:
            return redirect(f"/users/{session['username']}/add")
        
        form = SubmitFeedBack()

        if form.validate_on_submit():
            newC = form.content.data

            newFB = Feedback(content = newC, username = UN)
            db.session.add(newFB)
            db.session.commit()
            return redirect(f"/users/{UN}")
            
        return render_template("feedback.html", form_obj = form, header = "New Feedback")
    
    return redirect("/login")

@app.route('/feedback/<id>/update', methods = ['POST', 'GET'])
def editFeedback(id):
    currFB = Feedback.query.get(id)
    if "username" in session and currFB:
        UN = currFB.user.username
        if not session['username'] == UN:
            return redirect(f"/users/{session['username']}/add")
        
        form = SubmitFeedBack(obj = currFB)

        if form.validate_on_submit():
            newC = form.content.data
            currFB.content = newC
            db.session.commit()
            return redirect(f"/users/{UN}")
            
        return render_template("feedback.html", form_obj = form, header = "New Feedback")
    
    return redirect("/login")

@app.route('/feedback/<id>/delete', methods = ['POST'])
def deleteFeedback(id):
    currFB = Feedback.query.get(id)
    if "username" in session and currFB:
        UN = currFB.user.username
        if not session['username'] == UN:
            return redirect(f"/users/{session['username']}/add")
        db.session.delete(currFB)
        db.session.commit()
        return redirect(f"/users/{UN}")


    return redirect("/login")