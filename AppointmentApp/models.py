from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        validators=[FileExtensionValidator(['pdf'])],
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE
    )

    appointment_date = models.DateTimeField()

    def clean(self):
        if self.appointment_date:
            if self.pk is None or not Appointment.objects.filter(pk=self.pk, appointment_date=self.appointment_date).exists():
                if self.appointment_date <= timezone.now():
                    raise ValidationError({
                        'appointment_date': "La date du rendez-vous doit être dans le futur."
                    })

    class Meta:
        ordering = ['appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment'
            )
        ]