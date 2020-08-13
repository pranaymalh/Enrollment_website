from app import app,db,api
from flask import render_template,request,Response,json,flash,redirect,url_for,session,jsonify
from app.models import User,Course,Enroll
from app.forms import LoginForm,RegisterForm
from flask_restplus import Resource

#######################################################

@api.route("/api","/api/")
class GetAndPost(Resource):
	def get(self):
		return jsonify(User.objects.all())

	def post(self):
		data=api.payload
		user=User(user_id=data["user_id"],email=data["email"],first_name=data["first_name"],last_name=data["last_name"])
		user.set_password(data["password"])
		user.save()
		return jsonify(User.objects(user_id=data["user_id"]))

@api.route("/api/<idx>")
class GetUpdateDelete(Resource):
	def get(self,idx):
		return jsonify(User.objects(user_id=idx))

	def put(self,idx):
		data=api.payload
		User.objects(user_id=idx).update(**data)
		return jsonify(User.objects(user_id=data["user_id"]))

	def delete(self,idx):
		User.objects(user_id=idx).delete()
		return jsonify("User deleted!")
#######################################################

coursesData=[{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
	return render_template('index.html',index=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="2019"):
	classes=Course.objects.order_by("-courseID")
	return render_template('courses.html',courseData=classes,courses=True,term=term)

@app.route("/login",methods=["GET","POST"])
def login():
	if session.get('username'):
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		email=form.email.data
		password=form.password.data
		user=User.objects(email=email).first()
		if user and user.get_password(password):
			flash(f"{user.first_name},You are successfully logged in!","success")
			session["user_id"]=user.user_id
			session["username"]=user.first_name
			return redirect("/index")
		else:
			flash("Sorry! something went wrong!","danger")
	return render_template('login.html',title="Login",form=form,login=True)
@app.route("/logout")
def logout():
	session["user_id"]=False
	session.pop('username',None)
	return redirect(url_for('login'))

@app.route("/register",methods=["GET","POST"])
def register():
	if session.get('username'):
		return redirect(url_for('index'))
	form=RegisterForm()
	if form.validate_on_submit():
		user_id=User.objects.count()
		user_id+=1
		email=form.email.data
		password=form.password.data
		first_name=form.first_name.data
		last_name=form.last_name.data
		user=User(user_id=user_id,email=email,first_name=first_name,last_name=last_name)
		user.set_password(password)
		user.save()
		flash("You are successfully registered!","success")
		return redirect("/index")
	return render_template('register.html',title="Register",form=form,register=True)

@app.route("/enrollment",methods=["GET","POST"])
def enrollment():
	if not session.get("username"):
		return redirect(url_for('login'))
	courseID=request.form.get('courseID')
	courseTitle=request.form.get('title')
	user_id=session.get('user_id')
	if courseID:
		if Enroll.objects(user_id=user_id,courseID=courseID):
			flash(f"Oops! you are already registered in this course","danger")
		else:
			Enroll(user_id=user_id,courseID=courseID).save()
			flash("You are successfully enrolled","success")
	classes=list(User.objects.aggregate(*[
			    {
			        '$lookup': {
			            'from': 'enroll', 
			            'localField': 'user_id', 
			            'foreignField': 'user_id', 
			            'as': 'r1'
			        }
			    }, {
			        '$unwind': {
			            'path': '$r1', 
			            'includeArrayIndex': 'r1_id', 
			            'preserveNullAndEmptyArrays': False
			        }
			    }, {
			        '$lookup': {
			            'from': 'course', 
			            'localField': 'r1.courseID', 
			            'foreignField': 'courseID', 
			            'as': 'r2'
			        }
			    }, {
			        '$unwind': {
			            'path': '$r2', 
			            'preserveNullAndEmptyArrays': False
			        }
			    }, {
			        '$match': {
			            'user_id': user_id
			        }
			    }, {
			        '$sort': {
			            'courseID': 1
			        }
			    }
			]))
	return render_template('enrollment.html',enrollment=True,classes=classes,title="Enrollment")

'''@app.route("/api")
@app.route("/api/<idx>")
def api(idx=None):
	if idx==None:
		jdata=coursesData
	else:
		jdata=coursesData[int(idx)]
	return Response(json.dumps(jdata),mimetype="application/json")'''

@app.route("/user")
def user():
	User(user_id=1,first_name="Pranay",last_name="Malhan",email="pranay1998@xyz.com",password="helloworld").save()
	User(user_id=2,first_name="Pulkit",last_name="Chauhan",email="pulkit1998@xyz.com",password="helloearth").save()
	users=User.objects.all()
	return render_template("user.html",users=users)