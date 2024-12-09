from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/",views.register,name="register"),
     # change password urls
    path('password-change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    # reset password urls
    path('password-reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    # edit profile
    path('edit/', views.edit, name='edit'),
    path('show_profile/<int:id>/', views.show_profile, name='show_profile'),
    path("people/",views.show_people,name="people"),
    # company
    path("register-company/",views.register_company,name="register_company"),
    path("show-company/<int:id>/",views.show_company,name="show_company"),
    path('edit-company/', views.editcompany, name='edit_company'),
    path('announce-job/', views.announce_job, name='announce_job'),
    path("jobs",views.job_list,name="jobs"),
    path("job-details/<int:id>/",views.job_details,name="job_details"),
    path("unauthorized-access",views.unauthorized_access,name="unauthorized_access"),
    path("apply-job/<int:id>/", views.apply_job, name='apply_job'),
    path("delete-job/<int:id>/", views.delete_job, name='delete_job'),
    path("delete-suggestion/<int:id>/", views.delete_suggestion, name='delete_suggestion'),
    path("users", views.all_user, name='all_user'),
    path("search-user", views.search_user, name='search_user'),
    path("search-jobs", views.search_jobs, name='search_jobs'),
    path("suggestions/<int:id>/", views.suggestions, name='suggestions'),
    path("view-suggestion/<int:id>/", views.view_suggestion, name='view_suggestion'),
    path("suggestion-details/<int:id>/", views.suggestion_details, name='suggestion_details'),
    path('rate-user/<int:id>/', views.rate_user, name='rate_user'),
    path('rate-company/<int:id>/', views.rate_company, name='rate_company'),
    path("manage-user-rates", views.manage_user_rates, name='manage_user_rates'),
    path("manage-company-rates", views.manage_company_rates, name='manage_company_rates'),
    path("delete-user-rate/<int:id>/", views.delete_user_rates, name='delete_user_rate'),
    path("delete-company-rate/<int:id>/", views.delete_company_rates, name='delete_company_rate'),
    ]   