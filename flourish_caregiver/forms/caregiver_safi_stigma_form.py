from django import forms
from edc_base.sites import SiteModelFormMixin
from .form_mixins import SubjectModelFormMixin
from flourish_form_validations.form_validators import CaregiverSafiStigmaFormValidator
from ..models import CaregiverSafiStigma


class CaregiverSafiStigmaForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CaregiverSafiStigmaFormValidator

    class Meta:
        model = CaregiverSafiStigma
        fields = '__all__'
