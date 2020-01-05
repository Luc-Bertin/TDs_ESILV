from django.db import models

# Create your models here.
class House(models.Model):
    CRIM        = models.FloatField()
    ZN          = models.FloatField()
    INDUS       = models.FloatField()
    CHAS        = models.FloatField()
    NOX         = models.FloatField()
    RM          = models.FloatField()
    AGE         = models.FloatField()
    DIS         = models.FloatField()
    RAD         = models.FloatField()
    TAX         = models.FloatField()
    PTRATIO     = models.FloatField()
    B           = models.FloatField()
    LSTAT       = models.FloatField()
    # The dependent variable: y
    MEDV          = models.FloatField(null=True)
    # Just to give a date to the creation of the object instance
    created       = models.DateTimeField(auto_now_add=True)

    # We don't have to...
    #class Meta:
    #    ordering = ['created']
