import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
import smtplib


EMAIL = os.environ.get("EMAIL_ADD")
PASSWORD = os.environ.get("EMAIL_PASS")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)


class EmailForm(FlaskForm):
    email = StringField("Email", validators=[Email(), Length(max=250)])
    name = StringField("Name", validators=[DataRequired(), Length(max=250)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=3000)])
    send = SubmitField("Send Message")


@app.route("/", methods=["GET", "POST"])
def home():
    email_form = EmailForm()
    if email_form.validate_on_submit():
        send_email(email_form.email.data, email_form.name.data, email_form.message.data)
        flash("Message sent. Expect a response within 24-48 hrs.")
        return redirect(url_for('home')+"#contact")
    return render_template("index.html", form=email_form)


def send_email(email, name, message):
    email_message = f"Subject:New Message\n\nEmail: {email}\nName: {name}\nMessage:\n\n{message}"
    with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(EMAIL, EMAIL, email_message)


if __name__ == "__main__":
    app.run()
