from django.db import models


class Species(models.Model):
    """Model to store IUCN species data"""
    
    # Status choices based on IUCN Red List categories
    STATUS_CHOICES = [
        ('CR', 'Critically Endangered'),
        ('EN', 'Endangered'),
        ('VU', 'Vulnerable'),
        ('NT', 'Near Threatened'),
        ('LC', 'Least Concern'),
        ('DD', 'Data Deficient'),
        ('EW', 'Extinct in the Wild'),
        ('EX', 'Extinct'),
    ]
    
    TREND_CHOICES = [
        ('Increasing', 'Increasing'),
        ('Decreasing', 'Decreasing'),
        ('Stable', 'Stable'),
        ('Unknown', 'Unknown'),
    ]
    
    animal_name = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    pop_size = models.CharField(max_length=100, blank=True, null=True)
    trend = models.CharField(max_length=20, choices=TREND_CHOICES, blank=True, null=True)
    decline_rate = models.FloatField(blank=True, null=True, help_text="Decline rate in percentage")
    range_size = models.CharField(max_length=100, blank=True, null=True, help_text="Range size in km²")
    locations = models.CharField(max_length=100, blank=True, null=True)
    fragmented = models.CharField(max_length=50, blank=True, null=True)
    threats = models.TextField(blank=True, null=True)
    extinct_prob = models.FloatField(blank=True, null=True, help_text="Extinction probability in percentage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Species"
        ordering = ['animal_name']
    
    def __str__(self):
        return f"{self.animal_name} ({self.get_status_display()})"
