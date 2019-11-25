
from django.db import models

# Create your models here.
from django.db import models

pol = (
    ('М' , "М"),
    ('Ж' , "Ж")
)


class users(models.Model):

    fullname = models.CharField(max_length=200)
    age = models.DateField()
    pol = models.CharField(choices=pol , max_length=10)
    specialite = models.CharField(max_length=100)
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname


class vibor_test(models.Model):

    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

class stimul_slov(models.Model):
    a = 'stimul'
    stimulus = models.CharField(max_length=200)
    test_id = models.ForeignKey(vibor_test, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s" % (self.id , self.stimulus)

class otvet(models.Model):

    answer = models.CharField(max_length=200)
    user_id = models.ForeignKey(users, on_delete=models.CASCADE)
    test_id = models.ForeignKey(vibor_test, on_delete=models.CASCADE)
    stimul_id = models.ForeignKey(stimul_slov, on_delete=models.CASCADE)
    def __str__(self):
        return  self.answer

class userlink(models.Model):

    user_id = models.ForeignKey(users, on_delete=models.CASCADE)
    vibor_test_id = models.ForeignKey(vibor_test, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s " % (self.user_id, self.vibor_test_id, )
