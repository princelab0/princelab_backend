from django.db import models

# Create your models here.
class AI_APP(models.Model):
    fields_options={
        ('cardiology','Cardiology'),
        ('neurology','neurology'),
        ( 'opthamology','opthamology'),
        ('pshycology','pshycology'),
        ('oncology','oncology'),
    }
    name=models.CharField(max_length=50, verbose_name='Full NAME',blank=False, null=True)
    Type=models.CharField(max_length=20,verbose_name="Type ", choices=fields_options,blank=False,null=True)
    image=models.ImageField(verbose_name='Profile picture',blank=False,null=True)
    describe=models.CharField(max_length=800,verbose_name='description',blank=False,null=True)

