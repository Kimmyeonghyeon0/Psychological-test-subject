from .database import db
from datetime import datetime

class Participant(db.Model):
    __tablename__ = "Participant"
    id = db.Column(db.Integer, primery_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primery_key=True)
    username = db.Column(db.string(50))
    password = db.Column(db.string(50))

class Question(db.Model):
    __tablename__ = "question"
    id  = db.Column(db.Integer, primery_key=True)
    content = db.Column(db.String(255))
    order_num = db.Column(db.Integer, defult=0)     #질문의 순서가 중요하지 않은 질문의 초기상태 =0 (변경 가능)
    is_active = db.Column(db.Boolean, defult=True)  #질문의 활성화 여부

class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    #Participant, Question 외래키 사용
    Participant_id = db.Column(db.Integer, db.ForeignKey("Participant_id"))
    Question_id = db.Column(db.Integer, db.ForeignKey("Question_id"))
    chosed_answer = db.COlumn(db.string(255))       #참가자가 선택한 답변

    #관계설정
    participant = db.relationship("Participant", backref="quizzes")
    #참가자와 퀴즈간의 관계 (응답한 모든 퀴즈 참조)
    question = db.relationship("Question", backref="quizzes")
    #질문과 퀴즈간의 관계 (질문에 대한 모든 퀴즈결과 참조)