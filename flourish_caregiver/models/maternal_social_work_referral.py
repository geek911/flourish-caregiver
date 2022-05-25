from django.db import models
from .model_mixins import CrfModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from ..choices import HIV_STATUS
from edc_base.model_fields import OtherCharField
from .list_models import MaternalSocialWorkReferralList

class MaternalSocialWorkReferral(CrfModelMixin):
    
    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, datetime_not_before_study_start],)
    
    is_preg = models.CharField(
        verbose_name='Is the caregiver pregnant? ',
        max_length=3,
        choices=YES_NO)
    
    current_hiv_status = models.CharField(
        verbose_name='What is your current HIV status?',
        choices=HIV_STATUS,
        max_length=14,
        null=True,
        blank=True,)
    
    referral_reason = models.ManyToManyField(
        MaternalSocialWorkReferralList,
        verbose_name='Please indicate reasons for the need for a social work '
        'referral for the Mother/Caregiver (select all that apply)',
        blank=True,
    )

    reason_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )
    
    comment = models.TextField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal Social Work ReferralList'
        verbose_name_plural = 'Maternal Social Work ReferralList'


