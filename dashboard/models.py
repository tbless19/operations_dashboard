from django.db import models

class Flight_count(models.Model):
    count= models.IntegerField(null=True)
    
    

    

class Reset(models.Model):
    date_swapped = models.DateField(auto_now_add= True)
    owner =models.CharField (max_length = 100, null= True)

    def __str__(self):
        return self.owner