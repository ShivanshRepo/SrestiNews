# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField, PasswordField
from wtforms.validators import DataRequired

class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
    ("top", "टॉप न्यूज़"),
    ("state", "राज्य-शहर"),
    ("national", "देश"),
    ("international", "विदेश"),
    ("Science&Tech", "विज्ञान और तकनीक"),
    ("cricket", "क्रिकेट"),
    ("sports", "स्पोर्ट्स"),
    ("bollywood", "बॉलीवुड"),
    ("education", "जॉब - एजुकेशन"),
    ("business", "बिज़नेस"),
    ("lifestyle", "लाइफस्टाइल"),
    ("spiritual", "जीवन मंत्र"),
])

    image = FileField('Image')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# app/forms.py

class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    youtube_url = StringField('YouTube URL', validators=[DataRequired()])


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
