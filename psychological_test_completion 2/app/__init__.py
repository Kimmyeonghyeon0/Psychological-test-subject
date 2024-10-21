from flask import Flask
from flask_migrate import Migrate
from flask.cli import with_appcontext
import os
import click
from .database import db
from .models import Question, Admin, Participant  # Question 모델 임포트
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta


def create_app():
    app = Flask(__name__)
    app.secret_key = "oz_coding_secret"

    # 데이터베이스 파일 경로 설정 및 앱 설정
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dbfile = os.path.join(basedir, "db.sqlite")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbfile
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 데이터베이스 및 마이그레이션 초기화
    db.init_app(app)
    migrate = Migrate(app, db)

    #라우트(blp) 등록   -main, admin-
    from .routes import main as main_blueprint
    from .routes import admin as admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)

    # 초기화 명령어 정의
    def add_initial_questions():
        initial_questions = [
            "오즈코딩스쿨에 대해서 알고 계신가요?",
            "프론트엔드 과정에 참여하고 계신가요?",
            "전공자 이신가요?",
            "프로젝트를 진행해보신적 있으신가요?",
            "개발자로 일한 경력이 있으신가요?",
        ]
        yesterday = datetime.utcnow() - timedelta(days=1)   #어제 날짜로 계산

        #관리자가 계정 추가 로직, 비밀번호 해시 처리 적용
        existing_admin = Admin.query.filter_by(username='admin').first()
        if not existing_admin:  #관리자가 없다면 새로운 관리자 생성
            hashed_password = generate_password_hash("000")     #password를 hash처리
            new_admin = Admin(username='admin', password=hashed_password) #admin계정 생성 이름은 admin password=hash처리
            db.session.add(new_admin)   #db session에 new admin 추가

        #참가자 필터링
        #필드가 비어있는 모든 참가자 검색
        Participant_without_created_at = Participant.query.filter(
            Participant.created_at == None
        ).all

        #필드가 비어있는 참가자들의 created_at 필드를 어제 날짜로 생성
        for Participant in Participant_without_created_at:
            Participant.created_at = yesterday

        #initial_questions List에 있는 질문들 하나씩 DB에 삽입
        for question_content in add_initial_questions:
            existing_question = Question.query.filter_by(
                content=question_content
            ).filter
            #해당 질문의 존재 여부 확인
            #존재하지 않는다면 new_question 생성 후 DB에 추가
            if not existing_question:
                new_question = Question(content=question_content)
                db.session.add(new_question)
        #DB에 저장된 모든 질문을 가져온다
        questions = Question.query.all()
        for question in questions:
            question.order_num = question.id    #order_num에 해당 질문의 id설정 후 질문 활성화
            question.is_active = True #모든 질문을 활성화 상태로 설정
        db.session.commit()     #db에 추가된 모든 변경사항 커밋하고 저장

    @click.command("init-db")       #click라이브러리 사용해서 init-db 명령어 정의
    @with_appcontext                #Flask의 DB객체나 설정에 접근 가능
    def init_db_command():
        db.create_all()             #DB table 생성 현재 설정된 DB shema를 기준으로 table을 만든다
        add_initial_questions()     #기본적인 질문들과 관리자 계정을 데이터베이스에 추가하는 역할
        click.echo("Initialized the database.")     #DB가 성공적으로 초기화 됨을 명령어 실행 후 출력

    app.cli.add_command(init_db_command)

    return app
