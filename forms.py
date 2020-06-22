#!/usr/bin/python3.5
#-*-coding: utf-8 -*-
"""
Created on Wed Apr 12 19:23:42 2017

@author: david
"""

from wtforms import Form
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import BooleanField
from wtforms import StringField
from wtforms import HiddenField
from wtforms import TextAreaField
from wtforms import TextField
from wtforms.validators import ValidationError

def is_4bye(form, field):
    if field.data != 'bye':
        raise ValidationError('Must be bye')

     
class ContactForm(Form):
    name = TextField("Name",  [validators.DataRequired(),validators.length(max=50, message='enter your name')])
    email = TextField("Email",  [validators.DataRequired(),validators.Email()])
    subject = TextField("Subject",  [validators.DataRequired(),validators.length(max=100, message = 'enter a short description')])
    message = TextAreaField("Message",  [validators.DataRequired(),validators.length(max=1000, message = 'enter your message' )])
    submit = SubmitField("Send", [validators.DataRequired()])
 