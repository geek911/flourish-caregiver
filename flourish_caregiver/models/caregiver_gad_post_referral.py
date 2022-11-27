from django.db import models

from ..choices import EMO_SUPPORT_PROVIDER
from .model_mixins import CrfModelMixin, ReferralFUFormMixin


class CaregiverGadPostReferral(ReferralFUFormMixin, CrfModelMixin):

    emo_support_provider = models.CharField(
        verbose_name=('1.    You mentioned that you are currently receiving emotional '
                      'support services. Do you mind sharing with us where you are receiving '
                      'these services?'),
        max_length=40,
        choices=EMO_SUPPORT_PROVIDER,
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver GAD-7 Post Referral Form'
        verbose_name_plural = 'Caregiver GAD-7 Post Referral Forms'
