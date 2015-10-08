from sqlalchemy.orm import sessionmaker
from models import Question, db_connect, create_deals_table

class QuizPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        question = Question(
        	question_number=item.get('question_number', ''),
        	question=item.get('question', ''),
            possible_answers=item.get('possible_answers', ''),
            correct_answer=item.get('correct_answer', ''),
            explanation=item.get('explanation', ''),
            section=item.get('section', ''),
            type_of_quiz=item.get('type_of_quiz', ''),
                  )

        existing_query = session.query(Question).filter(
            Question.question_number == question.question_number).first()

        if existing_query:
            question = existing_query
            question.question_number = item.get('question_number', '')
            question.question = item.get('question', '')
            question.possible_answers = item.get('possible_answers', '')
            question.correct_answer = item.get('correct_answer', '')
            question.explanation = item.get('explanation', '')
            question.section = item.get('section', '')
            question.type_of_quiz = item.get('type_of_quiz', '')

        else:
            session.add(question)
        session.commit()
        session.close()

        return item