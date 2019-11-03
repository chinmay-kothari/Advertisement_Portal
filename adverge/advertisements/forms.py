from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
from adverge.advertisements.models import Advertisement, Category, Subcategory


# class UserChangeForm(forms.UserChangeForm):
#     class Meta(forms.UserChangeForm.Meta):
#         model = User


class AdvertisementCreationForm(forms.ModelForm):

    # error_message = forms.UserCreationForm.error_messages.update(
    #     {"duplicate_username": _("This username has already been taken.")}
    # )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='advertisements:categoryAutoComplete'))
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='advertisements:subcategoryAutoComplete',
            forward=('category',)))
    agreement = forms.BooleanField(
        required=True, label="I have read and agree to the Terms and Conditions and Privacy Policy")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('description', css_class='col-md-6'),
                Column('product_page_link', css_class='col-md-6'),


                css_class='row'
            ),
            Row(
                Column('is_global', css_class='col-md-3 form-check-box'),
                Column('locations', css_class='col-md-9'),



                css_class='row'
            ),

            Row(
                Column('category', css_class='col-md-6'),
                Column('subcategory', css_class='col-md-6'),



                css_class='row'
            ),
            Row(
                Column('tags', css_class='col-md-12'),



                css_class='row'
            ),
            Row(
                Column('video', css_class='col-md-6'),
                Column('thumbnail', css_class='col-md-6'),



                css_class='row'
            ),
            Row(
                Column('validity', css_class='col-md-6'),
                Column('cost', css_class='col-md-6'),


                css_class='row'
            ),
            'agreement',
            Submit('submit', 'Submit', css_class='make_payment_button')

        )

    class Meta:
        model = Advertisement
        exclude = ('status', 'user')
        widgets = {
            'tags': autocomplete.TaggitSelect2(
                'advertisements:tagAutoComplete'
            ),
            'locations': autocomplete.ModelSelect2Multiple(
                url='advertisements:locationAutoComplete'
            )

        }
    # def clean_username(self):
    #     username = self.cleaned_data["username"]

    #     try:
    #         User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return username

    #     raise ValidationError(self.error_messages["duplicate_username"])


class AdvertisementUpdateForm(forms.ModelForm):

    # error_message = forms.UserCreationForm.error_messages.update(
    #     {"duplicate_username": _("This username has already been taken.")}
    # )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='advertisements:categoryAutoComplete'))
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='advertisements:subcategoryAutoComplete',
            forward=('category',)))

    class Meta:
        model = Advertisement
        exclude = ('status', 'user')
        widgets = {
            'tags': autocomplete.TaggitSelect2(
                'advertisements:tagAutoComplete'
            ),
            'locations': autocomplete.ModelSelect2Multiple(
                url='advertisements:locationAutoComplete'
            )

        }


class AdvertisementFilterForm(forms.ModelForm):

    # error_message = forms.UserCreationForm.error_messages.update(
    #     {"duplicate_username": _("This username has already been taken.")}
    # )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='advertisements:categoryAutoComplete'))
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='advertisements:subcategoryAutoComplete',
            forward=('category')))

    def __init__(self, *args, **kwargs):
        super(AdvertisementFilterForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = Advertisement
        fields = ('category', 'subcategory', 'tags', 'locations')
        widgets = {
            'tags': autocomplete.TaggitSelect2(
                'advertisements:tagAutoComplete'
            ),
            'locations': autocomplete.ModelSelect2Multiple(
                url='advertisements:locationAutoComplete'
            )

        }
