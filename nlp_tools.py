from nnsplit import NNSplit
from sentence_transformers import SentenceTransformer, util

def sentence_segment(text):
    splitter = NNSplit.load("en")
    split = splitter.split([text])[0]
    sentences = []
    for sentence in split:
        sentences.append(str(sentence))
    return sentences

def find_question_index(text, question):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedded_sentences = model.encode(text, convert_to_tensor=True)
    embedded_question = model.encode(question, convert_to_tensor=True)
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

def get_list_question_indices(text, questions):
    list_indices = []
    for question in questions:
        list_indices.append(find_question_index(text, question))
    return list_indices

def get_question_answers(text, question_index, list_of_questions):
    answer_sentences = []
    answer_index = question_index + 1
    while answer_index not in list_of_questions and answer_index < len(text):
        answer_sentences.append(text[answer_index])
        answer_index += 1
    return answer_sentences

def get_list_answer_indices(text, list_of_questions_indices):
    list_indices = []
    for question in list_of_questions_indices:
        list_indices.append(get_question_answers(text, question, list_of_questions_indices))
    return list_indices