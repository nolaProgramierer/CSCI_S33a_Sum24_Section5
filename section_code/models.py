from django.db import models

# -----------------------------------------------------------------
# Recursive m2m
# ------------------------------------------------------------------

class Employee(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=25)
    boss = models.BooleanField(default=False)
    supervisors = models.ManyToManyField("Employee", related_name="subordinates")

    class Meta:
        ordering = ["lname"]

    def __str__(self):
        return f"{self.lname}, {self.fname}, is a boss: {self.boss}"
    
    




