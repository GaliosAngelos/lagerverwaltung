from django.db import models
from django.contrib.auth.models import User


class Lager(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Der Besitzer des Lagers
    users = models.ManyToManyField(User, related_name='lagers')  # Benutzer, die diesem Lager zugewiesen sind

    def __str__(self):
        return self.name


class LagerAccess(models.Model):
    lager = models.ForeignKey(Lager, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} -> {self.lager.name}"



class Artikel(models.Model):
    name = models.CharField(max_length=100)
    menge = models.IntegerField()
    lager = models.ForeignKey(Lager, on_delete=models.CASCADE, related_name='artikel')
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)  # Optionales Bildfeld

    def __str__(self):
        return f"{self.name} (Menge: {self.menge})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('in', 'Eingang'),
        ('out', 'Ausgang'),
    ]
    article = models.ForeignKey(Artikel, on_delete=models.CASCADE)
    lager = models.ForeignKey(Lager, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)


