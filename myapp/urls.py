from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views


class RegistrationView:
	pass


urlpatterns = [
	#Leave as empty string for base url
    path('', views.page, name="page"),
    path('page/', views.page, name="some_page"),
	path('categories/', views.categories, name="categories"),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),

    path('process_order/', views.processOrder, name="process_order"),
	path('form/', views.form, name="form"),
	path('contact/',views.contact, name="contact"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	path('search/', views.product_search, name='product_search'),
	path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
	path('login/', views.login_view, name='login'),
	path('register/', views.register, name='register'),

]


