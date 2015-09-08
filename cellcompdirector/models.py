from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Avg
import time
import random

# Create your models here.

class PermuteTimeoutError(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Cell(models.Model):
    cellID = models.AutoField(primary_key = True)
    fileloc = models.CharField(max_length=400)

    def __str__(self):
        return self.fileloc

    def uniqueRatingforUser(self, rater):
        return Rating.objects.filter(controlCell = self,user = rater).aggregate(sum = Sum('rating'))['sum']


def checkForRedundant(ratingQset,cells):
    return ratingQset.filter(controlCell = cells[0],variableCell = cells[1]).count() > 0


class Rater(models.Model):
    userId = models.AutoField(primary_key = True)
    name = models.CharField(max_length=300)
    trustRating = models.DecimalField(max_digits = 10,decimal_places=5)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name+' '+str(self.trustRating)

    def nextCellPair(self,cCell = None): #TODO revise cell picking algorithm
        rated = self.ratings()

        if cCell is None:
            cCell = self.pickCell() 

        rcell = self.pickCell()
        cells = (cCell, rcell)
        pretime = time.time()
        while checkForRedundant(rated,cells):
            rcell = self.pickCells()
            cells = (cCell,rcell)
            diff = time.time() - pretime
            if diff > 30:
                raise PermuteTimeoutError(rated.all())
        return cells

    def ratings(self):
        return Rating.objects.filter(user = self)

    def mean(self):
        return self.ratings.aggregate(avg = Avg('rating'))['avg']

    def pickCell(self):
        set = [d['cellID'] for d in Cell.objects.all().values('cellID')]

        id2 = random.choice(set)

        cell = Cell.objects.get(cellID = id2)
        return cell



class Rating(models.Model):
    controlCell = models.ForeignKey(Cell, related_name='control')
    variableCell = models.ForeignKey(Cell, related_name='variable')
    user = models.ForeignKey(Rater)
    rating = models.SmallIntegerField()

    def __str__(self):
        return str(self.controlCell)+' '+str(self.variableCell)+' '+str(self.user)+' '+str(self.rating)
