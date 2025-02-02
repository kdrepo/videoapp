from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = ""  # Hide Email Label
        self.fields['password'].label = ""  # Hide Password Label
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('login', 'Login', css_class='btn btn-primary'))
