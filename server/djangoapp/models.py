from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car Make"
        verbose_name_plural = "Car Makes"


class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('HATCHBACK', 'Hatchback'),
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('MINIVAN', 'Minivan'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=20, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)],
        default=2023
    )
    dealer_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"

    class Meta:
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"
