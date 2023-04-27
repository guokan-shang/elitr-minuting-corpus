# ELITR Minuting Corpus
This is a python3 project that converts some annotations of the [ELITR Minuting Corpus](http://hdl.handle.net/11234/1-4692) from the original TEXT format into the JSON format, to be consistent with the format of [ami-and-icsi-corpora](https://github.com/guokan-shang/ami-and-icsi-corpora).

The processed corpora can be directly downloaded from [here](https://drive.google.com/drive/folders/1YnhWBOTKeFicrAvZl_4z-VI4Dl3lECN_?usp=sharing) (last update 21/04/2023).

Click ► in below to see example and explication of each annotation.

If you want to run the code yourself, please follow the following instructions.

1. Extract [ELITR Minuting Corpus (ELITR-minuting-corpus.zip)](http://groups.inf.ed.ac.uk/ami/download/) under `input/ELITR-minuting-corpus`.

2. Run the following Python scripts to obtain respective annotations in JSON format under `output/`.

* **Manual meeting transcriptions** (transcript.py). Note: you should run this script first.
<details>
  <summary>example</summary>

```json
[
   ...,
   {
      "id":"meeting_en_dev_003.u.4",
      "speaker":"PERSON12",
      "text":"And maybe you, you could write some this, some of the sections, I think.",
      "problem":[
         "1",
         "None"
      ],
      "gender":"male",
      "annotator":"annot18"
   },
   ...
]
```
`id` denotes utterance id, e.g., "meeting_en_dev_003" refers to the meeting id, "u" to "utterance", "4" to the line number of the utterance in orginal transcript file.

`speaker` and `gender` denotes the deidentified speaker tags, and their gender, sometimes they both can be `UNKNOWN`.
The ID numbers are shuffled and unique for each meeting, i.e. PERSON1 denotes the same person across all the files of one meeting but a different person in the files of another meeting.

`annotator` denotes the annotator of the transcript.

`problem` denotes problematic or interesting properties of the utterance, e.g., ["1","None"] means there are two annotators, the first one thinks this utterance relates to organizational talk, and the second one find it contains no problematic or interesting properties. `problem` can be empty `[]`.

```
1 - Organizational
    Organizational talk not directly related to the subject of the meeting
    (e.g. discussing technical issues with the video call).
2 - Speech incomprehensible
    It is not clear what the speaker is saying.
3 - Other issue
4 - Small talk
    Small talk or conversation unrelated to the subject of the meeting
    (e.g. discussing the weather).
5 - Censored
    This part of the transcript had to be removed for privacy reasons.
```

```
The text can contain entities, which are enclosed in square brackets, of types: 
PERSON, ORGANIZATION, PROJECT, LOCATION, ANNOTATOR, URL, 
NUMBER, PASSWORD, PHONE, PATH, EMAIL, OTHER.

The transcript data also contains the following tags:

<another_language>...</another_language> or <another_language/>
  speech in a different language than the rest of the transcript
<typing/>
  sounds of typing
<parallel_talk>...</parallel_talk> or <parallel_talk/>
  speakers talking over each other
<cough/>
  coughing
<other_yawn/>
  yawning
<censored/>
  section of the transcript has been censored for privacy
  or ethical reasons
<laugh/>
  laughter
<unintelligible/>
  speech is not comprehensible
<other_sigh/>
  sighing
<talking_to_self/>
  speaker talking to themselves
<other_noise/>
  another further unspecified noise
```
</details>


* **Extractive summaries** (extractive.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"meeting_en_dev_003.u.11",
      "speaker":"PERSON12",
      "text":"So, so let's go on agenda.",
      "problem":[
         "None",
         "None"
      ],
      "gender":"male",
      "annotator":"annot18"
   },
   {
      "id":"meeting_en_dev_003.u.12",
      "speaker":"PERSON12",
      "text":"First we have accepted paper to [OTHER8], to [PROJECT2].",
      "problem":[
         "None",
         "None"
      ],
      "gender":"male",
      "annotator":"annot18"
   },
   ...
]
```
One meeting can have zero to multiple extractive summaries, the file(s) are named in two ways:
- [meeting_id]_ORIG.json, summary provided by meeting organizer.
- [meeting_id]_GENER_annot[YY].json, summary provided by the annotator YY.

</details>


* **Meeting minutes / Abstractive summaries** (minute.py)
<details>
  <summary>example</summary>

```json
[
   ...,
   {
      "id":"meeting_en_dev_004.GENER_annot18.13",
      "text":"- [PERSON5] explained [PERSON17] what he wanted to say in his comments"
   },
   {
      "id":"meeting_en_dev_004.GENER_annot18.14",
      "text":"- the next meeting is planned on 21th July"
   },
   ...
]
```
One meeting can have zero to multiple minutes, the file(s) are named in two ways:
- [meeting_id]_ORIG.json, the original agenda or minutes, written by meeting organizer.
- [meeting_id]_GENER_annot[YY].json, the minutes files, i.e. summaries written by the annotator YY.

The format of minute is somewhat free form but is always in the form of bullet points rather than a coherent text summary.

</details>


* **Alignment / Abstractive summaries** (alignment.py)
<details>
  <summary>example</summary>

```json
[
   {
      "abstractive":{
         "id":"meeting_en_dev_004.GENER_annot02.9",
         "text":"- inform that his part of book is ready to comments, except introduction and morfology."
      },
      "extractive":[
         {
            "id":"meeting_en_dev_004.u.94",
            "speaker":"PERSON6",
            "text":"OK, um, so I'm still missing the introduction so it's stil this, um, this, this bullets which I plan to rewrite into the text like one to put this text away.",
            "problem":[
               "None",
               "None"
            ],
            "gender":"male",
            "annotator":"annot18"
         },
         {
            "id":"meeting_en_dev_004.u.95",
            "speaker":"PERSON6",
            "text":"And I still didn't touch morfology so I still need to rewrite it into sentences.",
            "problem":[
               "None",
               "None"
            ],
            "gender":"male",
            "annotator":"annot18"
         },
         ...
         ]
   },
   ...
]
```
One meeting can have zero to multiple minutes, the file(s) are named in two ways:
- [meeting_id]_ORIG.json, the alignments between `minute/[meeting_id]_ORIG.json` and `transcript/[meeting_id].json`
- [meeting_id]_GENER_annot[YY].json, the alignments between `minute/[meeting_id]_GENER_annot[YY].json` and `transcript/[meeting_id].json`

</details>

For more details of these annotations, please refer to the `README` and `stats.tsv` of the original corpus and the citations in below.

# Training, Validation, and Test Sets
The data is separated into the following directories:
- elitr-minuting-corpus-en: the English data
- elitr-minuting-corpus-cs: the Czech data
Meetings are further split into train, dev, test and test2 sets by their ids.

```python
elitr_en_train = ['meeting_en_train_'+f'{idx:03}' for idx in range(1,85)]
elitr_en_dev = ['meeting_en_dev_'+f'{idx:03}' for idx in range(1,11)]
elitr_en_test = ['meeting_en_test_'+f'{idx:03}' for idx in range(1,19)]
elitr_en_test2 = ['meeting_en_test2_'+f'{idx:03}' for idx in range(1,9)]

elitr_cs_train = ['meeting_cs_train_'+f'{idx:03}' for idx in range(1,34)]
elitr_cs_dev = ['meeting_cs_dev_'+f'{idx:03}' for idx in range(1,11)]
elitr_cs_test = ['meeting_cs_test_'+f'{idx:03}' for idx in range(1,11)]
elitr_cs_test2 = ['meeting_cs_test2_'+f'{idx:03}' for idx in range(1,7)]
```


# Citations
In addition to the original dataset paper, if you find this repository helpful, please consider to cite the publications:

[1] [Abstractive Meeting Summarization: A Survey](https://arxiv.org/abs/2208.04163)
```
@article{rennard2022abstractive,
  title={Abstractive Meeting Summarization: A Survey},
  author={Rennard, Virgile and Shang, Guokan and Hunter, Julie and Vazirgiannis, Michalis},
  journal={arXiv preprint arXiv:2208.04163},
  year={2022}
}
```
[2] [Energy-based Self-attentive Learning of Abstractive Communities for Spoken Language Understanding](https://aclanthology.org/2020.aacl-main.34/)
```
@inproceedings{shang2020energy,
  title={Energy-based Self-attentive Learning of Abstractive Communities for Spoken Language Understanding},
  author={Shang, Guokan and Tixier, Antoine and Vazirgiannis, Michalis and Lorr{\'e}, Jean-Pierre},
  booktitle={Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing},
  pages={313--327},
  year={2020}
}
```
[3] [Spoken Language Understanding for Abstractive Meeting Summarization](https://tel.archives-ouvertes.fr/tel-03169877/document)
```
@phdthesis{shang2021spoken,
  title={Spoken Language Understanding for Abstractive Meeting Summarization},
  author={Shang, Guokan},
  year={2021},
  school={Institut polytechnique de Paris}
}
```
[4] [Unsupervised abstractive meeting summarization with multi-sentence compression and budgeted submodular maximization](https://aclanthology.org/P18-1062/)
```
@article{shang2018unsupervised,
  title={Unsupervised abstractive meeting summarization with multi-sentence compression and budgeted submodular maximization},
  author={Shang, Guokan and Ding, Wensi and Zhang, Zekun and Tixier, Antoine Jean-Pierre and Meladianos, Polykarpos and Vazirgiannis, Michalis and Lorr{\'e}, Jean-Pierre},
  journal={arXiv preprint arXiv:1805.05271},
  year={2018}
}
```
