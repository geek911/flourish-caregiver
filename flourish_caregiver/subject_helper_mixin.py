from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from .models import CaregiverLocator, MaternalDataset


class SubjectHelperMixin:

    maternal_dataset_options = {
        'cooking_method': '',
        'delivdt': datetime(2015, 3, 31).date(),
        'delivery_location': 'Molepolole',
        'delivmeth': '',
        'house_type': 'Formal: tin-roofed & concrete walls',
        'live_inhouse_number': 5,
        'mom_age_enrollment': '18-24 years',
        'mom_arvstart_date': datetime(2014, 6, 17).date(),
        'mom_baseline_cd4': 516,
        'mom_education': 'Secondary',
        'mom_enrolldate': datetime(2015, 4, 1).date(),
        'mom_hivstatus': 'HIV-infected',
        'mom_maritalstatus': 'Single',
        'mom_moneysource': 'Relative',
        'mom_occupation': 'Housewife or unemployed',
        'mom_personal_earnings': 'None',
        'mom_pregarv_strat': '3-drug ART',
        'parity': 1,
        'piped_water': 'Other water source',
        'protocol': 'Tshilo Dikotla',
        'site_name': 'Gaborone',
        'study_maternal_identifier': '142-4995638-1',
        'toilet': 2,
        'toilet_indoors': 'Latrine or none',
        'toilet_private': 'Indoor toilet or private latrine',
        'preg_efv': '1'}

    def create_antenatal_enrollment(self, **kwargs):
        import_holidays()

        preg_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        self.options = {
            'consent_datetime': get_utcnow(),
            'screening_identifier': preg_screening.screening_identifier,
            'breastfeed_intent': YES,
            'version': '1'}

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_caregiver.caregiverlocator',
            subject_identifier=subject_consent.subject_identifier,)

        return subject_consent.subject_identifier

    def create_TD_efv_enrollment(self, screening_identifier, **kwargs):
        import_holidays()

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            prior_screening = mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier)

            consent_options = {
                'consent_datetime': get_utcnow(),
                'screening_identifier': prior_screening.screening_identifier,
                'breastfeed_intent': YES,
                'version': '1'}

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                ** consent_options)

            mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                child_dob=maternal_dataset_obj.delivdt,)

            mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled')

            return subject_consent.subject_identifier
        return None

    def create_TD_no_hiv_enrollment(self, screening_identifier, **kwargs):
        import_holidays()

        self.maternal_dataset_options['mom_hivstatus'] = 'HIV uninfected'

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            prior_screening = mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier)

            consent_options = {
                'consent_datetime': get_utcnow(),
                'screening_identifier': prior_screening.screening_identifier,
                'breastfeed_intent': YES,
                'version': '1'}

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                ** consent_options)

            mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                child_dob=maternal_dataset_obj.delivdt,)

            mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled')

            return subject_consent.subject_identifier
        return None

    def prepare_prior_participant_enrollment(self, maternal_dataset_obj):

        try:
            caregiver_locator = CaregiverLocator.objects.get(
                screening_identifier=maternal_dataset_obj.screening_identifier)
        except CaregiverLocator.DoesNotExist:
            caregiver_locator = mommy.make_recipe(
                'flourish_caregiver.caregiverlocator',
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
                screening_identifier=maternal_dataset_obj.screening_identifier)

        worklist_cls = django_apps.get_model('flourish_follow.worklist')
        try:
            worklist_cls.objects.get(
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)
        except worklist_cls.DoesNotExist:
            mommy.make_recipe(
                'flourish_follow.worklist',
                subject_identifier=None,
                study_maternal_identifier=caregiver_locator.study_maternal_identifier,)

        call = mommy.make_recipe(
            'flourish_follow.call',
            label='worklistfollowupmodelcaller')

        log = mommy.make_recipe(
            'flourish_follow.log',
            call=call,)

        mommy.make_recipe(
            'flourish_follow.logentry',
            log=log,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,)

    def enroll_prior_participant(self, screening_identifier):

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            self.options = {
                'consent_datetime': get_utcnow(),
                'version': '1'}

            mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier,)

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                **self.options)

            mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                child_dob=maternal_dataset_obj.delivdt,)

            mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled')

    def enroll_prior_participant_assent(self, screening_identifier):

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            self.options = {
                'consent_datetime': get_utcnow(),
                'version': '1'}

            mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier,)

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                subject_identifier=self.subject_identifier,
                **self.options)

            caregiver_child_consent_obj = mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                child_dob=maternal_dataset_obj.delivdt,)

            mommy.make_recipe(
                'flourish_child.childassent',
                subject_identifier=self.subject_identifier + '-10',
                dob=maternal_dataset_obj.delivdt,
                identity=caregiver_child_consent_obj.identity,
                confirm_identity=caregiver_child_consent_obj.identity,
                remain_in_study=NO,
                version=subject_consent.version)

            mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled')
