import zmq
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.tools as tls

import plotly

import plotly.graph_objs as go

import time
import datetime
import numpy as np

#socket
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://10.50.0.118:6300')
socket.setsockopt_string(zmq.SUBSCRIBE, '')


stream_tokens = tls.get_credentials_file()['stream_ids']
token_1 = stream_tokens[-1]
token_2 = stream_tokens[-2]
token_3 = stream_tokens[-3]
token_4 = stream_tokens[-4]
token_5 = stream_tokens[-5]
token_6 = stream_tokens[-6]

stream_id1 = dict(token=token_1, maxpoints=60)
stream_id2 = dict(token=token_2, maxpoints=60)
stream_id3 = dict(token=token_3, maxpoints=60)
stream_id4 = dict(token=token_4, maxpoints=60)
stream_id5 = dict(token=token_5, maxpoints=60)
stream_id6 = dict(token=token_6, maxpoints=60)

trace1 = go.Scatter(x=[], y=[], stream=stream_id1, name='trace1',  mode='lines+markers')
trace2 = go.Scatter(x=[], y=[], stream=stream_id2, name='trace2',  mode='lines+markers')
trace3 = go.Scatter(x=[], y=[], stream=stream_id3, name='trace3',  mode='lines+markers')
trace4 = go.Scatter(x=[], y=[], stream=stream_id4, name='trace4',  mode='lines+markers')
trace5 = go.Scatter(x=[], y=[], stream=stream_id5, name='trace5',  mode='lines+markers')
trace6 = go.Scatter(x=[], y=[], stream=stream_id6, name='trace6',  mode='lines+markers')


data = [trace1, trace2, trace3, trace4, trace5, trace6]
layout = go.Layout(
    title='Streaming Two Traces',
    yaxis=dict(
        title='y for trace1'
    )
    )

fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='multiple-trace-axes-streaming', auto_open=True)

s_1 = py.Stream(stream_id=token_1)
s_2 = py.Stream(stream_id=token_2)
s_3 = py.Stream(stream_id=token_3)
s_4 = py.Stream(stream_id=token_4)
s_5 = py.Stream(stream_id=token_5)
s_6 = py.Stream(stream_id=token_6)

s_1.open()
s_2.open()
s_3.open()
s_4.open()
s_5.open()
s_6.open()

keywords = ['England','America','France','North Korea','Chile']

#try:
while True:
    msg = socket.recv_string()
    print(msg)
    s,text = msg.split(' | ')
    t = datetime.datetime.now()
    for a in text:
        if 'ENGLAND' in text.upper():
            s_1.write(dict(x=t, y=s))
        elif 'AMERICA' in text.upper():
            s_2.write(dict(x=t, y=s))
        elif 'FRANCE' in text.upper():
            s_3.write(dict(x=t, y=s))
        elif 'NORTH KOREA' in text.upper():
            s_4.write(dict(x=t, y=s))
        elif 'CHILE' in text.upper():
            s_5.write(dict(x=t, y=s))
        else:
            s_6.write(dict(x=t, y=s))

            #time.sleep(0.8)
#except:
    #print('uh ohhhh')

#s_1.close()
#s_2.close()
#s_3.close()
#s_4.close()
#s_5.close()
#s_6.close()


tls.embed('streaming-demos','124')

