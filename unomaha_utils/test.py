import unittest

from web import app

class TestUnomahaUtils(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_college_view(self):
        result = self.app.get('/classes/view?term=1121&college=ACCT')
        self.assertEqual(result.status_code, 200)

        self.assertIn(b"ACCT", result.data)
        self.assertIn(b"Spring 2012", result.data)

    def test_class_history_view(self):
        result = self.app.get('/classes/history?college=ACCT&course=2010')
        self.assertEqual(result.status_code, 200)

    def test_room_view(self):
        result = self.app.get('/rooms/view?term=1121&building=Peter+Kiewit+Institute&room_number=260')
        self.assertEqual(result.status_code, 200)

        self.assertIn(b"Peter Kiewit Institute 260", result.data)
        self.assertIn(b"Spring 2012", result.data)

    def test_teacher_view(self):
        result = self.app.get('/teachers/view?lastname=poss')
        self.assertEqual(result.status_code, 200)

        self.assertIn(b"PRINCIPLES OF ACCOUNTING I", result.data)

    def test_teacher_wordcloud(self):
        result = self.app.get('/teachers/cloud.png?name=nelson')
        self.assertEqual(result.status_code, 200)

        self.assertEqual(result.headers.get('Content-Type'), 'image/png')


if __name__ == '__main__':
  unittest.main()
