from django.apps import apps as django_apps
from edc_constants.date_constants import timezone
from edc_base.utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .cohort import Cohort
from ..models import (
    AntenatalEnrollment, CaregiverPreviouslyEnrolled,
    CaregiverChildConsent, OnScheduleCohortBFU, OnScheduleCohortAFU,
    OnScheduleCohortAFUQuarterly, OnScheduleCohortAQuarterly,
    OnScheduleCohortBFUQuarterly, OnScheduleCohortBQuarterly,
    OnScheduleCohortCFUQuarterly, OnScheduleCohortCQuarterly,
    OnScheduleCohortASecQuart, OnScheduleCohortBSecQuart,
    CaregiverOffSchedule)


class SequentialCohortEnrollmentError(Exception):
    pass


class SequentialCohortEnrollment:

    """Class that checks and enrols participants to the next
    the next cohort when they age up.
    """

    def __init__(self, child_subject_identifier=None):
        
        self.child_subject_identifier = child_subject_identifier
    
    @property
    def caregiver_subject_identifier(self):
        """Return child caregiver subject identifier.
        """
        registration_mdl_cls = django_apps.get_model('edc_registration', 'registeredsubject')
        try:
            registered_subject = registration_mdl_cls.objects.get(
                subject_identifier=self.child_subject_identifier)
        except registration_mdl_cls.DoesNotExist:
            return None
        else:
            registered_subject.relative_identifier
        return None


    def check_enrollment(self):
        """Return True if the child is enrolled.
        """
        enrolled = False
        try:
            AntenatalEnrollment.objects.get(
                subject_identifier=self.caregiver_subject_identifier)
        except AntenatalEnrollment.DoesNotExist:
            enrolled = False
        else:
            enrolled = True

        try:
            CaregiverPreviouslyEnrolled.objects.get(
                subject_idetifier=self.caregiver_subject_identifier)
        except CaregiverPreviouslyEnrolled.DoesNotExist:
            enrolled = False
        else:
            enrolled = True
        return enrolled
    
    @property
    def enrollment_cohort(self):
        """Returns the cohort the child was enrolled on the first time.
        """
        cohort = None
        try:
            cohort =  Cohort.objects.get(
                subject_identifier=self.child_subject_identifier)
        except Cohort.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f"The subject: {self.child_subject_identifier} does not "
                "have an enrollment cohort")
        else:
            cohort = cohort.name
        return cohort

    @property
    def child_current_age(self):
        try:
            caregiver_child_consent =  CaregiverChildConsent.objects.get(
                study_child_identifier=self.child_subject_identifier)
        except CaregiverChildConsent.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f"The subject: {self.child_subject_identifier} does not "
                "have a caregiver child consent")
        else:
            dob = caregiver_child_consent.child_dob
            age = Cohort(
                child_dob=dob,
                enrollment_date=timezone.now().date())
            return age
        return None

    @property
    def aged_up(self):
        """Return true if the child has aged up on the cohort
        they are currently enrolled on
        """
        if self.current_cohort == 'cohort_a':
            if self.child_current_age >= 5:
                return True
        elif self.current_cohort == 'cohort_b':
            if self.child_current_age > 10:
                True
        return False
    
    @property
    def current_cohort(self):
        """Returns the cohort the child was enrolled on the first time.
        """
        cohort = Cohort.objects.objects(
            suject_identifier=self.child_subject_identifier).order_by(
                'assign_datetime'
            )
        if cohort:
            return cohort.name
        return None

    @property
    def enroll_on_age_up_cohort(self):
        """Enroll a participant on new aged up cohort.
        """
        if self.current_cohort == 'cohort_a' and self.aged_up:
            # put them on a new aged up cohort
            # Put them offschedule
            helper_cls = onschedule_helper_cls(
                subject_identifier=self.caregiver_subject_identifier,)


            if instance.visit_code in ['2000M', '2000D', '3000M']:
                base_appt_datetime = instance.report_datetime.replace(microsecond=0)
                helper_cls = onschedule_helper_cls(instance.subject_identifier, )
                helper_cls.add_on_schedule()
                helper_cls.put_quarterly_onschedule(
                    instance, base_appt_datetime=base_appt_datetime)
                
            subject_identifier = self.subject_identifier or instance.subject_consent.subject_identifier
        if instance:
            schedule, onschedule_model_cls, schedule_name = self.get_onschedule_model(
                cohort=cohort,
                caregiver_visit_count=caregiver_visit_count,
                instance=instance)

            assent_onschedule_datetime = self.get_assent_onschedule_datetime
            self.add_on_schedule(
                schedule=schedule, subject_identifier=subject_identifier, instance=instance,
                schedule_name=schedule_name, base_appt_datetime=base_appt_datetime,
                child_subject_identifier=child_subject_identifier, onschedule_model_cls=onschedule_model_cls, 
                assent_onschedule_datetime=assent_onschedule_datetime,
                
            )
            # put them on the new cohort schedule
            pass
        elif self.current_cohort == 'cohort_b' and self.aged_up:
            pass
        elif self.current_cohort == 'cohort_sec_a' and self.aged_up:
            pass
        elif self.current_cohort == 'cohort_sec_b' and self.aged_up:
            pass

    @property
    def take_off_schedule(self):
        """Take participant off schedule from previous age cohort.
        """
        a_onschedule_models = [
            OnScheduleCohortAFUQuarterly,
            OnScheduleCohortAQuarterly,
        ]
        b_onschedule_models = [
            OnScheduleCohortBFUQuarterly,
            OnScheduleCohortBQuarterly,
        ]
        if self.enrollment_cohort == 'cohort_a' and self.aged_up:
            for onschedule_model in a_onschedule_models:
                if onschedule_model == OnScheduleCohortAFUQuarterly:
                    try:
                        OnScheduleCohortAFU.objects.get(
                         subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier
                        )
                    except OnScheduleCohortAFU.DoesNotExist:
                        pass
                    else:
                        try:
                            onschedule_obj = onschedule_model.objects.get(
                                subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
                        except onschedule_model.DoesNotExist:
                            pass
                        else:
                            #put offschedule
                            _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                                onschedule_model=onschedule_model._meta.label_lower,
                                name=onschedule_obj.schedule_name)
                            if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                  report_datetime=get_utcnow()):
                                CaregiverOffSchedule.objects.create(
                                    schedule_name=onschedule_obj.schedule_name,
                                    subject_identifier=self.caregiver_subject_identifier
                                )
                else:
                    try:
                        onschedule_obj = onschedule_model.objects.get(
                            subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
                    except onschedule_model.DoesNotExist:
                        pass
                    else:
                        #put offschedule
                        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                            onschedule_model=onschedule_model._meta.label_lower,
                            name=onschedule_obj.schedule_name)
                        if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                report_datetime=get_utcnow()):
                            CaregiverOffSchedule.objects.create(
                                schedule_name=onschedule_obj.schedule_name,
                                subject_identifier=self.caregiver_subject_identifier
                            )
        elif self.enrollment_cohort == 'cohort_b' and self.aged_up:
            for onschedule_model in b_onschedule_models:
                if onschedule_model == OnScheduleCohortBFUQuarterly:
                    try:
                        OnScheduleCohortBFU.objects.get(
                         subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier   
                        )
                    except OnScheduleCohortBFU.DoesNotExist:
                        pass
                    else:
                        try:
                            onschedule_obj = onschedule_model.objects.get(
                                subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
                        except onschedule_model.DoesNotExist:
                            pass
                        else:
                            #put offschedule
                            _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                                onschedule_model=onschedule_model._meta.label_lower,
                                name=onschedule_obj.schedule_name)
                            if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                  report_datetime=get_utcnow()):
                                CaregiverOffSchedule.objects.create(
                                    schedule_name=onschedule_obj.schedule_name,
                                    subject_identifier=self.caregiver_subject_identifier
                                )
                else:
                    try:
                        onschedule_obj = onschedule_model.objects.get(
                            subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
                    except onschedule_model.DoesNotExist:
                        pass
                    else:
                        #put offschedule
                        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                            onschedule_model=onschedule_model._meta.label_lower,
                            name=onschedule_obj.schedule_name)
                        if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                report_datetime=get_utcnow()):
                            CaregiverOffSchedule.objects.create(
                                schedule_name=onschedule_obj.schedule_name,
                                subject_identifier=self.caregiver_subject_identifier
                            )
        elif self.enrollment_cohort == 'cohort_sec_a' and self.aged_up:
            try:
                onschedule_obj = OnScheduleCohortASecQuart.objects.get(
                    subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
            except OnScheduleCohortASecQuart.DoesNotExist:
                pass
            else:
                #put offschedule
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=onschedule_model._meta.label_lower,
                    name=onschedule_obj.schedule_name)
                if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                        report_datetime=get_utcnow()):
                    CaregiverOffSchedule.objects.create(
                        schedule_name=onschedule_obj.schedule_name,
                        subject_identifier=self.caregiver_subject_identifier
                    )
        elif self.enrollment_cohort == 'cohort_sec_b' and self.aged_up:
            try:
                onschedule_obj = OnScheduleCohortBSecQuart.objects.get(
                    subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
            except OnScheduleCohortBSecQuart.DoesNotExist:
                pass
            else:
                #put offschedule
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=onschedule_model._meta.label_lower,
                    name=onschedule_obj.schedule_name)
                if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                        report_datetime=get_utcnow()):
                    CaregiverOffSchedule.objects.create(
                        schedule_name=onschedule_obj.schedule_name,
                        subject_identifier=self.caregiver_subject_identifier
                    )