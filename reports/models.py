from django.db import models

from django.db import models

class Report(models.Model):
    year = models.IntegerField()
    month = models.CharField(max_length=20)

    internal_castration = models.IntegerField(null=True, blank=True)
    external_castration = models.IntegerField(null=True, blank=True)

    internal_attendance = models.IntegerField(null=True, blank=True)
    external_attendance = models.IntegerField(null=True, blank=True)
    
    deaths = models.IntegerField(null=True, blank=True)
    euthanasia = models.IntegerField(null=True, blank=True)

    samuvet_requests = models.IntegerField(null=True, blank=True)

    animal_donations = models.IntegerField(null=True, blank=True)

    releases = models.IntegerField(null=True, blank=True)

    rescue_animals = models.IntegerField(null=True, blank=True)

    donations = models.IntegerField(null=True, blank=True)

    sheltered_animals = models.IntegerField(null=True, blank=True)

    def _str_(self):
        return f"(self.year) - (self.month)"