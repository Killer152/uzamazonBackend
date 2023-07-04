from django.urls import path

from account.utils import NewObtainJSONWebToken
from account.views import RegistrationView, RegistrationTokenView, PasswordSetView, ChangePasswordView, \
    PasswordForgetCodeView, ResetTokenView, ProfileView, ProfileAvatarView, UserDeleteView, UserStatus

urlpatterns = [
    path('login', NewObtainJSONWebToken.as_view(), name='login'),
    path('status', UserStatus.as_view(), name='status'),
    path('register', RegistrationView.as_view(), name='registration'),
    path('register/token', RegistrationTokenView.as_view(), name='registration-token'),
    path('password/set', PasswordSetView.as_view(), name='password-set'),
    path('password/change', ChangePasswordView.as_view(), name='password-change'),
    path('password/reset', PasswordForgetCodeView.as_view(), name='password-reset'),
    path('password/reset/code', ResetTokenView.as_view(), name='token-reset'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/avatar', ProfileAvatarView.as_view(), name='profile-avatar'),
    path('delete', UserDeleteView.as_view(), name='user-delete')
]
