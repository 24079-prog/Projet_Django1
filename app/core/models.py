from django.db import models


class Asset(models.Model):
    CATEGORY_CHOICES = [
        ("currency", "Currency"),
        ("commodity", "Commodity"),
    ]

    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.code


class Price(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="prices")
    date = models.DateField()
    value_mru = models.DecimalField(max_digits=15, decimal_places=4)
    source = models.CharField(max_length=50)

    class Meta:
        unique_together = ("asset", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.asset.code} - {self.date}"
