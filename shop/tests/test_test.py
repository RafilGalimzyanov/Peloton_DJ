from django.test import TestCase


class MyTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('setUpTestData: вызывается один раз')

    def setUp(self):
        print('setUp: вызывается перед каждым тестом')

    def tearDown(self):
        print('tearDown: вызывается после каждого теста')

    def test_1(self):
        print('test_1')
        self.assertFalse(False)

    def test_2(self):
        print('test_2')
        #self.assertTrue(False)
        self.assertTrue(True)

    def test_3(self):
        print('test_3')
        self.assertEqual(6, 2 * 3)
