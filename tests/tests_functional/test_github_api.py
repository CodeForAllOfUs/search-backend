import datetime

from django.test import TestCase # used for DB transactions to reset state between tests
from django.core.urlresolvers import reverse

from search.models import Tag

# Create your tests here.

def create_question(question_text, days):
    """
    Creates a question with the given `question_text` published the given
    number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class IndexViewTests(TestCase):
    def test_index_view_with_no_query_params(self):
        response = self.client.get(reverse('search:index'))
        self.assertTemplateUsed(response, 'search/index.htmldjango')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input id="searchbar" type="search" placeholder="Search" class="form-control input-lg" />', html=True)

    def test_index_view_with_search_query_param(self):
        context = {'query': 'test search'}
        response = self.client.get(reverse('search:index'), context)
        self.assertTemplateUsed(response, 'search/index.htmldjango')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['search_query'], context['query'])
        self.assertContains(response, '<input id="searchbar" type="search" value="{}" placeholder="Search" class="form-control input-lg" />'.format(context['query']), html=True)

    def xtest_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls_generic_views:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def xtest_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls_generic_views:index'))
        self.assertContains(response, 'No polls are available.', status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def xtest_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls_generic_views:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def xtest_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text='Past question 1.', days=-30)
        create_question(question_text='Past question 2.', days=-5)
        response = self.client.get(reverse('polls_generic_views:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDetailTests(TestCase):
    def xtest_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls_generic_views:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def xtest_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past question.', days=-5)
        response = self.client.get(reverse('polls_generic_views:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)

class QuestionMethodTests(TestCase):
    def xtest_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def xtest_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def xtest_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)
