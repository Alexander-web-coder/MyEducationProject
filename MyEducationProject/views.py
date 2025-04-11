'''Вызов страниц сайта'''
#from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from MyEducationProject import terms_work
from MyEducationProject.terms_work import (get_terms_for_table_from_db,
                                             generate_test_question)
from MyEducationProject.terms_work import check_answer
# from .models import MusicTerm





def index(request):
    '''Вызываем начальную страницу'''
    return render(request, "index.html")


def terms_list(request):
    '''Выводим страницу с таблицей   терминов'''
    terms = get_terms_for_table_from_db()
    return render(request, "term_list.html", context={"terms": terms})

@login_required
def add_term(request):
    '''Добавляем новый термин, показываем страницу'''
    return render(request, "term_add.html")


def send_term(request):
    '''Показываем страницу с подтверждением добавления термина'''
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_description = request.POST.get("new_description", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_description) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            #terms_work.write_term(new_term, new_definition)
            terms_work.write_term_to_db(new_term, new_description, user_name)
        if context["success"]:
            context["success-title"] = ""
        # return render(request, "term_request.html", context)
    else:
        add_term(request)
    return render(request, "term_request.html", context)


def show_stats(request):
    '''Показываем страницу с статистикой'''
    stats = terms_work.get_terms_stats_from_db()
    return render(request, "stats.html", stats)



def music_test(request):
    """Выводим страницу тестирования.
    В сессии пользователя сохраняем данные"""
    test_data = generate_test_question()

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
    """Проверка ответа на тест.
    Меняем внешний вид в зависимости от ответа.
    Проверка идет по сохраненным данным в сессии"""

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
