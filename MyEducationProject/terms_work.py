from cgi import maxlen

from .models import MusicTerm
#from .views import terms_list
import random


def get_terms_for_table_from_db():
    return [[t.id, t.m_term, t.description] for t in MusicTerm.objects.all()]




def write_term_to_db(new_term, new_description, user_name):
    term = MusicTerm(m_term=new_term, description=new_description, author=user_name)
    term.save()

# def get_terms_for_table():
#     terms = []
#     with open("./data/terms.csv", "r", encoding="utf-8") as f:
#         cnt = 1
#         for line in f.readlines()[1:]:
#             term, definition, source = line.split(";")
#             terms.append([cnt, term, definition])
#             cnt += 1
#     return terms


# def write_term(new_term, new_definition):
#     new_term_line = f"{new_term};{new_definition};user"
#     with open("./data/terms.csv", "r", encoding="utf-8") as f:
#         existing_terms = [l.strip("\n") for l in f.readlines()]
#         title = existing_terms[0]
#         old_terms = existing_terms[1:]
#     terms_sorted = old_terms + [new_term_line]
#     terms_sorted.sort()
#     new_terms = [title] + terms_sorted
#     with open("./data/terms.csv", "w", encoding="utf-8") as f:
#         f.write("\n".join(new_terms))


def get_terms_stats_from_db():
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
    #user_terms = Term.objects.filter(author=(not None)).count()
    terms_all = MusicTerm.objects.count()
    terms_added = terms_all - db_terms
    # full_text = " ".join(Term.objects.all().)
    full_text_list = MusicTerm.objects.values_list("description") # получен список из кортежей со значениями поля description
    for _ in full_text_list:
        full_text += (_[0] + " ")

    words = full_text.split()
    words_count = len(words)
    words_max = len(max(words, key = len))
    words_min = len(min(words, key = len))
    words_avg = len("".join(words))/words_count


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

def get_test_from_db(): #TODO
    pass

def check_test(): #TODO
    pass


def generate_test_question():
    """Сгенерировать вопрос для тестирования"""
    # valid_terms = MusicTerm.objects.exclude(description__isnull=True).exclude(description__exact='')
    # if not valid_terms.exists():
    #     return None
    num_of_rbutton = 3 #кол-во вариантов ответа
    all_terms = [[t.id, t.m_term, t.description] for t in MusicTerm.objects.all()]
    # random.shuffle(all_terms)
    terms = random.choices(all_terms, k=num_of_rbutton)
    correct_term = random.choice(terms)
    question = correct_term[2]
    id_correct_term = correct_term[0]

    # wrong_terms = MusicTerm.objects.exclude(id=correct_term.id).order_by('?')[:2]
    # terms = list(wrong_terms) + [correct_term]
    # random.shuffle(terms)

    return {
        'question': question,
        'terms': terms,
        'correct_term': correct_term,
        'id_correct_term': id_correct_term
    }


def check_answer(user_answer_id, correct_term_id):
    """Проверить ответ пользователя"""

    if int(user_answer_id) == int(correct_term_id):
        return 'correct'
    else:
        return 'incorrect'
    # try:
    #
    #     is_correct = int(user_answer_id) == int(correct_term_id)
    #     # correct_term = MusicTerm.objects.get(id=correct_term_id)
    #     # selected_term = MusicTerm.objects.get(id=user_answer_id) if user_answer_id else None
    #
    #     return {
    #         'is_correct': is_correct,
    #         'correct_term': correct_term,
    #         'selected_term': selected_term
    #     }
    # except (ValueError, MusicTerm.DoesNotExist):
    #     return None
