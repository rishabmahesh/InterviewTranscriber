import unittest
from nlp_tools import NLP_Tools, InvalidQuestionError

class nlp_tools_test(unittest.TestCase):

    def setUp(self):
        self.nlp_tool = NLP_Tools('Demo-Europarl-EN.pcl', 'all-MiniLM-L6-v2')
        self.sentence_one = 'can you tell me when was the last time you went to the movies '
        self.sentence_two = 'the last time i went to the movies was three years ago '
        self.sentence_three = 'there are so many different movies playing which made it hard to pick one '
        self.sentence_four = 'i think we watched a comedy but i do not remember the name of it '
        self.sentence_five = 'can you tell me how many days are there in one year '
        self.sentence_six = 'i do not think there are enough days in a year '

    def test_sentence_segment(self):
        sentences = self.sentence_one + self.sentence_two
        segmented = self.nlp_tool.sentence_segment(sentences)
        print(segmented)
        for s in segmented:
            print(s)
        self.assertEqual('Can you tell me when was the last time you went to the movies? ', segmented[0])
        self.assertEqual('The last time I went to the movies was three years ago.', segmented[1])

    def test_find_question_index(self):
        index = self.nlp_tool.find_question_index(
            [self.sentence_one, self.sentence_two, self.sentence_three, self.sentence_four], self.sentence_three)
        self.assertEqual(2, index)
        index = self.nlp_tool.find_question_index(
            [self.sentence_one, self.sentence_two, self.sentence_three, self.sentence_four], self.sentence_one)
        self.assertEqual(0, index)
        index = self.nlp_tool.find_question_index(
            [self.sentence_one, self.sentence_two, self.sentence_three, self.sentence_four], self.sentence_four)
        self.assertEqual(3, index)

    def test_get_list_question_indices(self):
        text = [self.sentence_one, self.sentence_two, self.sentence_three, self.sentence_four,
                self.sentence_five, self.sentence_six]
        questions = [self.sentence_one, self.sentence_five]
        question_indices = self.nlp_tool.get_list_question_indices(text, questions)
        self.assertEqual(len(questions), len(question_indices))
        self.assertEqual(0, question_indices[0])
        self.assertEqual(4, question_indices[1])

    def test_get_question_answers(self):
        text = [self.sentence_one, self.sentence_two, self.sentence_three, self.sentence_four,
                self.sentence_five, self.sentence_six]
        question_indices = [0, 4]
        answers_0 = self.nlp_tool.get_question_answers(text, 0, question_indices)
        answers_4 = self.nlp_tool.get_question_answers(text, 4, question_indices)
        self.assertEqual(3, len(answers_0))
        self.assertEqual(1, len(answers_4))
        self.assertEqual(self.sentence_two, answers_0[0])
        self.assertEqual(self.sentence_three, answers_0[1])
        self.assertEqual(self.sentence_four, answers_0[2])
        self.assertEqual(self.sentence_six, answers_4[0])

    def test_error_question_not_in_list(self):
        with self.assertRaises(InvalidQuestionError):
            self.nlp_tool.get_question_answers([self.sentence_one], 5, [0,3])

    def test_get_list_answer_indices(self):
        text = [self.sentence_one, self.sentence_two, self.sentence_three, self.sentence_four,
                self.sentence_five, self.sentence_six]
        question_indices = [0, 4]
        answer_indices = self.nlp_tool.get_list_answer_indices(text, question_indices)
        self.assertEqual(2, len(answer_indices))
        self.assertEqual([self.sentence_two, self.sentence_three, self.sentence_four], answer_indices[0])
        self.assertEqual([self.sentence_six], answer_indices[1])

    def test_get_questions_and_answers(self):
        text = self.sentence_one + self.sentence_two + self.sentence_three + self.sentence_four + self.sentence_five + self.sentence_six
        questions = [self.sentence_one, self.sentence_five]
        q_and_a = self.nlp_tool.get_questions_and_answers(text, questions)
        print(q_and_a)
        self.assertIsNotNone(q_and_a[0])
        self.assertIsNotNone(q_and_a[1])
        with self.assertRaises(KeyError):
            q_and_a[2]
        self.assertEqual('Can you tell me when was the last time you went to the movies? ', q_and_a[0]['question'])
        self.assertEqual('Can you tell me how many days are there in one year? ' , q_and_a[1]['question'])
        self.assertEqual(3, len(q_and_a[0]['answer']))
        self.assertEqual(1, len(q_and_a[1]['answer']))


if __name__ == '__main__':
    unittest.main()