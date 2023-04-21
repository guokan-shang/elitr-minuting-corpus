import os
import json
from collections import defaultdict

if not os.path.exists('output/elitr-minuting-corpus-en/minute'):
    os.makedirs('output/elitr-minuting-corpus-en/minute')
if not os.path.exists('output/elitr-minuting-corpus-cs/minute'):
    os.makedirs('output/elitr-minuting-corpus-cs/minute')

meeting_list_en = [
    ['input/ELITR-minuting-corpus/elitr-minuting-corpus-en'+'/'+partition+'/'+meeting_id 
    for meeting_id in os.listdir('input/ELITR-minuting-corpus/elitr-minuting-corpus-en'+'/'+partition)] 
    for partition in ['train', 'test2', 'test', 'dev']
    ]

meeting_list_cs = [
    ['input/ELITR-minuting-corpus/elitr-minuting-corpus-cs'+'/'+partition+'/'+meeting_id 
    for meeting_id in os.listdir('input/ELITR-minuting-corpus/elitr-minuting-corpus-cs'+'/'+partition)] 
    for partition in ['train', 'test2', 'test', 'dev']
    ]

def flatten(l):
    return [item for sublist in l for item in sublist]

for meeting_path in flatten(meeting_list_en)+flatten(meeting_list_cs):
    meeting_id = meeting_path.split('/')[-1]
    en_or_cs = 'en' if '_en_' in meeting_id else 'cs'

    # ORIG minitue
    if 'minutes_ORIG.txt' in os.listdir(meeting_path):
        with open(meeting_path+'/'+'minutes_ORIG.txt') as f:
            lines = [line.rstrip() for line in f]

        minute = []
        for idx,line in enumerate(lines):
            minute.append({
                'id': meeting_id+'.ORIG.'+str(idx+1),
                'text': line
            })
        
        with open('output/elitr-minuting-corpus-'+en_or_cs+'/minute'+'/'+meeting_id+'_ORIG.json', 'w', encoding='utf-8') as f:
            json.dump(minute, f, ensure_ascii=False)

    # GENER minute
    minute_files = [file_name for file_name in os.listdir(meeting_path) if file_name.startswith('minutes_GENER_')]
    for minute_file in minute_files:
        with open(meeting_path+'/'+minute_file) as f:
            lines = [line.rstrip() for line in f]
        
        minute = []
        for idx,line in enumerate(lines):
            minute.append({
                'id': meeting_id+'.'+minute_file[minute_file.index('_')+1:minute_file.index('.')]+'.'+str(idx+1),
                'text': line
            })
            
        with open('output/elitr-minuting-corpus-'+en_or_cs+'/minute'+'/'+meeting_id+'_'+minute_file[minute_file.index('_')+1:minute_file.index('.')]+'.json', 'w', encoding='utf-8') as f:
            json.dump(minute, f, ensure_ascii=False)
