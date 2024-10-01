from django.db import models

class NSSVolunteer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Donor(models.Model):
    volunteer = models.ForeignKey(NSSVolunteer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)  # Change to CharField for formatting
    blood_group = models.CharField(max_length=5)

    def __str__(self):
        return self.name
