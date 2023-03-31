import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()
from hrv.models import DataCollection


def populate():
    data = [{"id": "1", "bpm": 66.9, "sdnn": 52.1, "rmssd": 55.4, "pnn20": 0.6,  "hr_mad": 33.1, "sd1": 0.6, "breathingrate": 0.2, "lf_hf": 2.3},
            {"id": "2", "bpm": 65, "sdnn": 50, "rmssd": 53.2, "pnn20": 0.5,  "hr_mad": 32.0, "sd1": 0.7, "breathingrate": 0.2, "lf_hf": 2.4},
            {"id": "3", "bpm": 68, "sdnn": 55, "rmssd": 54.7, "pnn20": 0.6,  "hr_mad": 31.7, "sd1": 0.6, "breathingrate": 0.2, "lf_hf": 2.3},
            {"id": "4", "bpm": 70, "sdnn": 57, "rmssd": 55.2, "pnn20": 0.7,  "hr_mad": 30.4, "sd1": 0.6, "breathingrate": 0.2, "lf_hf": 2.4},
            {"id": "5", "bpm": 72, "sdnn": 48, "rmssd": 57.7, "pnn20": 0.6,  "hr_mad": 29.5, "sd1": 0.8, "breathingrate": 0.2, "lf_hf": 2.3},
            {"id": "6", "bpm": 76, "sdnn": 59, "rmssd": 56.8, "pnn20": 0.7,  "hr_mad": 29.9, "sd1": 0.7, "breathingrate": 0.2, "lf_hf": 2.5},
            {"id": "7", "bpm": 71, "sdnn": 62, "rmssd": 55.9, "pnn20": 0.5,  "hr_mad": 30.2, "sd1": 0.6, "breathingrate": 0.2, "lf_hf": 2.3},
            {"id": "8", "bpm": 65, "sdnn": 54, "rmssd": 55.3, "pnn20": 0.6,  "hr_mad": 30.5, "sd1": 0.7, "breathingrate": 0.2, "lf_hf": 2.1},

            ]
    for x in data:
        add_data(x["id"], x["bpm"], x["sdnn"], x["rmssd"], x["pnn20"], x["hr_mad"], x["sd1"], x["breathingrate"], x["lf_hf"])

def add_data(id, bpm, sdnn,	rmssd,	pnn20,	hr_mad,	sd1, breathingrate, lf_hf):
    d = DataCollection.objects.get_or_create(id = id, BPM = bpm, sdnn= sdnn, rmssd = rmssd,	pnn20 = pnn20,	hr_mad = hr_mad, sd1 = sd1, breathingrate = breathingrate, lf_hf = lf_hf)[0]
    d.save()
    return d


if __name__ == '__main__':
    print("Starting population")
    populate()
    print("ending population")
