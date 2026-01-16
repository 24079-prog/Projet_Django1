from django.db import models

class Asset(models.Model):
    CATEGORY_CHOICES = [
        ("currency", "Devise"),
        ("commodity", "Matière première"),
        ("crypto", "Crypto"),
    ]

    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    api_source = models.CharField(max_length=50)
    api_symbol = models.CharField(max_length=50)
    base_currency = models.CharField(max_length=10, default="USD")

    def __str__(self):
        return self.code



class Price(models.Model):
    asset = models.ForeignKey(Asset,related_name="prices",on_delete=models.CASCADE)
    date = models.DateField()
    value_source = models.DecimalField(max_digits=15,decimal_places=4,default=0)
    value_mru = models.DecimalField(max_digits=15,decimal_places=4,default=0)
    source = models.CharField(max_length=50)

    class Meta:
        unique_together = ("asset", "date")
        ordering = ["date"]

    def __str__(self):
        return f"{self.asset.code} - {self.date}"

