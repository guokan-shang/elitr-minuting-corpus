import os
import json
from collections import defaultdict

if not os.path.exists('output/elitr-minuting-corpus-en/alignment'):
    os.makedirs('output/elitr-minuting-corpus-en/alignment')
if not os.path.exists('output/elitr-minuting-corpus-cs/alignment'):
    os.makedirs('output/elitr-minuting-corpus-cs/alignment')

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

    # load transcription
    transcript = {}
    transcript_json = json.load(open('output/elitr-minuting-corpus-'+en_or_cs+'/transcript'+'/'+meeting_id+'.json'))
    for utterance in transcript_json:
        transcript[utterance['id']] = utterance

    # alignment
    alignment_files = [file_name for file_name in os.listdir(meeting_path) if file_name.startswith('alignment+')]

    for alignment_file in alignment_files:
        alignment = []
        
        communities = defaultdict(list)
        with open(meeting_path+'/'+alignment_file) as f:
            lines = [line.rstrip() for line in f]
    
        for idx,line in enumerate(lines):
            if line.split(' ')[1] == 'None':
                continue
            else:
                communities[line.split(' ')[1]].append(line.split(' ')[0])
        
        # load minute
        minute = {}
        minute_file = alignment_file.split('+')[-1]
        minute_json = json.load(open('output/elitr-minuting-corpus-'+en_or_cs+'/minute'+'/'+meeting_id+'_'+minute_file[minute_file.index('_')+1:minute_file.index('.')]+'.json'))
        for sentence in minute_json:
            minute[sentence['id']] = sentence

        # construct community
        for community_idx in communities.keys():
            abstractive = minute[meeting_id+'.'+minute_file[minute_file.index('_')+1:minute_file.index('.')]+'.'+community_idx]
            extractive = []
            for utterance_idx in communities[community_idx]:
                extractive.append(transcript[meeting_id+'.'+'u'+'.'+utterance_idx])

            alignment.append({
                'abstractive': abstractive,
                'extractive': extractive
            })

        with open('output/elitr-minuting-corpus-'+en_or_cs+'/alignment'+'/'+meeting_id+'_'+minute_file[minute_file.index('_')+1:minute_file.index('.')]+'.json', 'w', encoding='utf-8') as f:
            json.dump(alignment, f, ensure_ascii=False)