'''
tt = {
permutation:
reduce(lambda x, y: x * y, [bbn_node.func(*[argvals[arg_name] for arg_name in get_args(bbn_node.func)])
for bbn_node in bbn_nodes], 1)
for permutation in permutations}

for permutation in permutations:
    argvals = dict(permutation)
    potential = 1
    for bbn_node in bbn_nodes:
        bbn_node.clique = clique
        arg_list = []
        for arg_name in get_args(bbn_node.func):
            arg_list.append(argvals[arg_name])
        potential *= bbn_node.func(*arg_list)
    tt[permutation] = potential


for split in ['train', 'val']:
    filtered_annot = dict()
    for (ik, iv) in annotations[split].items():
        new_q = dict()
        for (qk, qv) in iv.items():
            if len(qv[1]['labels']) != 0:
                new_q[qk] = qv
        if len(new_q) != 0:
            filtered_annot[ik] = new_q
    annotations[split] = filtered_annot


annotations.update(
{split: {ik: new_q for (ik, iv) in annotations[split].items()
for (qk, qv) in iv.items() if len(qv[1]['labels']) != 0}
 for split in ['train', 'val'] if len(filtered_annot) != 0})

a_list=[1,2]
for i,name in enumerate(a_list,0):
    print("i,name: ",i,name)


for ((symbol, dur), rs) in gc_rangeset.items():
    gc_klines_diff.setdefault(symbol, {})
    gc_klines_diff[symbol][str(dur)] = {'data': {}}
    serial = _get_obj(self._data, ['klines', symbol, str(dur)])
    serial_binding = serial.get('binding', None)
    if serial_binding:
        gc_klines_diff[symbol][str(dur)]['binding'] = {s: {} for s in serial_binding.keys()}
    for (start_id, end_id) in rs:
        for i in range(start_id, end_id):
            gc_klines_diff[symbol][str(dur)]['data'][str(i)] = None
            if serial_binding:
                for (s, s_binding) in serial_binding.items():
                    gc_klines_diff[symbol][str(dur)]['binding'][s][str(i)] = None

gc_klines_diff = {(symbol, str(dur)):
{'data': {str(i): None for (start_id, end_id) in rs for i in range(start_id, end_id)}, 'binding': {s: {str(i): None for i in range(start_id, end_id)} for (s, s_binding) in serial_binding.items()} if serial_binding else None}
    for ((symbol, dur), rs) in gc_rangeset.items()
for serial_binding in [_get_obj(self._data, ['klines', symbol, str(dur)], {}).get('binding', None)]
}
'''


for question_type in ('question', 'help'):
    if question_type not in output:
        continue
    phrase = docassemble.base.functions.server.to_text(output[question_type])
    if not phrase or len(phrase) < 10:
        phrase = 'The sky is blue.'
    phrase = re.sub('[^A-Za-z 0-9\\.\\,\\?\\#\\!\\%\\&\\(\\)]', ' ', phrase)
    readability[question_type] = \
        [('Flesch Reading Ease', textstat.flesch_reading_ease(phrase)),
         ('Flesch-Kincaid Grade Level', textstat.flesch_kincaid_grade(phrase)),
         ('Gunning FOG Scale', textstat.gunning_fog(phrase)),
         ('SMOG Index', textstat.smog_index(phrase)),
         ('Automated Readability Index', textstat.automated_readability_index(phrase)),
         ('Coleman-Liau Index', textstat.coleman_liau_index(phrase)),
         ('Linsear Write Formula', textstat.linsear_write_formula(phrase)),
         ('Dale-Chall Readability Score', textstat.dale_chall_readability_score(phrase)),
         ('Readability Consensus', textstat.text_standard(phrase))]

readability = {question_type:
[('Flesch Reading Ease', textstat.flesch_reading_ease(phrase)),
 ('Flesch-Kincaid Grade Level', textstat.flesch_kincaid_grade(phrase)),
 ('Gunning FOG Scale', textstat.gunning_fog(phrase)),
 ('SMOG Index', textstat.smog_index(phrase)),
 ('Automated Readability Index', textstat.automated_readability_index(phrase)),
 ('Coleman-Liau Index', textstat.coleman_liau_index(phrase)),
 ('Linsear Write Formula', textstat.linsear_write_formula(phrase)),
 ('Dale-Chall Readability Score', textstat.dale_chall_readability_score(phrase)),
 ('Readability Consensus', textstat.text_standard(phrase))]
if question_type in output and len((phrase := re.sub('[^A-Za-z 0-9\\.\\,\\?\\#\\!\\%\\&\\(\\)]', ' ',
    docassemble.base.functions.server.to_text(output[question_type])))) >= 10
else [('Flesch Reading Ease', textstat.flesch_reading_ease('The sky is blue.')),
      ('Flesch-Kincaid Grade Level', textstat.flesch_kincaid_grade('The sky is blue.')),
      ('Gunning FOG Scale', textstat.gunning_fog('The sky is blue.')),
      ('SMOG Index', textstat.smog_index('The sky is blue.')),
      ('Automated Readability Index', textstat.automated_readability_index('The sky is blue.')),
      ('Coleman-Liau Index', textstat.coleman_liau_index('The sky is blue.')),
      ('Linsear Write Formula', textstat.linsear_write_formula('The sky is blue.')),
      ('Dale-Chall Readability Score', textstat.dale_chall_readability_score('The sky is blue.')),
      ('Readability Consensus', textstat.text_standard('The sky is blue.'))]
    for question_type in ('question', 'help')}
