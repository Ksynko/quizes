import time

from scrapy.http import Request, HtmlResponse
from scrapy.spider import Spider
from scrapy.utils.response import open_in_browser
from scrapy.log import ERROR, WARNING, INFO, DEBUG

from pass_quiz import PassQuiz
from quiz.items import QuizItem

is_empty = lambda x, y=None: x[0] if x else y


class SurgeonsSpider(Spider):
    name = 'quiz'
    allowed_domains = ["elearning.surgeons.org"]
    start_urls = [
        'http://elearning.surgeons.org/course/view.php?id=127&section=1',
        'http://elearning.surgeons.org/course/view.php?id=127&section=2',
        'http://elearning.surgeons.org/course/view.php?id=127&section=3',
        'http://elearning.surgeons.org/course/view.php?id=127&section=4',
    ]
    search_url = 'http://elearning.surgeons.org/course/view.php?id=127'

    user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:35.0) Gecko'
                  '/20100101 Firefox/35.0')

    def __init__(self, *args, **kwargs):
        self.pq = PassQuiz()
        super(SurgeonsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        self.pq.driver.get(self.search_url)
        self.pq.sign_in()
        cookies = self.pq.driver.get_cookies()
        response = HtmlResponse(self.search_url, encoding='utf-8',
                                body=self.pq.get_body().encode('utf-8'))

        for section in self.start_urls:
            yield Request(
                url=section,
                cookies=cookies,
                callback=self.parse_section)

    def parse_section(self, response):

        tests = response.xpath(
            '//div[@class="activityinstance"]/a/@href').extract()
        for test in tests:
            yield Request(
                url=test,
                callback=self.parse_test)

    def parse_test(self, response):
        links = response.xpath(
            '//a[contains(text(),"Review")]/@href').extract()

        for link in links:
            yield Request(
                url=link,
                callback=self.parse_quiz)

    def parse_quiz(self, response):
        section = is_empty(
            response.xpath('//nav/ul/li[5]/a/text()').extract(), '')
        type_of_quiz = is_empty(
            response.xpath('//nav/ul/li[6]/a/text()').extract(), '')

        questions = response.xpath('//form/div/div')
        for q in questions:
            item = QuizItem()
            question = q.xpath(
                './/div[@class="qtext"]/text()').re('(\d+)-(.*)')
            if not question:
                continue
            answers = '|'.join(q.xpath(
                './/div[@class="answer"]/div/label/text()').extract())

            correct_answer = q.xpath(
                './/div[@class="rightanswer"]/text()').re(':(.*)')

            explanation = ' '.join(q.xpath(
                './/div[@class="generalfeedback"]/text()[2] | '
                './/div[@class="generalfeedback"]/p/text() | '
                './/div[@class="generalfeedback"]/p/i/text()').extract())
            if not explanation:
                explanation = is_empty(
                    q.xpath(
                        './/div[@class="generalfeedback"]/text()[1]'
                    ).extract())

            item['question_number'] = question[0]
            item['question'] = question[1]
            item['possible_answers'] = answers
            item['correct_answer'] = is_empty(correct_answer, '')
            item['explanation'] = explanation
            item['section'] = section
            item['type_of_quiz'] = type_of_quiz

            yield item
