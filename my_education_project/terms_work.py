'''Модуль с функциями обработки логики сайта'''
# from cgi import maxlen
# from os.path import split
import random
from .models import MusicTerm
#from .views import terms_list



def get_terms_for_table_from_db():
    '''Получаем список с полями из базы'''
    return [[t.id, t.m_term, t.description, t.author] for t in MusicTerm.objects.all()]




def write_term_to_db(new_term, new_description, user_name):
    '''Заносим в базу термины'''
    if MusicTerm.objects.filter(m_term__iexact=new_term).exists():
        return False
    term = MusicTerm(m_term=new_term, description=new_description, author=user_name)
    term.save()
    return True




def get_terms_stats_from_db():
    '''Получаем статистику по словам из базы'''

    # db_terms = 0
    # user_terms = 0
    # defin_len = []
    full_text = str()
    # with open("./data/terms.csv", "r", encoding="utf-8") as f:
    #     for line in f.readlines()[1:]:
    #         term, defin, added_by = line.split(";")
    #         words = defin.split()
    #         defin_len.append(len(words))
    #         if "user" in added_by:
    #             user_terms += 1
    #         elif "db" in added_by:
    #             db_terms += 1

    db_terms = MusicTerm.objects.filter(author=None).count()

    terms_all = MusicTerm.objects.count()
    terms_added = terms_all - db_terms


    full_text_list = [t.description for t in MusicTerm.objects.all()]

    full_text = " ".join(full_text_list)
    # чистим ненужные символы. Список не полный, но достаточный.
    for junk_char in ',().;:\'\"':
        full_text = full_text.replace(junk_char, ' ')


    words = full_text.split()
    words_count = len(words)
    words_max = len((max(full_text_list, key = lambda x: len(x.split()))).split())
    words_min = len((min(full_text_list, key = lambda x: len(x.split()))).split())
    words_avg = round(words_count/len(full_text_list), 1)


    stats = {
        #"terms_all": db_terms + user_terms,
        "terms_all": terms_all,
        "terms_own": db_terms,
        "terms_added": terms_added,
        # "words_avg": sum(defin_len)/len(defin_len),
        # "words_max": max(defin_len),
        # "words_min": min(defin_len)
        "words_avg": words_avg,
        "words_max": words_max,
        "words_min": words_min
    }
    return stats




def generate_test_question():
    """Сгенерировать вопрос для тестирования"""

    # кол-во вариантов ответа
    num_of_rbutton = 3
    all_terms = [[t.id, t.m_term, t.description] for t in MusicTerm.objects.all()]

    terms = random.sample(all_terms, num_of_rbutton)
    correct_term = random.choice(terms)
    question = correct_term[2]
    id_correct_term = correct_term[0]

    return {
        'question': question,
        'terms': terms,
        'correct_term': correct_term,
        'id_correct_term': id_correct_term
    }


def check_answer(user_answer_id, correct_term_id):
    """Проверить ответ пользователя"""

    if int(user_answer_id) == int(correct_term_id):
        result = 'correct'
    else:
        result =  'incorrect'
    return result
