from app import app

from flask import request, render_template, flash, redirect
from app.forms import ContactForm, flash_errors
import os
import smtplib



@app.route("/")
def index():

    return render_template("public/index.html")

@app.route("/contact", methods=("GET", "POST"))
def contact():
    form = ContactForm()
    flash_errors(form)
    MAIL_PASS = request.environ['MAIL_PASS']
    if form.validate_on_submit():
        sender = "%s <%s>" % (form.name.data, form.email.data)
        subject = "Asunto: %s, %s" % (form.subject.data , form.email.data)
        message = "From: %s, \n\n %s, \n\n %s" % (
            sender, subject, form.body.data)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("webpuppys@gmail.com", MAIL_PASS)
        server.sendmail("webpuppys@gmail.com",
                        "innovacionespuppys@hotmail.com", message.encode('utf-8'))

        flash("Tu mensaje ha sido enviado")
        return redirect("/contact")
    else:
        flash_errors(form)
    return render_template("public/contact.html", form=form)

@app.route("/about")
def about():

    return render_template("public/about.html")

@app.route("/products")
def products():

    return render_template("public/products.html")

@app.route("/services")
def services():

    return render_template("public/services.html")
