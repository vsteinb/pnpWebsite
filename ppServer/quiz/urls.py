from django.urls import path

from . import views, views_sp

app_name = 'quiz'

urlpatterns = [
	path('sp', views_sp.sp_index, name='sp_index'),
	path('sp/questions', views_sp.sp_questions, name="sp_questions"),
	path('sp/modules', views_sp.sp_modules, name="sp_modules"),
	path('sp/correct/<int:id>', views_sp.sp_correct, name="sp_correct"),


	path('', views.index, name='index'),
	path('question', views.question, name='question'),
	path('done', views.session_done, name='session_done'),
	path('review/<int:id>', views.review, name="review"),
	path('review_done', views.session_done, name='review_done'),
	path('scoreBoard', views.score_board, name='scoreBoard'),
]
