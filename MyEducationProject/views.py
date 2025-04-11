from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.core.cache import cache
from MyEducationProject import terms_work
from MyEducationProject.terms_work import get_terms_for_table_from_db, get_test_from_db, generate_test_question
from MyEducationProject.terms_work import check_answer
from .models import MusicTerm
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, "index.html")


def terms_list(request):
    #terms = terms_work.get_terms_for_table()
    terms = get_terms_for_table_from_db()
    return render(request, "term_list.html", context={"terms": terms})

@login_required
def add_term(request):
    return render(request, "term_add.html")

# @login_required
# def send_term(request):
#     if request.method == "POST":
#         cache.clear()
#         user_name = request.POST.get("name")
#         new_term = request.POST.get("new_term", "")
#         new_description = request.POST.get("new_description", "").replace(";", ",")
#         context = {"user": user_name}
#         if len(new_description) == 0:
#             context["success"] = False
#             context["comment"] = "Описание должно быть не пустым"
#         elif len(new_term) == 0:
#             context["success"] = False
#             context["comment"] = "Термин должен быть не пустым"
#         else:
#             context["success"] = True
#             context["comment"] = "Ваш термин принят"
#             #terms_work.write_term(new_term, new_definition)
#             terms_work.write_term_to_db(new_term, new_description, user_name)
#         if context["success"]:
#             context["success-title"] = ""
#         return render(request, "term_request.html", context)
#     else:
#         add_term(request)


def show_stats(request):
    stats = terms_work.get_terms_stats_from_db()
    return render(request, "stats.html", stats)

# def testing(request):
#     question = get_test_from_db()
#     return render(request, "testing.html", question)

def music_test(request):
    """Страница тестирования"""

    test_data = generate_test_question()

    # if not test_data:
    #     return render(request, 'testing.html', {'error': 'Нет доступных терминов для тестирования'})

    # сохраняем данные, которые отправляем на страницу
    request.session['question'] = test_data['question']
    request.session['terms'] = test_data['terms']
    request.session['correct_term'] = test_data['correct_term']
    request.session['id_correct_term'] = test_data['id_correct_term']

    return render(request, 'testing.html', {
        'question': request.session['question'],
        'terms': request.session['terms'],
        'result': 'unknown'
        # 'correct_term': request.session['correct_term']
    })


def check_test(request):
    """Проверка ответа на тест"""

    if request.method == 'POST':
        result = check_answer(
            user_answer_id=request.POST.get('answer'),
            correct_term_id=request.session['id_correct_term']
        )

    return render(request, 'testing.html', {
        'question': request.session['question'],
        'terms': request.session['terms'],
        'correct_term': request.session['correct_term'],
        'result': result
    })

    #     if not result:
    #         return redirect('music_test')
    #
    #     return render(request, 'testing.html', {
    #         'question': result['correct_term'].description,
    #         'terms': MusicTerm.objects.filter(id__in=[
    #             request.POST.get('answer'),
    #             request.POST.get('correct_term')
    #         ]),
    #         'correct_term': result['correct_term'],
    #         'result': 'correct' if result['is_correct'] else 'incorrect'
    #     })
    #
    # return redirect('music_test')