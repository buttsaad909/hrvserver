from django.shortcuts import render
from django.http import HttpResponse
import json
from collections import deque
from hrv.models import DataCollection
from django.template import loader
from datetime import datetime, timedelta
from .data_processing import enqueue, hrv_generator, get_ppg
import matplotlib.pyplot as plt
import base64
from io import BytesIO, StringIO

ppg_data = deque()
ppg = []
measures = {}
num = 0


from .models import CountdownTimer
from .forms import CountdownTimerForm

# Create your views here.

def index(request):
    # global ppg, ppg_data, measures
    # sampling_rate, ppg, ppg_data = get_ppg(100, ppg_data)
    # working_data, measures = hrv_generator(measures, ppg, sampling_rate)
    return HttpResponse("hello HRV")

# 接口函数
def post(request):
    global ppg_data, ppg, sampling_rate
    global measures
    global num
    context_dict = {}
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        num += 1
        print(num)
        data = json.loads(request.body)
        # print(data["total_event"])
        if len(data):
            ppg_data = enqueue(ppg_data, data)
            sampling_rate, ppg, ppg_data = get_ppg(ppg_data, 60)
            working_data, measures = hrv_generator(measures, ppg, sampling_rate)
    
            '''
            {'bpm': nan, 'ibi': nan, 'sdnn': nan, 
            'rmssd': nan, 'pnn20': nan, 'pnn50': nan, 'hr_mad': nan, 
            'sd1': nan, 'sd2': nan, 's': nan, 'sd1/sd2': nan, 'breathingrate': nan, 
            'vlf': nan, 'lf': nan, 'hf': nan, 'lf/hf': nan}
            '''
    '''
    if len(measures):
        D = DataCollection.objects.get_or_create(date=datetime.data.now(),BPM=measures['bpm'], ibi=measures['ibi'], sdnn=measures['sdnn'], rmssd=measures['rmssd'], 
        pnn20=measures['pnn20'], pnn50=measures['pnn50'], hr_mad=measures['hr_mad'], sd1=measures['sd1'], sd2=measures['sd2'], s=measures['s'], sd1_sd2=measures['sd1/sd2'], 
        breathingrate=measures['breathingrate'], vlf=measures['vlf'], lf=measures['lf'], hf=measures['hf'], lf_hf=measures['lf/hf'])[0]
        D.save()
    print(measures)
    '''
    data = DataCollection.objects.all()
    #print(data[0].BPM)

    avgBPM = 0
    avgsdnn = 0
    avgrmssd = 0
    avgpnn20 = 0
    avghr_mad = 0
    avgsd1 = 0
    avgbreathingrate = 0
    avglf_hf = 0
    
    for i in range (len(data)-1):
        avgBPM += data[i].BPM
        avgsdnn += data[i].sdnn
        avgrmssd += data[i].rmssd
        avgpnn20 += data[i].pnn20
        avghr_mad += data[i].hr_mad
        avgsd1 += data[i].sd1
        avgbreathingrate += data[i].breathingrate
        avglf_hf += data[i].lf_hf


    avgBPM = avgBPM/ len(data)
    avgsdnn = avgsdnn/ len(data)
    avgrmssd = avgrmssd/ len(data)
    avgpnn20 = avgpnn20/ len(data)
    avghr_mad = avghr_mad/ len(data)
    avgsd1 = avgsd1/ len(data)
    avgbreathingrate = avgbreathingrate/ len(data)
    avglf_hf = avglf_hf/ len(data)

    context_dict["avgBPM"] = avgBPM
    context_dict["avgsdnn"] = avgsdnn
    context_dict["avgrmssd"] = avgrmssd
    context_dict["avgpnn20"] = avgpnn20
    context_dict["avghr_mad"] = avghr_mad
    context_dict["avgsd1"] = avgsd1
    context_dict["avgbreathingrate"] = avgbreathingrate
    context_dict["avglf_hf"] = avglf_hf


    return render(request, "measures.html", context_dict)
    '''
    template = loader.get_template('measures.html')
    context = {
        "measures": measures
    }
    return HttpResponse(template.render(context, request))
    '''

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3), facecolor='none')
    plt.title("Stress Visualisation")
    plt.plot(x,y,color='red', marker='o')
    ax = plt.axes()
    ax.set_facecolor("none")
    plt.xlabel("Readings")
    plt.ylabel('BPM')
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_bar_chart():
    labels = ["Monday", "Tuesday", "Wednesday"]
    values = [23, 45, 34]
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Stress Level")
    ax.set_title("Stress Levels over the past week")
    ax.set_facecolor("none")
    fig.patch.set_facecolor('none')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return chart_data

def get_pie_chart():
    labels = ["Meditation", "Yoga", "Exercise", "Sleep", "Dinning", "Hobbies", "Work"]
    values = [8, 12, 10 ,32, 5, 15, 18]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title("Methods On Improving Stress Levels")
    fig.patch.set_facecolor('none')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return chart_data

def page(request):
    context_dict = {}
    data1 = DataCollection.objects.all()
    x = [x.id for x in data1]
    y = [y.BPM for y in data1]
    chart = get_plot(x,y)
    chart_data = get_bar_chart()
    pie_chart_data = get_pie_chart()
    context_dict["pie_chart_data"] = pie_chart_data
    context_dict["chart_data"] = chart_data
    context_dict["chart"] = chart
    return render(request, "page.html", context_dict)

def page2(request):
    form = CountdownTimerForm(request.POST or None)
    timer = None

    if form.is_valid():
        timer = form.save()
        end_time = datetime.now() + timedelta(seconds=timer.seconds)
        timer.end_time = end_time
        timer.save()

    context = {
        'form': form,
        'timer': timer,
    }
    return render(request, "page2.html", context)