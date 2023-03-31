import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'mysite.settings')

import django
django.setup()

from hrv.data_processing import enqueue, hrv_generator, get_ppg
from collections import deque
import random
import json
import string
import time
from datetime import datetime, timedelta

testing = True

ppg_data = deque()
ppg = []
measures = {}
num = 0
def test_data_processing(username):
    with open('unprocessed_data.json', 'r') as f:
        # Load the JSON data from the file into a Python variable
        unprocessed_data = json.load(f)
    print(type(unprocessed_data))

    global ppg_data, ppg, sampling_rate
    global measures
    global num
    successful_attempts = 0
    failed = 0
    measures_dict = {}
    error_types = []
    errors = {}
    error_type_count = {}
    for data in unprocessed_data.values():
        try:
            time = data['time']
            ppg_data = enqueue(ppg_data,data)
            sampling_rate, ppg, ppg_data = get_ppg(ppg_data, 60)
            working_data, measures = hrv_generator(measures, ppg, sampling_rate)
            if measures != {}:
                measures_dict[time] = json.dumps(measures)

                successful_attempts+=1
        except Exception as e:
            if type(e) not in error_types:
                error_types.append(type(e))
                errors[type(e)] = e
                error_type_count[type(e)] = 1
                #print(e)
            else:
                error_type_count[type(e)] = error_type_count[type(e)]+1
            failed+=1

    #print("Failed",failed, "times")
    #print(measures)
    print(successful_attempts,'successful_attempts.')


    print(failed,'failed')
    print("Success rate:",(successful_attempts/ len(unprocessed_data.values()))*100)

    print(error_type_count)

    #print(type(json.loads(measures_dict['2023-03-02T16:44:38.048'])))
    #print(type(measures_dict['2023-03-02T16:44:38.048']))

    return measures_dict

# Start execution here!
if __name__ == '__main__':
    print("Testing data_processing")
    test_data_processing("y")
    #save_user_data('y')
    #test_data_filtration(username)
    #testing()
    #userprofile = UserProfile.objects.filter(user__username__startswith = 'y')[0]
    #data = Data.objects.filter(user_id__startswith = userprofile.slug)
    #test_group_data(data)
