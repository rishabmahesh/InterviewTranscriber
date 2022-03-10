from nnsplit import NNSplit
from punctuator import Punctuator
import spacy

from sentence_transformers import SentenceTransformer, util


class InvalidQuestionError(Exception):
    pass


class NLP_Tools:

    def __init__(self, punct_language, sent_model):
        """
        Parameters:
          language : the language for the sentence segmenter
          model : model for the sentence transformer
        """

        self.punctuator = Punctuator(punct_language)
        self.splitter = NNSplit.load('en')
        self.model = SentenceTransformer(sent_model)
        self.nlp = spacy.load('en_core_web_lg')

    def sentence_segment(self, text):
        split = self.punctuator.punctuate(text)
        split = self.splitter.split([split])[0]
        print(split)
        sentences = []
        for sentence in split:
            sentences.append(str(sentence))
        return sentences

    def find_question_index(self, text, question):
        embedded_sentences = self.model.encode(text, convert_to_tensor=True)
        embedded_question = self.model.encode(question, convert_to_tensor=True)
        #Compute cosine-similarits
        cosine_scores = util.cos_sim(embedded_sentences, embedded_question)
        #find index of the matching sentence:
        index = -1
        highest_similarity = -1
        for i in range(len(cosine_scores)):
            if cosine_scores[i] > highest_similarity:
                index = i
                highest_similarity = cosine_scores[i]

        return(index)

    def get_list_question_indices(self, text, questions):
        list_indices = []
        for question in questions:
            list_indices.append(self.find_question_index(text, question))
        return list_indices

    def get_question_answers(self, text, question_index, list_of_questions):
        if question_index not in list_of_questions:
            raise InvalidQuestionError('An invalid question index was specified when trying to find corresponding answers.')
        answer_sentences = []
        answer_index = question_index + 1
        while answer_index not in list_of_questions and answer_index < len(text):
            answer_sentences.append(text[answer_index])
            answer_index += 1
        return answer_sentences

    def get_list_answer_indices(self, text, list_of_questions_indices):
        list_indices = []
        for question in list_of_questions_indices:
            list_indices.append(self.get_question_answers(text, question, list_of_questions_indices))
        return list_indices

    def get_questions_and_answers(self, text, questions):
        sentences = self.sentence_segment(text)
        question_indices = self.get_list_question_indices(sentences, questions)
        answer_lists = self.get_list_answer_indices(sentences, question_indices)
        q_and_a = []
        for i in range(len(question_indices)):
            q_and_a_pair = {}
            q_and_a_pair['question'] = sentences[question_indices[i]]
            q_and_a_pair['answer'] = answer_lists[i]
            q_and_a.append(q_and_a_pair)
        return q_and_a

    def get_ner(self, text):
        doc = self.nlp(text)
        ners = []
        for ent in doc.ents:
            ner = {}
            ner['label'] = ent.label_
            ner['start_index'] = ent.start_char
            ner['end_index'] = ent.end_char
            ners.append(ner)
            #print(ent.text, ent.start_char-ent.sent.start_char, ent.end_char-ent.sent.start_char, ent.label_)
        return ners