from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class PPG(models.Model):
    date = models.DateTimeField('date inserted')
    time_stamp = models.IntegerField(default=0)
    ppg_signal = models.FloatField(default=0.0)


class DataCollection(models.Model):
    id = models.CharField(max_length= 100, primary_key= True)
    BPM = models.FloatField(default=0.00)
    sdnn = models.FloatField(default=0.00)
    rmssd = models.FloatField(default=0.00)
    pnn20 = models.FloatField(default=0.00)
    hr_mad = models.FloatField(default=0.00)
    sd1 = models.FloatField(default=0.00)
    breathingrate = models.FloatField(default=0.00)
    lf_hf = models.FloatField(default=0.00)

    def __str__(self):
        return self.id


class CountdownTimer(models.Model):
    seconds = models.IntegerField()