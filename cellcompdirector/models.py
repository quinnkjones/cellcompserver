from django.db import models

# Create your models here.
class Cell(models.Model):
    cellID = models.AutoField(primary_key = True)
    fileloc = models.CharField(max_length=400)

    def __str__(self):
        return self.fileloc


class User(models.Model):
    userId = models.AutoField(primary_key = True)
    name = models.CharField(max_length=300)
    uname = models.CharField(max_length = 100)
    trustRating = models.DecimalField(max_digits = 10,decimal_places=5)

    def __str__(self):
        return self.name+' '+str(self.trustRating)

class Rating(models.Model):
    controlCell = models.ForeignKey(Cell, related_name='control')
    variableCell = models.ForeignKey(Cell, related_name='variable')
    user = models.ForeignKey(User)
    rating = models.SmallIntegerField()

    def __str__():
        return str(self.controlCell)+' '+str(self.variableCell)+' '+str(self.user)+' '+str(self.rating)
