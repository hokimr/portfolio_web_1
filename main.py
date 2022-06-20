from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, validators,SubmitField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

import os

load_dotenv()
mySecret = os.environ.get('MySecret')
secret_key = os.environ.get('SECRET_KEY')


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Qa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.String(250))
    q2 = db.Column(db.String(250))
    q3 = db.Column(db.String(250))
    q4 = db.Column(db.String(250))
    q5 = db.Column(db.String(250))
    q6 = db.Column(db.String(250))
    q7 = db.Column(db.String(250))
    q8 = db.Column(db.String(250))
    q9 = db.Column(db.String(250))
    q10 = db.Column(db.String(250))
    q11 = db.Column(db.String(250))
    q12 = db.Column(db.String(250))
    q13 = db.Column(db.String(250))
    q14 = db.Column(db.String(250))
    q15 = db.Column(db.String(250))

db.create_all()




class QuestionsForm(FlaskForm):
    q1 = StringField('"할머니, 할아버지가 가장 보고 싶었던 때는 언제인가요?"' , validators=[DataRequired()])
    q2 = StringField('"어릴 때 제일 좋아했던 놀이는 뭐예요?"', validators=[DataRequired()])
    q3 = StringField('"젋을 때 하지 못해서 후회했던 것이 있다면?"', validators=[DataRequired()])
    q4 = StringField('"20대로 돌아간다면 해보고 싶은것이 있나요?"', validators=[DataRequired()])
    q5 = StringField('"엄마/아빠로 산다는 것 힘들지 않나요?"', validators=[DataRequired()])
    submit = SubmitField('다음단계')

class QuestionsForm1(FlaskForm):
    q6 = StringField('"학창시절 별명은 뭐였어요?"' , validators=[DataRequired()])
    q7 = StringField('"엄마,아빠가 가족을 위해 포기하신것은 무엇인가요?"', validators=[DataRequired()])
    q8 = StringField('언제 외롭다고 느끼나요?', validators=[DataRequired()])
    q9 = StringField('가장 좋아하는 음식 3가지는요?', validators=[DataRequired()])
    q10 = StringField('제가 태어났을 때 기분이 어떠셨어요?', validators=[DataRequired()])
    q11 = StringField('"엄마/아빠(상대)의 매력 포인트는 무엇인가요?"' , validators=[DataRequired()])
    q12 = StringField('"첫 데이트는 어디에서 했어요?"', validators=[DataRequired()])
    q13 = StringField('요즘 혹시 걱정거리 있으세요?', validators=[DataRequired()])
    q14 = StringField('다시 태어나도 저의 부모님이 되어주실 건가요?', validators=[DataRequired()])
    q15 = StringField('마지막으로 하고싶은말을 자유롭게 써주세요!', validators=[DataRequired()])
    submit = SubmitField('다음단계')




@app.route('/')
def home():

    return render_template("index.html",mySecret=mySecret)




@app.route('/https://parentautobiography.herokuapp.com/questions',methods=["GET", "POST"])
def q_page_1():
    form = QuestionsForm()
    if request.method == 'POST':
        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        q4 = request.form.get('q4')
        q5 = request.form.get('q5')
        return redirect(url_for('q_page_2', q1=q1,q2=q2,q3=q3,q4=q4,q5=q5))

    return render_template("questions_1.html",form=form)

@app.route('/questions1',methods=["GET", "POST"])
def q_page_2():
    form = QuestionsForm1()


    if form.validate_on_submit():
        answer = Qa(
            q1=request.args.get('q1', None),
            q2=request.args.get('q2', None),
            q3=request.args.get('q3', None),
            q4=request.args.get('q4', None),
            q5=request.args.get('q5', None),
            q6=form.q6.data,
            q7=form.q7.data,
            q8=form.q8.data,
            q9=form.q9.data,
            q10=form.q10.data,
            q11=form.q11.data,
            q12=form.q12.data,
            q13=form.q13.data,
            q14=form.q14.data,
            q15=form.q15.data
        )

        db.session.add(answer)
        db.session.commit()
        user=answer.id


        return redirect(url_for("result",user=user))

    return render_template("questions_2.html",form=form)



@app.route('/result',methods=["GET", "POST"])
def result():
    user_id = request.args.get('user')
    result=Qa.query.get(user_id)
    answer=[]

    questions_list=['"할머니, 할아버지가 가장 보고 싶었던 때는 언제인가요?"',
                    '"어릴 때 제일 좋아했던 놀이는 뭐예요?"',
                    '"젋을 때 하지 못해서 후회했던 것이 있다면?"',
                    '"20대로 돌아간다면 해보고 싶은것이 있나요?"',
                    '"엄마/아빠로 산다는 것 힘들지 않나요?"',
                    '"학창시절 별명은 뭐였어요?"',
                    '"엄마,아빠가 가족을 위해 포기하신것은 무엇인가요?"',
                    '"언제 외롭다고 느끼나요?"',
                    '"가장 좋아하는 음식 3가지는요?"',
                    '"제가 태어났을 때 기분이 어떠셨어요?"',
                    '"엄마/아빠(상대)의 매력 포인트는 무엇인가요?"',
                    '"첫 데이트는 어디에서 했어요?"',
                    '"요즘 혹시 걱정거리 있으세요?"',
                    '"다시 태어나도 저의 부모님이 되어주실 건가요?"',
                    '"마지막으로 하고싶은말을 자유롭게 써주세요!"',]


    answer.append(result.q1)
    answer.append(result.q2)
    answer.append(result.q3)
    answer.append(result.q4)
    answer.append(result.q5)
    answer.append(result.q5)
    answer.append(result.q6)
    answer.append(result.q7)
    answer.append(result.q8)
    answer.append(result.q9)
    answer.append(result.q10)
    answer.append(result.q11)
    answer.append(result.q12)
    answer.append(result.q13)
    answer.append(result.q14)
    answer.append(result.q15)


    print(answer)


    return render_template("result.html",answer_list=answer,questions_list=questions_list,user_id=user_id,mySecret=mySecret)


@app.route('/contact')
def contact():

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
