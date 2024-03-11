from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from edc_senaite_interface.admin import SenaiteResultAdminMixin
from edc_model_admin import audit_fieldset_tuple
from edc_fieldsets.fieldsets import Fieldsets
from edc_constants.constants import POS

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverSafiStigmaForm
from ..models import CaregiverSafiStigma
from .modeladmin_mixins import CrfModelAdminMixin
from ..helper_classes import MaternalStatusHelper


@admin.register(CaregiverSafiStigma, site=flourish_caregiver_admin)
class CaregiverSafiStigmaAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverSafiStigmaForm

    fieldsets = [
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'judged',
                'judged_period',
                'avoided',
                'avoided_period',
                'discriminated',
                'discriminated_period'
            ]}
         ),
        ('Because someone else in my family has HIV or because I have HIV, I have experienced discrimination at:', {
            'fields': [
                'at_home',
                'at_home_period',
                'at_neigborhood',
                'at_neigborhood_period',
                'at_religious',
                'at_religious_period',
                'at_clinic',
                'at_clinic_period',
                'at_workplace',
                'at_workplace_period',
                'other_place',
                'other_place_period'
            ]}),

        ('Because someone else in my family has HIV or because I have HIV, discrimination has led my family to: ', {
            'fields': [
                'finacial_support',
                'finacial_support_period',
                'social_support',
                'social_support_period',

            ]}),
        ('Because someone else in my family has HIV or because I have HIV, discrimination has made me feel:', {
            'fields': [
                'stressed',
                'stressed_period',
                'saddened',
                'saddened_period',
                'hiv_perspective'
            ]}),
    ]

    hiv_fieldsets = [
        ('The questions below also ask about stigma and discrimination, but we are now going to ask '
         'about stigma and discrimination that you experience.', {
            'fields': [
                'isolated',
                'isolated_period',
                'insulted',
                'insulted_period'

            ]},
         ),
        ('Because of my HIV status, I have experienced discrimination', {
            'fields': [
                'home_discr',
                'home_discr_period',
                'neighborhood_discr',
                'neighborhood_discr_period',
                'religious_place_discr',
                'religious_place_discr_period',
                'clinic_discr',
                'clinic_discr_period',
                'other_discr',
                'other_discr_period',

            ]},
        ),
        ('Because of my HIV status, discrimination has negatively affected me in the following ways', {
            'fields': [
                'social_effect',
                'social_effect_period',
                'emotional_effect',
                'emotional_effect_period',
                'pespective_changed',
                'pespective_changed_period',
        ]},
        ),
    ]

    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets after modifications declared in
        "conditional" dictionaries.
        """
        fieldsets = list(super().get_fieldsets(request, obj=obj))

        status = self.hiv_status(request)
        if status == POS:
            fieldsets.extend(self.hiv_fieldsets)

        fieldsets.append(audit_fieldset_tuple)
        fieldsets = Fieldsets(fieldsets=fieldsets)

        return fieldsets.fieldsets

    def hiv_status(self, request):
        try:
            appointment_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            return None
        else:

            subject_identifier = appointment_obj.subject_identifier

            status_helper = MaternalStatusHelper(subject_identifier=subject_identifier)

            return status_helper.hiv_status

    radio_fields = {
        'judged': admin.VERTICAL,
        'judged_period': admin.VERTICAL,
        'avoided': admin.VERTICAL,
        'avoided_period': admin.VERTICAL,
        'discriminated': admin.VERTICAL,
        'discriminated_period': admin.VERTICAL,
        'at_home': admin.VERTICAL,
        'at_home_period': admin.VERTICAL,
        'at_neigborhood': admin.VERTICAL,
        'at_neigborhood_period': admin.VERTICAL,
        'at_religious': admin.VERTICAL,
        'at_religious_period': admin.VERTICAL,
        'at_clinic': admin.VERTICAL,
        'at_clinic_period': admin.VERTICAL,
        'at_workplace': admin.VERTICAL,
        'at_workplace_period': admin.VERTICAL,
        'finacial_support': admin.VERTICAL,
        'finacial_support_period': admin.VERTICAL,
        'social_support': admin.VERTICAL,
        'social_support_period': admin.VERTICAL,
        'stressed': admin.VERTICAL,
        'stressed_period': admin.VERTICAL,
        'saddened': admin.VERTICAL,
        'saddened_period': admin.VERTICAL,
        'hiv_perspective': admin.VERTICAL,
        'isolated': admin.VERTICAL,
        'isolated_period': admin.VERTICAL,
        'insulted': admin.VERTICAL,
        'insulted_period': admin.VERTICAL,
        'home_discr': admin.VERTICAL,
        'home_discr_period': admin.VERTICAL,
        'neighborhood_discr': admin.VERTICAL,
        'neighborhood_discr_period': admin.VERTICAL,
        'religious_place_discr': admin.VERTICAL,
        'religious_place_discr_period': admin.VERTICAL,
        'clinic_discr': admin.VERTICAL,
        'clinic_discr_period': admin.VERTICAL,
        'social_effect': admin.VERTICAL,
        'social_effect_period': admin.VERTICAL,
        'emotional_effect': admin.VERTICAL,
        'emotional_effect_period': admin.VERTICAL,
        'pespective_changed': admin.VERTICAL,
        'pespective_changed_period': admin.VERTICAL,
        'other_discr_period': admin.VERTICAL,
        'other_place_period': admin.VERTICAL,

    }
