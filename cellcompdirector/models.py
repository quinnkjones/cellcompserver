from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
class Cell(models.Model):
    cellID = models.AutoField(primary_key = True)
    fileloc = models.CharField(max_length=400)

    def __str__(self):
        return self.fileloc

def checkForRedundant(ratingQset,cells):
    return ratingQset.filter(controlCell = cells[0],variableCell = cells[1]).count() > 0


class Rater(models.Model):
    userId = models.AutoField(primary_key = True)
    name = models.CharField(max_length=300)
    trustRating = models.DecimalField(max_digits = 10,decimal_places=5)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name+' '+str(self.trustRating)

    def nextCellPair(self): #TODO revise cell picking algorithm
        rated = self.ratings()
        cells = self.pickCells()
        while checkForRedundant(rated,cells):
            cells = self.pickCells()
        return cells

    def ratings(self):
        return Rating.objects.filter(user = self)

    def mean(self):
        rated = self.ratings().all()
        sum = 0
        count = 0.0
        for r in rated:
            count += 1.0
            sum += r.rating

        return sum/count if count != 0 else 0

    def pickCells(self):
        max = Cell.objects.latest('cellID').cellID
        min = Cell.objects.first().cellID
        id1 = random.randint(min,max)
        id2 = random.randint(min,max)
        leftcell = Cell.objects.get(cellID = id1)
        rightcell = Cell.objects.get(cellID = id2)
        return (leftcell,rightcell)



class Rating(models.Model):
    controlCell = models.ForeignKey(Cell, related_name='control')
    variableCell = models.ForeignKey(Cell, related_name='variable')
    user = models.ForeignKey(Rater)
    rating = models.SmallIntegerField()

    def __str__(self):
        return str(self.controlCell)+' '+str(self.variableCell)+' '+str(self.user)+' '+str(self.rating)
