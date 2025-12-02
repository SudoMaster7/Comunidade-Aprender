from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL

class ResourceForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL()])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    type = SelectField('Tipo', choices=[
        ('Vídeo', 'Vídeo'),
        ('Artigo', 'Artigo'),
        ('Ferramenta', 'Ferramenta'),
        ('Notícia', 'Notícia')
    ], validators=[DataRequired()])
    tags = StringField('Tags (separadas por vírgula)', validators=[DataRequired()])
    submit = SubmitField('Adicionar Recurso')
