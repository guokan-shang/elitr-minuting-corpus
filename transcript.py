import os
import json
import numpy as np
from collections import defaultdict

if not os.path.exists('output/elitr-minuting-corpus-en/transcript'):
    os.makedirs('output/elitr-minuting-corpus-en/transcript')
if not os.path.exists('output/elitr-minuting-corpus-cs/transcript'):
    os.makedirs('output/elitr-minuting-corpus-cs/transcript')

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

    # geneder
    with open(meeting_path+'/'+'gender.tsv') as f:
        lines = [line.rstrip() for line in f]
    gender = {}
    for line in lines:
        gender[line.split('\t')[0]] = line.split('\t')[1]
    gender['UNKNOWN'] = 'UNKNOWN'
    gender['PERSON'] = 'UNKNOWN'

    # problem labels
    transcript_file = [file_name for file_name in os.listdir(meeting_path) if file_name.startswith('transcript_')][0]
    with open(meeting_path+'/'+transcript_file) as f:
        num_utterances = len(f.readlines())

    alignment_files = [file_name for file_name in os.listdir(meeting_path) if file_name.startswith('alignment+')]
    problem_labels = np.empty((num_utterances,len(alignment_files)), dtype=object)
    problem_labels.fill('None')

    for idx,alignment_file in enumerate(alignment_files):
        with open(meeting_path+'/'+alignment_file) as f:
            lines = [line.rstrip() for line in f]
    
        for line in lines:
            if int(line.split(' ')[0])-1 < num_utterances:
                problem_labels[int(line.split(' ')[0])-1][idx] = line.split(' ')[-1]

    # transcription
    transcript_file = [file_name for file_name in os.listdir(meeting_path) if file_name.startswith('transcript_')][0]
    with open(meeting_path+'/'+transcript_file) as f:
        lines = [line.rstrip() for line in f]

    transcript = []
    speaker = 'UNKNOWN'
    for idx,line in enumerate(lines):
        if line.startswith('(PERSON'):
            speaker = line[1:line.index(')')]
            text = line[line.index(')')+2:]
        else:
            text = line
        
        # resolve some speaker noise
        if speaker == 'PERSON4n':
            speaker = 'PERSON4'
        if speaker == 'PERSON1.':
            speaker = 'PERSON1'

        transcript.append({
            'id': meeting_id+'.u.'+str(idx+1),
            'speaker': speaker,
            'text': text,
            'problem': list(problem_labels[idx]),
            'gender': gender[speaker],
            'annotator': transcript_file[transcript_file.index('annot'):transcript_file.index('.')]
        })
    
    with open('output/elitr-minuting-corpus-'+en_or_cs+'/transcript'+'/'+meeting_id+'.json', 'w', encoding='utf-8') as f:
        json.dump(transcript, f, ensure_ascii=False)
