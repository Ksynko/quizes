from scrapy import Item, Field


class QuizItem(Item):
	question_number = Field()
	question = Field()
	possible_answers = Field()
	correct_answer = Field()
	explanation = Field()
	# reference = Field()

	section = Field()
	type_of_quiz = Field()

    
