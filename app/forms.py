from app import app

from flask import flash
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, Email


class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Nombre', [
        InputRequired("Por favor ingresa tu nombre")])
    email = StringField('Email', [
        Email(message=('No es una direccion de correo valida.')),
        InputRequired("Por favor ingresa tu email")])
    subject = StringField('Asunto', [
        InputRequired("Por favor ingresa el asunto")])
    body = TextAreaField('Mensaje', [
        InputRequired("Por favor ingresa un mensaje"),
        Length(min=4, message=('El mensaje es muy corto.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Enviar')

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"%s" % (error), 'error')
