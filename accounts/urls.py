from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    #path('dashboard/<str:username>/', views.dashboard_redirect, name='dashboard-redirect'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('logout/', views.logout, name='logout'),
    # password change urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # else use this instead
    #path('', include('django.contrib.auth.urls')),
    #path('register/', views.register, name='register'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('register/activate/<str:sign>', views.user_activate, name='register_activate'),
    path('register/done/', views.RegisterDoneView.as_view(), name='register_done'),
    #path('profile/', views.profile_edit, name='profile'),
    path('profile/', views.ChangeUserInfoView.as_view(), name='profile'),
    path('add/block/', views.AddBlock.as_view(), name='add_block'),
    path('delete/block/<int:pk>/', views.del_block, name='del_block'),
    path('change/block/<int:pk>/', views.UpdateBlock.as_view(), name='change_block'),
    # faq
    #path('block/<int:pk>/add/faq/', views.add_faq, name='add_faq'),
    path('block/<int:pk>/add/faq/', views.AddFaq.as_view(), name='add_faq'),
    path('delete/faq/<int:pk>/', views.del_faq, name='del_faq'),
    path('change/faq/<int:pk>/', views.UpdateFaq.as_view(), name='change_faq'),
    # table
    path('block/<int:pk>/add/table/', views.add_table, name='add_table'),
    #path('block/<int:pk>/add/table/', views.AddTable.as_view(), name='add_table'),
    #path('block/<int:pk>/add/table/', multiform.CatItemView.as_view(), name='add_table'),
    #path('block/<int:pk>/add/category/', views.AddCat.as_view(), name='add_cat'),
    #path('block/<int:pk>/add/table/', views.AddTableItem.as_view(), name='add_table'),
    path('category-autocomplete/', views.CategoryAutocomplete.as_view(), name='category-autocomplete'),
    #path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('delete/item/<int:pk>/', views.del_item, name='del_item'),
    path('change/item/<int:pk>/', views.change_item, name='change_item'),
    path('delete/category/<int:pk>/', views.del_cat, name='del_cat'),
    path('change/category/<int:pk>/', views.UpdateTableCat.as_view(), name='change_cat'),
    # images
    path('block/<int:pk>/add/image/', views.AddImageView.as_view(), name='add_image'),
    path('delete/image/<int:pk>/', views.del_image, name='del_image'),
    # video
    path('block/<int:pk>/add/video/', views.AddVideoView.as_view(), name='add_video'),
    path('delete/video/<int:pk>/', views.del_video, name='del_video'),
    # links
    path('block/<int:pk>/add/link/', views.AddLinkView.as_view(), name='add_link'),
    path('delete/link/<int:pk>/', views.del_link, name='del_link'),
    path('change/link/<int:pk>/', views.UpdateLinkView.as_view(), name='change_link'),
    # profile card
    #path('card/profile/edit/', views.CardProfileUpdate.as_view(), name='card_profile'),
    # bg design
    path('create/background/<int:pk>/', views.BackgroundCreateView.as_view(), name='bg_create'),
    path('edit/background/<int:pk>/', views.BackgroundUpdateView.as_view(), name='bg_edit'),
    #path('background/<int:pk>/', views.BGView.as_view(), name='bg_test'),
]