from flask import render_template, url_for, flash, redirect, request, jsonify
from flasksite import application, db
from flasksite.models import Store, Product
from flasksite.render import render_plot
from flasksite.insert_data import insert_data
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route("/")
@application.route("/home", methods=['POST', 'GET'])
def home():
    stores = Store.query.all()
    products = Product.query.all()
    if request.method == 'POST':
        term = request.form['time']
        selected_store = request.form['selected_store']
        selected_product = request.form['selected_product']
        if term == "":
            flash("Enter the time period", "danger")
            return render_template('home.html')
        else:
            render_plot(int(term),int(selected_store),int(selected_product))
            i = 0
            with open(os.getcwd() + "/flasksite/templates/plot.html", "w") as w:
                w.write('{% extends "layout.html" %} {% block content %}')
                with open(os.getcwd() + "/flasksite/templates/temp-plot.html", "r") as f:
                    for line in f:
                        if i < 3:
                            i += 1
                        elif i > 29:
                            break
                        else:
                            i += 1
                            w.write(line)
                w.write('{% endblock content %}')
            return render_template('plot.html')
    return render_template('home.html', stores=stores, products=products)

@application.route('/render')
def render():
    return render_template('plot.html', title='Render')

@application.route('/upload')
def redirect_upload():
    return render_template('upload.html')

@application.route('/uploadFile', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template('home.html')
        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], 'sales_data.csv'))
                insert_data()
                os.remove(os.getcwd() + "/flasksite/data/sales_data.csv")
                flash('File successfully uploaded')
                return render_template('home.html')
            else:
                flash('Allowed file types is csv')
                return render_template('home.html')