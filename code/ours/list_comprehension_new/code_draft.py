for view_directory in self.view_directories:
    if not os.path.exists(view_directory):
        log.warning(f'Failed to find toolbox view directory {view_directory}')
    for filename in os.listdir(view_directory):
        if not looks_like_view_source_filename(filename):
            continue
        view_path = os.path.join(view_directory, filename)
        with open(view_path) as f:
            view_dict = yaml.safe_load(f)
        if 'id' not in view_dict:
            file_id = os.path.splitext(filename)[0]
            view_dict['id'] = file_id
        view_definitions.append(StaticToolBoxView.from_dict(view_dict))



view_definitions += [StaticToolBoxView.from_dict(view_dict) for view_directory in self.view_directories
if os.path.exists(view_directory)
for filename in os.listdir(view_directory)
if looks_like_view_source_filename(filename)
for view_path in [os.path.join(view_directory, filename)]
for file_id in [os.path.splitext(filename)[0]]
for view_dict in
    [{'id': file_id, **yaml.safe_load(open(view_path))}
     if 'id' not in yaml.safe_load(open(view_path))
     else yaml.safe_load(open(view_path))]]



for y in range(size[1]):
    row = []
    x_min = 0
    for x_max in intervals[y] + [size[0]]:
        interval = []
        for x in range(x_min, x_max):
            if mask_data[x, y]:
                interval.append(image_data[x, y])
        if random.random() < randomness / 100:
            row += interval
        else:
            row += sort_interval(interval, sorting_function)
        x_min = x_max
    sorted_pixels.append(row)


sorted_pixels = [
[image_data[x, y] for x in range(x_min, x_max) if mask_data[x, y]]
if random.random() < randomness / 100
else sort_interval([image_data[x, y]
for x in range(x_min, x_max) if mask_data[x, y]], sorting_function)
for y in range(size[1])
for (x_min, x_max) in zip([0] + intervals[y], intervals[y] + [size[0]])]





for medium in tweet['extended_entities']['media']:
    if medium['type'] == 'photo':
        if '.' not in medium['media_url_https']:
            logger.warning(f"Skipping malformed medium URL on tweet {kwargs['id']}: {medium['media_url_https']!r} contains no dot")
            continue
        (baseUrl, format) = medium['media_url_https'].rsplit('.', 1)
        if format not in ('jpg', 'png'):
            logger.warning(f"Skipping photo with unknown format on tweet {kwargs['id']}: {format!r}")
            continue
        media.append(Photo(previewUrl=f'{baseUrl}?format={format}&name=small', fullUrl=f'{baseUrl}?format={format}&name=large'))
    elif medium['type'] == 'video' or medium['type'] == 'animated_gif':
        variants = []
        for variant in medium['video_info']['variants']:
            variants.append(VideoVariant(contentType=variant['content_type'], url=variant['url'], bitrate=variant.get('bitrate')))
        mKwargs = {'thumbnailUrl': medium['media_url_https'], 'variants': variants}
        if medium['type'] == 'video':
            mKwargs['duration'] = medium['video_info']['duration_millis'] / 1000
            if (ext := medium['ext']) and (mediaStats := ext['mediaStats']) and isinstance((r := mediaStats['r']), dict) and ('ok' in r) and isinstance(r['ok'], dict):
                mKwargs['views'] = int(r['ok']['viewCount'])
            cls = Video
        elif medium['type'] == 'animated_gif':
            cls = Gif
        media.append(cls(**mKwargs))


for elem_entry in elem_list:
    if elem_entry.tag == 'section':
        for existing_elem in config_elems:
            if existing_elem.tag == 'section' and existing_elem.attrib.get('id', None) == elem_entry.attrib.get('id', None):
                for child in elem_entry:
                    existing_elem.append(child)
                break
        else:
            config_elems.append(elem_entry)
    else:
        config_elems.append(elem_entry)


config_elems += [existing_elem.append(child)
if existing_elem.tag == 'section' and existing_elem.attrib.get('id', None) == elem_entry.attrib.get('id', None)
else config_elems.append(elem_entry)
if elem_entry.tag == 'section'
else config_elems.append(elem_entry)
for elem_entry in elem_list
for existing_elem in config_elems
if elem_entry.tag == 'section' and existing_elem.tag == 'section'
and (existing_elem.attrib.get('id', None) == elem_entry.attrib.get('id', None))]



for batch_index in range(pred.shape[0]):
    (height, width) = pred.shape[-2:]
    (tmp_boxes, tmp_scores) = self.boxes_from_bitmap(pred[batch_index], segmentation[batch_index], width, height)
    boxes = []
    for k in range(len(tmp_boxes)):
        if tmp_scores[k] > self.box_thresh:
            boxes.append(tmp_boxes[k])
    if len(boxes) > 0:
        boxes = np.array(boxes)
        (ratio_h, ratio_w) = ratio_list[batch_index]
        boxes[:, :, 0] = boxes[:, :, 0] / ratio_w
        boxes[:, :, 1] = boxes[:, :, 1] / ratio_h
    boxes_batch.append(boxes)


boxes_batch = [np.array([box / ratio_list[batch_index][1],
                         box / ratio_list[batch_index][0]])
for batch_index in range(pred.shape[0])
for (box, score) in zip(*self.boxes_from_bitmap(pred[batch_index], segmentation[batch_index], pred.shape[-1], pred.shape[-2]))
if score > self.box_thresh]



for e in ann_obj.get_events():
    if e.type in ignore_types:
        continue
    if restrict_types != [] and e.type not in restrict_types:
        continue
    try:
        t_ann = ann_obj.get_ann_by_id(e.trigger)
    except BaseException:
        Messager.error('Failed to retrieve trigger annotation %s, skipping event %s in search' % (e.trigger, e.id))
    if trigger_text is not None and trigger_text != '' and (trigger_text != DEFAULT_EMPTY_STRING) and (not trigger_match_regex.search(t_ann.text)):
        continue
    arg_constraints = []
    for arg in args:
        if arg['role'] != '' or arg['type'] != '' or arg['text'] != '':
            arg_constraints.append(arg)
    args = arg_constraints
    if len(args) > 0:
        missing_match = False
        for arg in args:
            for s in ('role', 'type', 'text'):
                assert s in arg, "Error: missing mandatory field '%s' in event search" % s
            found_match = False
            for (role, aid) in e.args:
                if arg['role'] is not None and arg['role'] != '' and (arg['role'] != role):
                    continue
                arg_ent = ann_obj.get_ann_by_id(aid)
                if arg['type'] is not None and arg['type'] != '' and (arg['type'] != arg_ent.type):
                    continue
                if arg['text'] is not None and arg['text'] != '':
                    match_regex = _get_match_regex(arg['text'], text_match, match_case)
                    if match_regex is None:
                        return matches
                    if isinstance(arg_ent, annotation.EventAnnotation):
                        text_ent = ann_obj.get_ann_by_id(ann_ent.trigger)
                    else:
                        text_ent = arg_ent
                    if not match_regex.search(text_ent.get_text()):
                        continue
                found_match = True
                break
            if not found_match:
                missing_match = True
                break
        if missing_match:
            continue
    ann_matches.append((t_ann, e))


ann_matches = [(t_ann, e) for e in ann_obj.get_events()
if e.type not in ignore_types and (restrict_types == [] or e.type in restrict_types) and (trigger_text is None or trigger_text == '' or trigger_text == DEFAULT_EMPTY_STRING or trigger_match_regex.search(ann_obj.get_ann_by_id(e.trigger).text)) and all((s in arg for s in ('role', 'type', 'text'))) and (not any((arg['role'] is not None and arg['role'] != role or (arg['type'] is not None and arg['type'] != ann_obj.get_ann_by_id(aid).type) or (arg['text'] is not None and arg['text'] != '' and (not _get_match_regex(arg['text'], text_match, match_case).search(ann_obj.get_ann_by_id(aid).get_text()))) for arg in args)))
for t_ann in [ann_obj.get_ann_by_id(e.trigger)]
if isinstance(t_ann, annotation.TextBoundAnnotation)]



for y in range(size[1]):
    row = []
    x_min = 0
    for x_max in intervals[y] + [size[0]]:
        interval = []
        for x in range(x_min, x_max):
            if mask_data[x, y]:
                interval.append(image_data[x, y])
        if random.random() < randomness / 100:
            row += interval
        else:
            row += sort_interval(interval, sorting_function)
        x_min = x_max
    sorted_pixels.append(row)


sorted_pixels = [[image_data[x, y] for x in range(x_min, x_max) if mask_data[x, y]]
if random.random() < randomness / 100
else sort_interval([image_data[x, y]
for x in range(x_min, x_max) if mask_data[x, y]], sorting_function)
for y in range(size[1])
for (x_min, x_max) in zip([0] + intervals[y], intervals[y] + [size[0]])]



for file_name in file_names:
    file_features = features[features.file_names == file_name]
    number_notes = Counter(file_features.num_notes)
    notes = []
    for ele in number_notes:
        if number_notes[ele] > 1:
            notes.append(ele)
    h_pits = []
    for note in notes:
        number_h_pit = Counter(file_features[file_features.num_notes == note].h_pit)
        for ele in number_h_pit:
            if number_h_pit[ele] > 1:
                h_pits.append(ele)
    l_pits = []
    for h_pit in h_pits:
        number_l_pit = Counter(file_features[file_features.h_pit == h_pit].l_pit)
        for ele in number_l_pit:
            if number_l_pit[ele] > 1:
                l_pits.append(ele)
    notes = list(set(notes))
    h_pits = list(set(h_pits))
    l_pits = list(set(l_pits))
    for note in notes:
        note_index = file_features[file_features.num_notes == note].index.values
        for h_pit in h_pits:
            h_pit_index = file_features[file_features.h_pit == h_pit].index.values
            for l_pit in l_pits:
                l_pit_index = file_features[file_features.l_pit == l_pit].index.values
                index_intersect = reduce(np.intersect1d, (note_index, h_pit_index, l_pit_index))
                if len(index_intersect) > 1:
                    duplicates.append(index_intersect)

duplicates = [
reduce(np.intersect1d, (file_features[file_features.num_notes == note].index.values, file_features[file_features.h_pit == h_pit].index.values, file_features[file_features.l_pit == l_pit].index.values))

    for file_name in file_names for note in list(set([ele for (ele, count) in Counter(features[features.file_names == file_name].num_notes).items() if count > 1])) for h_pit in list(set([ele for (note_value, note_count) in Counter(features[features.file_names == file_name].num_notes).items() if note_count > 1 for (ele, count) in Counter(features[(features.file_names == file_name) & (features.num_notes == note_value)].h_pit).items() if count > 1])) for l_pit in list(set([ele for (note_value, note_count) in Counter(features[features.file_names == file_name].num_notes).items() if note_count > 1 for (h_pit_value, h_pit_count) in Counter(features[(features.file_names == file_name) & (features.num_notes == note_value)].h_pit).items() if h_pit_count > 1 for (ele, count) in Counter(features[(features.file_names == file_name) & (features.num_notes == note_value) & (features.h_pit == h_pit_value)].l_pit).items() if count > 1])) if len(reduce(np.intersect1d, (file_features[file_features.num_notes == note].index.values, file_features[file_features.h_pit == h_pit].index.values, file_features[file_features.l_pit == l_pit].index.values))) > 1]



for k in l:
    for m in self.shutit_modules:
        if m.module_id == k:
            count = 1
            compatible = True
            if not cfg[m.module_id]['shutit.core.module.build']:
                cfg[m.module_id]['shutit.core.module.build'] = True
                compatible = self.determine_compatibility(m.module_id) == 0
            if long_output:
                table_list.append([str(count), m.module_id, m.description, str(m.run_order), str(cfg[m.module_id]['shutit.core.module.build']), str(compatible)])
            else:
                table_list.append([m.module_id, m.description, str(cfg[m.module_id]['shutit.core.module.build']), str(compatible)])




table_list.update([
[str(count), m.module_id, m.description, str(m.run_order), str(cfg[m.module_id]['shutit.core.module.build']), str(self.determine_compatibility(m.module_id) == 0)]
if long_output
else
[m.module_id, m.description, str(cfg[m.module_id]['shutit.core.module.build']), str(self.determine_compatibility(m.module_id) == 0)]

for k in l
for m in self.shutit_modules if m.module_id == k])



for item in schema_base.registry.mappers:
    cls = item.class_
    if type(cls) == DeclarativeMeta:
        for provider in providers:
            if issubclass(cls, Mixin):
                cls.register_provider(provider)
        if zvt_context.dbname_map_schemas.get(db_name):
            schemas = zvt_context.dbname_map_schemas[db_name]
        zvt_context.schemas.append(cls)
        if entity_type:
            add_to_map_list(the_map=zvt_context.entity_map_schemas, key=entity_type, value=cls)
        schemas.append(cls)



schemas = [cls
for item in schema_base.registry.mappers
if type((cls := item.class_)) == DeclarativeMeta
for provider in providers
if issubclass(cls, Mixin) and cls.register_provider(provider) and
    zvt_context.dbname_map_schemas.get(db_name) and
    (schemas := zvt_context.dbname_map_schemas[db_name]) and
zvt_context.schemas.append(cls) and add_to_map_list(the_map=zvt_context.entity_map_schemas, key=entity_type, value=cls)
and schemas.append(cls)]



rst = [{'id': k, **rst_items[k]} if len(rst_items[k]['correct_text']) == len(rst_items[k]['original_text'])
else {'id': k, 'correct_text': text, 'original_text': text, 'wrong_ids': []}
for (k, text) in [(k, rst_items[k]['correct_text'])
for k in rst_items.keys()]]


for elem_entry in elem_list:
    if elem_entry.tag == 'section':
        for existing_elem in config_elems:
            if existing_elem.tag == 'section' and existing_elem.attrib.get('id', None) == elem_entry.attrib.get('id', None):
                for child in elem_entry:
                    existing_elem.append(child)
                break
        else:
            config_elems.append(elem_entry)
    else:
        config_elems.append(elem_entry)



config_elems.update(
[existing_elem.append(child)
 if existing_elem.tag == 'section' and existing_elem.attrib.get('id', None) == elem_entry.attrib.get('id', None)
 else config_elems.append(elem_entry)
if elem_entry.tag == 'section'
else config_elems.append(elem_entry)
 for elem_entry in elem_list
 for existing_elem in config_elems
 if elem_entry.tag == 'section' and existing_elem.tag == 'section'
 and (existing_elem.attrib.get('id', None) == elem_entry.attrib.get('id', None))])



for batch_index in range(pred.shape[0]):
    (height, width) = pred.shape[-2:]
    (tmp_boxes, tmp_scores) = self.boxes_from_bitmap(pred[batch_index], segmentation[batch_index], width, height)
    boxes = []
    for k in range(len(tmp_boxes)):
        if tmp_scores[k] > self.box_thresh:
            boxes.append(tmp_boxes[k])
    if len(boxes) > 0:
        boxes = np.array(boxes)
        (ratio_h, ratio_w) = ratio_list[batch_index]
        boxes[:, :, 0] = boxes[:, :, 0] / ratio_w
        boxes[:, :, 1] = boxes[:, :, 1] / ratio_h
    boxes_batch.append(boxes)

boxes_batch = [np.array(
[box / ratio_list[batch_index][1], box / ratio_list[batch_index][0]])
    for batch_index in range(pred.shape[0])
    for (box, score) in zip(*self.boxes_from_bitmap(pred[batch_index], segmentation[batch_index], pred.shape[-1], pred.shape[-2])) if score > self.box_thresh]



for factor in factors:
    X = np.repeat(data.data, factor, axis=0)
    y = np.repeat(data.target, factor, axis=0)
    local_speedups = []
    for trial in range(trials):
        local_speedups.append(pcoords_speedup(X, y))
    local_speedups = np.array(local_speedups)
    speedups.append(local_speedups.mean())
    variance.append(local_speedups.std())