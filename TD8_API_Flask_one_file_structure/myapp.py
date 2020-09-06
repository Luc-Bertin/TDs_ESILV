from flask import (Flask,
                   make_response,
                   redirect,
                   render_template,
                   abort, url_for, session)

from flask_script import Manager
from flask_bootstrap import Bootstrap

from werkzeug.exceptions import HTTPException

from collections import OrderedDict


from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_wtf import Form

app = Flask(__name__, template_folder="templates")
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def bonjour():
    return "test"

@app.route('/login/')
def myfonction():
	return render_template("autre_page.html")


app.config["SECRET_KEY"] = "randomstring"


class MyForm(Form):
	name = StringField("Name", validators=[DataRequired()])
	#age = IntegerField("Age", validators= [Length(min=13, max=19), DataRequired()])
	submit = SubmitField("Submit")

@app.route('/test/<name>', methods=['GET', 'POST'])
def test(name):
	name="Unknown"
	form = MyForm()
	if form.validate_on_submit():
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('test', name=session.get('name')))
	
	contenu_html = "<h1> Salut toi ;) </h1>"
	
	dico = OrderedDict({
		"tâche1": "Faire la vaisselle",
		"tâche2": "Faire le ménage",
		"tâche3": "écouter Monsieur Bertin"
		})
	# presentation rendered 
	return render_template("index.html", var1=session.get("name"), var2=contenu_html, dico=dico, form=form)


@app.route("/voiciunredirect/")
def unefonction():
    return redirect("myfonction")


@app.route('/user/<name>')
def trouve(name):
    # -----
    return "<h1>Hello <i>" + name + "</i></h1>"

#@app.route('/<path:nompath>')
# def test2(nompath):
#	return "<h1>Hello</h1>"

@app.route('/<path:nompath>')
def error_404(nompath):
	abort(404, "The page {} is not found".format(nompath))
	#message = "Page {} not found".format(nompath)
	#raise HTTPException(message, response=404)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', error_message=e), 404



if __name__ == "__main__":
    manager.run()
