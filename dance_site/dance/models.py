from django.db import models

class DanceGroup(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DanceStyle(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Dancer(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    group = models.ForeignKey(DanceGroup, on_delete=models.CASCADE, related_name='dancers')

    def __str__(self):
        return self.name

class Performance(models.Model):
    group = models.ForeignKey(DanceGroup, on_delete=models.CASCADE, related_name='performances')
    style = models.ForeignKey(DanceStyle, on_delete=models.CASCADE, related_name='performances')
    date = models.DateField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.group.name} - {self.style.name} on {self.date}"
