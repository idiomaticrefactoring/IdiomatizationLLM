def prepare_test_img(self, idx):
    """Prepare an image for testing.

        :param idx: index
        :type idx: int
        :return: an item of data according to the index
        :rtype: dict
        """
    target_pair = self.image_annot_path_pairs[idx]
    image_arr = imread(target_pair['image_path'])
    lane_object = self.read_annot(target_pair['annot_path'])
    whc = get_img_whc(image_arr)
    network_input_image = bgr2rgb(resize_by_wh(img=image_arr, width=512, height=288))
    item = dict(net_input_image=imagenet_normalize(img=network_input_image), net_input_image_mode='RGB', net_input_image_shape=dict(width=512, height=288, channel=3), src_image_shape=whc, src_image_path=target_pair['image_path'], annotation_path=target_pair['annot_path'], annotation_src_content=lane_object, regression_groundtruth=None, classfication_groundtruth=None)
    result = dict(image=np.transpose(item['net_input_image'], (2, 0, 1)).astype('float32'), net_input_image_shape=json.dumps(item['net_input_image_shape']), src_image_shape=json.dumps(item['src_image_shape']), annot=json.dumps(item['annotation_src_content']), src_image_path=item['src_image_path'], annotation_path=item['annotation_path'])
    return result


servers_prague_loc = (
            (self.PRIO_LOW, new_weight, DNSName(self.master.hostname)),
            (self.PRIO_HIGH, self.WEIGHT, DNSName(self.replicas[0].hostname)),
            (self.PRIO_LOW, self.WEIGHT, DNSName(self.replicas[1].hostname)),
        )
domain_prague_loc = (
            DNSName('{}._locations'.format(self.LOC_PRAGUE)) + DNSName(
                self.master.domain.name).make_absolute())

servers_paris_loc = (
            (self.PRIO_HIGH, new_weight, DNSName(self.master.hostname)),
            (self.PRIO_LOW, self.WEIGHT, DNSName(self.replicas[0].hostname)),
            (self.PRIO_HIGH, self.WEIGHT, DNSName(self.replicas[1].hostname)),
        )
domain_paris_loc = (
            DNSName('{}._locations'.format(self.LOC_PARIS)) + DNSName(
                self.master.domain.name).make_absolute())


self.fc0 = layers.fc(
            size=hid0_size,
            act='tanh',
            param_attr=ParamAttr(name='{}/h0/W'.format(scope_name)),
            bias_attr=ParamAttr(name='{}/h0/b'.format(scope_name)))
self.fc1 = layers.fc(
            size=hid1_size,
            act='tanh',
            param_attr=ParamAttr(name='{}/h1/W'.format(scope_name)),
            bias_attr=ParamAttr(name='{}/h1/b'.format(scope_name)))
self.vel_fc0 = layers.fc(
            size=vel_hid0_size,
            act='tanh',
            param_attr=ParamAttr(name='{}/vel_h0/W'.format(scope_name)),
            bias_attr=ParamAttr(name='{}/vel_h0/b'.format(scope_name)))
self.vel_fc1 = layers.fc(
            size=vel_hid1_size,
            act='tanh',
            param_attr=ParamAttr(name='{}/vel_h1/W'.format(scope_name)),
            bias_attr=ParamAttr(name='{}/vel_h1/b'.format(scope_name)))



def get_updated_changeset_revisions_for_repository_dependencies(self, key_rd_dicts):
    updated_key_rd_dicts = []
    for key_rd_dict in key_rd_dicts:
        key = next(iter(key_rd_dict))
        repository_dependency = key_rd_dict[key]
        (rd_toolshed, rd_name, rd_owner, rd_changeset_revision, rd_prior_installation_required, rd_only_if_compiling_contained_td) = common_util.parse_repository_dependency_tuple(repository_dependency)
        if suc.tool_shed_is_this_tool_shed(rd_toolshed):
            repository = tool_shed.util.repository_util.get_repository_by_name_and_owner(self.app, rd_name, rd_owner)
            if repository:
                repository_id = self.app.security.encode_id(repository.id)
                repository_metadata = metadata_util.get_repository_metadata_by_repository_id_changeset_revision(self.app, repository_id, rd_changeset_revision)
                if repository_metadata:
                    new_key_rd_dict = {}
                    new_key_rd_dict[key] = repository_dependency
                    updated_key_rd_dicts.append(key_rd_dict)
                else:
                    changeset_revision = metadata_util.get_next_downloadable_changeset_revision(self.app, repository, rd_changeset_revision)
                    if changeset_revision != rd_changeset_revision:
                        repository_metadata = metadata_util.get_repository_metadata_by_repository_id_changeset_revision(self.app, repository_id, changeset_revision)
                    if repository_metadata:
                        new_key_rd_dict = {}
                        new_key_rd_dict[key] = [rd_toolshed, rd_name, rd_owner, repository_metadata.changeset_revision, rd_prior_installation_required, rd_only_if_compiling_contained_td]
                        updated_key_rd_dicts.append(new_key_rd_dict)
                    else:
                        repository_components_tuple = container_util.get_components_from_key(key)
                        components_list = tool_shed.util.repository_util.extract_components_from_tuple(repository_components_tuple)
                        (toolshed, repository_name, repository_owner, repository_changeset_revision) = components_list[0:4]
                        if len(components_list) in (4, 5):
                            rd_only_if_compiling_contained_td = 'False'
                        message = 'The revision %s defined for repository %s owned by %s is invalid, so repository ' % (str(rd_changeset_revision), str(rd_name), str(rd_owner))
                        message += f'dependencies defined for repository {str(repository_name)} will be ignored.'
                        log.debug(message)
            else:
                repository_components_tuple = container_util.get_components_from_key(key)
                components_list = tool_shed.util.repository_util.extract_components_from_tuple(repository_components_tuple)
                (toolshed, repository_name, repository_owner, repository_changeset_revision) = components_list[0:4]
                message = 'The revision %s defined for repository %s owned by %s is invalid, so repository ' % (str(rd_changeset_revision), str(rd_name), str(rd_owner))
                message += f'dependencies defined for repository {str(repository_name)} will be ignored.'
                log.debug(message)
    return updated_key_rd_dicts


def test_update_mastodon_pictures_get_actor_404(self):
    self.expect_requests_get('https://foo.com' + test_mastodon.API_ACCOUNT % 123, headers={'Authorization': 'Bearer towkin'}).AndRaise(requests.exceptions.HTTPError(response=util.Struct(status_code='404', text='foo')))
    self.mox.ReplayAll()
    mastodon = self._setup_mastodon()
    resp = self.client.get('/cron/update_mastodon_pictures')
    self.assertEqual(200, resp.status_code)
    self.assertEqual('http://before', mastodon.key.get().picture)

def test_argon2_cffi_using_the_official_command_line_utility(self) -> None:
    min_password_length = 1
    max_password_length = 127
    min_salt_length = 8
    min_parallelism = 1
    max_parallelism = multiprocessing.cpu_count()
    min_time_cost = 1
    min_memory_cost = 7
    min_key_length = 4
    max_salt_length = 128
    max_time_cost = 3
    max_memory_cost = 15
    max_key_length = 64
    sys_rand = random.SystemRandom()
    for _ in range(self.number_of_tests):
        len_password = sys_rand.randint(min_password_length, max_password_length)
        len_salt = sys_rand.randint(min_salt_length, max_salt_length)
        parallelism = sys_rand.randint(min_parallelism, max_parallelism)
        time_cost = sys_rand.randint(min_time_cost, max_time_cost)
        memory_cost = sys_rand.randint(min_memory_cost, max_memory_cost)
        key_length = sys_rand.randint(min_key_length, max_key_length)
        password = ''.join([sys_rand.choice(ascii_letters + digits) for _ in range(len_password)])
        salt = ''.join([sys_rand.choice(ascii_letters + digits) for _ in range(len_salt)])
        output = subprocess.check_output(f'echo -n "{password}" | ./argon2 {salt} -t {time_cost} -m {memory_cost} -p {parallelism} -l {key_length} -id', shell=True).decode()
        key_test_vector = output.split('\n')[4].split('\t')[-1]
        purported_key = argon2.low_level.hash_secret_raw(secret=password.encode(), salt=salt.encode(), time_cost=time_cost, memory_cost=2 ** memory_cost, parallelism=parallelism, hash_len=key_length, type=argon2.Type.ID).hex()
        self.assertEqual(purported_key, key_test_vector)



def _real_extract(self, url):
    list_id = self._match_id(url)
    webpage = self._download_webpage(url, list_id)
    entries = [self.url_result('http://www.imdb.com' + m, 'Imdb') for m in re.findall('href="(/list/ls%s/videoplayer/vi[^"]+)"' % list_id, webpage)]
    list_title = self._html_search_regex('<h1[^>]+class="[^"]*header[^"]*"[^>]*>(.*?)</h1>', webpage, 'list title')
    list_description = self._html_search_regex('<div[^>]+class="[^"]*list-description[^"]*"[^>]*><p>(.*?)</p>', webpage, 'list description')
    return self.playlist_result(entries, list_id, list_title, list_description)

def to_feature_list(self, tokenizer, max_seq_length, doc_stride, max_query_length, set_type):
    is_training = set_type == PHASE.TRAIN
    features = []
    if is_training and (not self.is_impossible):
        start_position = self.start_position
        end_position = self.end_position
        actual_text = ' '.join(self.doc_tokens[start_position:end_position + 1])
        cleaned_answer_text = ' '.join(whitespace_tokenize(self.answer_text))
        if actual_text.find(cleaned_answer_text) == -1:
            logger.warning("Could not find answer: '%s' vs. '%s'", actual_text, cleaned_answer_text)
            return []
    tok_to_orig_index = []
    orig_to_tok_index = []
    all_doc_tokens = []
    for (i, token) in enumerate(self.doc_tokens):
        orig_to_tok_index.append(len(all_doc_tokens))
        if tokenizer.__class__.__name__ in ['RobertaTokenizer', 'LongformerTokenizer', 'BartTokenizer', 'RobertaTokenizerFast', 'LongformerTokenizerFast', 'BartTokenizerFast']:
            sub_tokens = tokenizer.tokenize(token, add_prefix_space=True)
        else:
            sub_tokens = tokenizer.tokenize(token)
        for sub_token in sub_tokens:
            tok_to_orig_index.append(i)
            all_doc_tokens.append(sub_token)
    if is_training and (not self.is_impossible):
        tok_start_position = orig_to_tok_index[self.start_position]
        if self.end_position < len(self.doc_tokens) - 1:
            tok_end_position = orig_to_tok_index[self.end_position + 1] - 1
        else:
            tok_end_position = len(all_doc_tokens) - 1
        (tok_start_position, tok_end_position) = _improve_answer_span(all_doc_tokens, tok_start_position, tok_end_position, tokenizer, self.answer_text)
    spans = []
    truncated_query = tokenizer.encode(self.question_text, add_special_tokens=False, truncation=True, max_length=max_query_length)
    tokenizer_type = type(tokenizer).__name__.replace('Tokenizer', '').lower()
    sequence_added_tokens = tokenizer.model_max_length - tokenizer.max_len_single_sentence + 1 if tokenizer_type in MULTI_SEP_TOKENS_TOKENIZERS_SET else tokenizer.model_max_length - tokenizer.max_len_single_sentence
    sequence_pair_added_tokens = tokenizer.model_max_length - tokenizer.max_len_sentences_pair
    span_doc_tokens = all_doc_tokens
    while len(spans) * doc_stride < len(all_doc_tokens):
        if tokenizer.padding_side == 'right':
            texts = truncated_query
            pairs = span_doc_tokens
            truncation = TruncationStrategy.ONLY_SECOND.value
        else:
            texts = span_doc_tokens
            pairs = truncated_query
            truncation = TruncationStrategy.ONLY_FIRST.value
        encoded_dict = tokenizer.encode_plus(texts, pairs, truncation=truncation, padding='max_length', max_length=max_seq_length, return_overflowing_tokens=True, stride=max_seq_length - doc_stride - len(truncated_query) - sequence_pair_added_tokens, return_token_type_ids=True)
        paragraph_len = min(len(all_doc_tokens) - len(spans) * doc_stride, max_seq_length - len(truncated_query) - sequence_pair_added_tokens)
        if tokenizer.pad_token_id in encoded_dict['input_ids']:
            if tokenizer.padding_side == 'right':
                non_padded_ids = encoded_dict['input_ids'][:encoded_dict['input_ids'].index(tokenizer.pad_token_id)]
            else:
                last_padding_id_position = len(encoded_dict['input_ids']) - 1 - encoded_dict['input_ids'][::-1].index(tokenizer.pad_token_id)
                non_padded_ids = encoded_dict['input_ids'][last_padding_id_position + 1:]
        else:
            non_padded_ids = encoded_dict['input_ids']
        tokens = tokenizer.convert_ids_to_tokens(non_padded_ids)
        token_to_orig_map = {}
        for i in range(paragraph_len):
            index = len(truncated_query) + sequence_added_tokens + i if tokenizer.padding_side == 'right' else i
            token_to_orig_map[index] = tok_to_orig_index[len(spans) * doc_stride + i]
        encoded_dict['paragraph_len'] = paragraph_len
        encoded_dict['tokens'] = tokens
        encoded_dict['token_to_orig_map'] = token_to_orig_map
        encoded_dict['truncated_query_with_special_tokens_length'] = len(truncated_query) + sequence_added_tokens
        encoded_dict['token_is_max_context'] = {}
        encoded_dict['start'] = len(spans) * doc_stride
        encoded_dict['length'] = paragraph_len
        spans.append(encoded_dict)
        if 'overflowing_tokens' not in encoded_dict or ('overflowing_tokens' in encoded_dict and len(encoded_dict['overflowing_tokens']) == 0):
            break
        span_doc_tokens = encoded_dict['overflowing_tokens']
    for doc_span_index in range(len(spans)):
        for j in range(spans[doc_span_index]['paragraph_len']):
            is_max_context = _new_check_is_max_context(spans, doc_span_index, doc_span_index * doc_stride + j)
            index = j if tokenizer.padding_side == 'left' else spans[doc_span_index]['truncated_query_with_special_tokens_length'] + j
            spans[doc_span_index]['token_is_max_context'][index] = is_max_context
    for span in spans:
        cls_index = span['input_ids'].index(tokenizer.cls_token_id)
        p_mask = np.ones_like(span['token_type_ids'])
        if tokenizer.padding_side == 'right':
            p_mask[len(truncated_query) + sequence_added_tokens:] = 0
        else:
            p_mask[-len(span['tokens']):-(len(truncated_query) + sequence_added_tokens)] = 0
        pad_token_indices = np.where(span['input_ids'] == tokenizer.pad_token_id)
        special_token_indices = np.asarray(tokenizer.get_special_tokens_mask(span['input_ids'], already_has_special_tokens=True)).nonzero()
        p_mask[pad_token_indices] = 1
        p_mask[special_token_indices] = 1
        p_mask[cls_index] = 0
        span_is_impossible = self.is_impossible
        start_position = 0
        end_position = 0
        if is_training and (not span_is_impossible):
            doc_start = span['start']
            doc_end = span['start'] + span['length'] - 1
            out_of_span = False
            if not (tok_start_position >= doc_start and tok_end_position <= doc_end):
                out_of_span = True
            if out_of_span:
                start_position = cls_index
                end_position = cls_index
                span_is_impossible = True
            else:
                if tokenizer.padding_side == 'left':
                    doc_offset = 0
                else:
                    doc_offset = len(truncated_query) + sequence_added_tokens
                start_position = tok_start_position - doc_start + doc_offset
                end_position = tok_end_position - doc_start + doc_offset
        features.append(DataRow(unique_id='', qas_id=self.qas_id, tokens=span['tokens'], token_to_orig_map=span['token_to_orig_map'], token_is_max_context=span['token_is_max_context'], input_ids=np.array(span['input_ids']), input_mask=np.array(span['attention_mask']), segment_ids=np.array(span['token_type_ids']), cls_index=np.array(cls_index), p_mask=np.array(p_mask.tolist()), paragraph_len=span['paragraph_len'], start_position=start_position, end_position=end_position, answers=self.answers, doc_tokens=self.doc_tokens))
    return features



def to_feature_list(self, tokenizer, max_seq_length, doc_stride, max_query_length, set_type):
    is_training = set_type == PHASE.TRAIN
    features = []
    if is_training and (not self.is_impossible):
        start_position = self.start_position
        end_position = self.end_position
        actual_text = ' '.join(self.doc_tokens[start_position:end_position + 1])
        cleaned_answer_text = ' '.join(whitespace_tokenize(self.answer_text))
        if actual_text.find(cleaned_answer_text) == -1:
            logger.warning("Could not find answer: '%s' vs. '%s'", actual_text, cleaned_answer_text)
            return []
    tok_to_orig_index = []
    orig_to_tok_index = []
    all_doc_tokens = []
    for (i, token) in enumerate(self.doc_tokens):
        orig_to_tok_index.append(len(all_doc_tokens))
        if tokenizer.__class__.__name__ in ['RobertaTokenizer', 'LongformerTokenizer', 'BartTokenizer', 'RobertaTokenizerFast', 'LongformerTokenizerFast', 'BartTokenizerFast']:
            sub_tokens = tokenizer.tokenize(token, add_prefix_space=True)
        else:
            sub_tokens = tokenizer.tokenize(token)
        for sub_token in sub_tokens:
            tok_to_orig_index.append(i)
            all_doc_tokens.append(sub_token)
    if is_training and (not self.is_impossible):
        tok_start_position = orig_to_tok_index[self.start_position]
        if self.end_position < len(self.doc_tokens) - 1:
            tok_end_position = orig_to_tok_index[self.end_position + 1] - 1
        else:
            tok_end_position = len(all_doc_tokens) - 1
        (tok_start_position, tok_end_position) = _improve_answer_span(all_doc_tokens, tok_start_position, tok_end_position, tokenizer, self.answer_text)
    spans = []
    truncated_query = tokenizer.encode(self.question_text, add_special_tokens=False, truncation=True, max_length=max_query_length)
    tokenizer_type = type(tokenizer).__name__.replace('Tokenizer', '').lower()
    sequence_added_tokens = tokenizer.model_max_length - tokenizer.max_len_single_sentence + 1 if tokenizer_type in MULTI_SEP_TOKENS_TOKENIZERS_SET else tokenizer.model_max_length - tokenizer.max_len_single_sentence
    sequence_pair_added_tokens = tokenizer.model_max_length - tokenizer.max_len_sentences_pair
    span_doc_tokens = all_doc_tokens
    while len(spans) * doc_stride < len(all_doc_tokens):
        if tokenizer.padding_side == 'right':
            texts = truncated_query
            pairs = span_doc_tokens
            truncation = TruncationStrategy.ONLY_SECOND.value
        else:
            texts = span_doc_tokens
            pairs = truncated_query
            truncation = TruncationStrategy.ONLY_FIRST.value
        encoded_dict = tokenizer.encode_plus(texts, pairs, truncation=truncation, padding='max_length', max_length=max_seq_length, return_overflowing_tokens=True, stride=max_seq_length - doc_stride - len(truncated_query) - sequence_pair_added_tokens, return_token_type_ids=True)
        paragraph_len = min(len(all_doc_tokens) - len(spans) * doc_stride, max_seq_length - len(truncated_query) - sequence_pair_added_tokens)
        if tokenizer.pad_token_id in encoded_dict['input_ids']:
            if tokenizer.padding_side == 'right':
                non_padded_ids = encoded_dict['input_ids'][:encoded_dict['input_ids'].index(tokenizer.pad_token_id)]
            else:
                last_padding_id_position = len(encoded_dict['input_ids']) - 1 - encoded_dict['input_ids'][::-1].index(tokenizer.pad_token_id)
                non_padded_ids = encoded_dict['input_ids'][last_padding_id_position + 1:]
        else:
            non_padded_ids = encoded_dict['input_ids']
        tokens = tokenizer.convert_ids_to_tokens(non_padded_ids)
        token_to_orig_map = {}
        for i in range(paragraph_len):
            index = len(truncated_query) + sequence_added_tokens + i if tokenizer.padding_side == 'right' else i
            token_to_orig_map[index] = tok_to_orig_index[len(spans) * doc_stride + i]
        encoded_dict['paragraph_len'] = paragraph_len
        encoded_dict['tokens'] = tokens
        encoded_dict['token_to_orig_map'] = token_to_orig_map
        encoded_dict['truncated_query_with_special_tokens_length'] = len(truncated_query) + sequence_added_tokens
        encoded_dict['token_is_max_context'] = {}
        encoded_dict['start'] = len(spans) * doc_stride
        encoded_dict['length'] = paragraph_len
        spans.append(encoded_dict)
        if 'overflowing_tokens' not in encoded_dict or ('overflowing_tokens' in encoded_dict and len(encoded_dict['overflowing_tokens']) == 0):
            break
        span_doc_tokens = encoded_dict['overflowing_tokens']
    for doc_span_index in range(len(spans)):
        for j in range(spans[doc_span_index]['paragraph_len']):
            is_max_context = _new_check_is_max_context(spans, doc_span_index, doc_span_index * doc_stride + j)
            index = j if tokenizer.padding_side == 'left' else spans[doc_span_index]['truncated_query_with_special_tokens_length'] + j
            spans[doc_span_index]['token_is_max_context'][index] = is_max_context
    for span in spans:
        cls_index = span['input_ids'].index(tokenizer.cls_token_id)
        p_mask = np.ones_like(span['token_type_ids'])
        if tokenizer.padding_side == 'right':
            p_mask[len(truncated_query) + sequence_added_tokens:] = 0
        else:
            p_mask[-len(span['tokens']):-(len(truncated_query) + sequence_added_tokens)] = 0
        pad_token_indices = np.where(span['input_ids'] == tokenizer.pad_token_id)
        special_token_indices = np.asarray(tokenizer.get_special_tokens_mask(span['input_ids'], already_has_special_tokens=True)).nonzero()
        p_mask[pad_token_indices] = 1
        p_mask[special_token_indices] = 1
        p_mask[cls_index] = 0
        span_is_impossible = self.is_impossible
        start_position = 0
        end_position = 0
        if is_training and (not span_is_impossible):
            doc_start = span['start']
            doc_end = span['start'] + span['length'] - 1
            out_of_span = False
            if not (tok_start_position >= doc_start and tok_end_position <= doc_end):
                out_of_span = True
            if out_of_span:
                start_position = cls_index
                end_position = cls_index
                span_is_impossible = True
            else:
                if tokenizer.padding_side == 'left':
                    doc_offset = 0
                else:
                    doc_offset = len(truncated_query) + sequence_added_tokens
                start_position = tok_start_position - doc_start + doc_offset
                end_position = tok_end_position - doc_start + doc_offset
        features.append(DataRow(unique_id='', qas_id=self.qas_id, tokens=span['tokens'], token_to_orig_map=span['token_to_orig_map'], token_is_max_context=span['token_is_max_context'], input_ids=np.array(span['input_ids']), input_mask=np.array(span['attention_mask']), segment_ids=np.array(span['token_type_ids']), cls_index=np.array(cls_index), p_mask=np.array(p_mask.tolist()), paragraph_len=span['paragraph_len'], start_position=start_position, end_position=end_position, answers=self.answers, doc_tokens=self.doc_tokens))
    return features



def run_use_fleet_api_trainer(self, args):
    assert args.update_method == 'nccl2' or 'bkcl'
    self.lr = args.lr
    exec_strategy = fluid.ExecutionStrategy()
    exec_strategy.num_threads = 1
    dist_strategy = DistributedStrategy()
    dist_strategy.exec_strategy = exec_strategy
    dist_strategy.fuse_memory_size = 1
    dist_strategy.fuse_laryer_size = 1
    if args.use_local_sgd:
        dist_strategy.use_local_sgd = True
    if args.ut4grad_allreduce:
        dist_strategy._ut4grad_allreduce = True
    if args.sync_batch_norm:
        dist_strategy.sync_batch_norm = True
    role = role_maker.PaddleCloudRoleMaker(is_collective=True)
    fleet.init(role)
    print_to_err('use_fleet', 'fleet.node_num:')
    (test_program, avg_cost, train_reader, test_reader, batch_acc, predict) = self.get_model(batch_size=args.batch_size, dist_strategy=dist_strategy)
    trainer_prog = fleet._origin_program
    dist_prog = fleet.main_program
    if fluid.core.is_compiled_with_cuda():
        device_id = int(os.getenv('FLAGS_selected_gpus', '0'))
        place = fluid.CUDAPlace(device_id)
    elif fluid.core.is_compiled_with_xpu():
        device_id = int(os.getenv('FLAGS_selected_xpus', '0'))
        place = fluid.XPUPlace(device_id)
    else:
        raise ValueError('fleet dygraph api must in paddlepaddle-xpu or paddlepaddle-gpu.')
    exe = fluid.Executor(place)
    exe.run(fluid.default_startup_program())
    eprint(type(self).__name__, 'run worker startup program done.')
    feed_var_list = [var for var in trainer_prog.global_block().vars.values() if var.is_data]
    eprint('feed_var_list:', feed_var_list)
    if feed_var_list[0].name == 'label':
        feed_var_list = feed_var_list[::-1]
    feeder = fluid.DataFeeder(feed_var_list, place)
    reader_generator = train_reader()

    def get_data():
        origin_batch = next(reader_generator)
        if args.update_method != 'local' and args.use_reader_alloc:
            new_batch = []
            for (offset, item) in enumerate(origin_batch):
                if offset % 2 == args.trainer_id:
                    new_batch.append(item)
            return new_batch
        else:
            return origin_batch
    print_to_err(type(self).__name__, 'begin to train on trainer')
    out_losses = []
    for i in range(RUN_STEP):
        (loss,) = exe.run(dist_prog, fetch_list=[avg_cost.name], feed=feeder.feed(get_data()))
        out_losses.append(loss[0])
        print_to_err(type(self).__name__, 'run step %d finished' % i)
    print_to_err(type(self).__name__, 'trainer run finished')
    sys.stdout.buffer.write(pickle.dumps(out_losses))
    if args.save_model:
        model_save_dir = '/tmp'
        if fleet.worker_index() == 0:
            model_save_dir_fluid = os.path.join(model_save_dir, 'fluid_persistables')
            model_save_dir_fleet = os.path.join(model_save_dir, 'fleet_persistables')
            infer_save_dir_fluid = os.path.join(model_save_dir, 'fluid_infer')
            infer_save_dir_fleet = os.path.join(model_save_dir, 'fleet_infer')
        else:
            model_save_dir_fluid = os.path.join(model_save_dir, 'fluid_persistables_2')
            model_save_dir_fleet = os.path.join(model_save_dir, 'fleet_persistables_2')
            infer_save_dir_fluid = os.path.join(model_save_dir, 'fluid_infer_2')
            infer_save_dir_fleet = os.path.join(model_save_dir, 'fleet_infer_2')
        paddle.distributed.io.save_persistables(exe, model_save_dir_fluid, fleet._origin_program)
        fleet.save_persistables(executor=exe, dirname=model_save_dir_fleet)
        feeded_var_names = [var.name for var in feed_var_list]
        fluid.io.save_inference_model(infer_save_dir_fluid, feeded_var_names, [avg_cost], exe, fleet._origin_program)
        fleet.save_inference_model(exe, infer_save_dir_fleet, feeded_var_names, [avg_cost])



def render_pep440_post_branch(pieces):
    """TAG[.postDISTANCE[.dev0]+gHEX[.dirty]] .

    The ".dev0" means not master branch.

    Exceptions:
    1: no tags. 0.postDISTANCE[.dev0]+gHEX[.dirty]
    """
    if pieces['closest-tag']:
        rendered = pieces['closest-tag']
        if pieces['distance'] or pieces['dirty']:
            rendered += '.post%d' % pieces['distance']
            if pieces['branch'] != 'master':
                rendered += '.dev0'
            rendered += plus_or_dot(pieces)
            rendered += 'g%s' % pieces['short']
            if pieces['dirty']:
                rendered += '.dirty'
    else:
        rendered = '0.post%d' % pieces['distance']
        if pieces['branch'] != 'master':
            rendered += '.dev0'
        rendered += '+g%s' % pieces['short']
        if pieces['dirty']:
            rendered += '.dirty'
    return rendered




def find_maximums(self, model, num, exclusive):
    tic = time.time()
    (temp, n_iter, early_stop, log_interval) = (self.temp, self.n_iter, self.early_stop, self.log_interval)
    if self.persistent and self.points is not None:
        points = self.points
    else:
        points = self.task.config_space.sample_ints(self.parallel_size)
    scores = model.predict(points)
    heap_items = [(float('-inf'), -1 - i) for i in range(num)]
    heapq.heapify(heap_items)
    in_heap = set(exclusive)
    in_heap.update([x[1] for x in heap_items])
    for (s, p) in zip(scores, points):
        if s > heap_items[0][0] and p not in in_heap:
            pop = heapq.heapreplace(heap_items, (s, p))
            in_heap.remove(pop[1])
            in_heap.add(p)
    k = 0
    k_last_modify = 0
    if isinstance(temp, (tuple, list, np.ndarray)):
        t = temp[0]
        cool = 1.0 * (temp[0] - temp[1]) / (n_iter + 1)
    else:
        t = temp
        cool = 0
    while k < n_iter and k < k_last_modify + early_stop:
        new_points = np.empty_like(points)
        for (i, p) in enumerate(points):
            new_points[i] = self.task.config_space.random_walk(p)
        new_scores = model.predict(new_points)
        ac_prob = np.exp(np.minimum((new_scores - scores) / (t + 1e-05), 1))
        ac_index = np.random.random(len(ac_prob)) < ac_prob
        points[ac_index] = new_points[ac_index]
        scores[ac_index] = new_scores[ac_index]
        for (s, p) in zip(new_scores, new_points):
            if s > heap_items[0][0] and p not in in_heap:
                pop = heapq.heapreplace(heap_items, (s, p))
                in_heap.remove(pop[1])
                in_heap.add(p)
                k_last_modify = k
        k += 1
        t -= cool
        if log_interval and k % log_interval == 0:
            t_str = '%.2f' % t
            logger.debug('SA iter: %d\tlast_update: %d\tmax-0: %.2f\tmax-1: %.2f\ttemp: %s\telapsed: %.2f', k, k_last_modify, heap_items[0][0], np.max([v for (v, _) in heap_items]), t_str, time.time() - tic)
    heap_items.sort(key=lambda item: -item[0])
    heap_items = [x for x in heap_items if x[0] >= 0]
    logger.debug('SA iter: %d\tlast_update: %d\telapsed: %.2f', k, k_last_modify, time.time() - tic)
    logger.debug('SA Maximums: %s', heap_items)
    if self.persistent:
        self.points = points
    return [x[1] for x in heap_items]


def deleted_histories(self, trans, **kwd):
    """
        The number of histories that were deleted more than the specified number of days ago, but have not yet been purged.
        Also included is the number of datasets associated with the histories.
        """
    params = util.Params(kwd)
    message = ''
    if params.deleted_histories_days:
        deleted_histories_days = int(params.deleted_histories_days)
        cutoff_time = datetime.utcnow() - timedelta(days=deleted_histories_days)
        history_count = 0
        dataset_count = 0
        disk_space = 0
        histories = trans.sa_session.query(model.History).filter(and_(model.History.table.c.deleted == true(), model.History.table.c.purged == false(), model.History.update_time < cutoff_time)).options(eagerload('datasets'))
        for history in histories:
            for hda in history.datasets:
                if not hda.dataset.purged:
                    dataset_count += 1
                    try:
                        disk_space += hda.dataset.file_size
                    except Exception:
                        pass
            history_count += 1
        message = '%d histories ( including a total of %d datasets ) were deleted more than %d days ago, but have not yet been purged, disk space: %s.' % (history_count, dataset_count, deleted_histories_days, nice_size(disk_space, True))
    else:
        message = 'Enter the number of days.'
    return (str(deleted_histories_days), message)


def main():
    bruteforce_tests = dict()
    for filename in os.listdir(API_DEFINITIONS):
        if not filename.endswith('.min.json'):
            continue
        api_json_data = open(os.path.join(API_DEFINITIONS, filename)).read()
        api_json = json.loads(api_json_data)
        service_name = extract_service_name(filename, api_json)
        if service_name is None:
            print('%s does not define a service name' % filename)
            continue
        operations = extract_operations(api_json)
        if not operations:
            continue
        if service_name in bruteforce_tests:
            bruteforce_tests[service_name].extend(operations)
        else:
            bruteforce_tests[service_name] = operations
    output = OUTPUT_FMT % json.dumps(bruteforce_tests, indent=4, sort_keys=True)
    open(OUTPUT_FILE, 'w').write(output)



def train(config, data_folder, learning_rate=0.0001, max_epoch=None):
    """ Train the Gensen model.

    Args:
        max_epoch(int): Limit training to specified number of epochs.
        config(dict): Loaded json file as a python object.
        data_folder(str): Path to the folder containing the data.
        learning_rate(float): Learning rate for the model.
    """
    owd = os.getcwd()
    os.chdir(data_folder)
    try:
        with mlflow.start_run():
            save_dir = config['data']['save_dir']
            if not os.path.exists('./log'):
                os.makedirs('./log')
            os.makedirs(save_dir, exist_ok=True)
            setup_logging(config)
            batch_size = config['training']['batch_size']
            src_vocab_size = config['model']['n_words_src']
            trg_vocab_size = config['model']['n_words_trg']
            max_len_src = config['data']['max_src_length']
            max_len_trg = config['data']['max_trg_length']
            model_state = {}
            train_src = [item['train_src'] for item in config['data']['paths']]
            train_trg = [item['train_trg'] for item in config['data']['paths']]
            tasknames = [item['taskname'] for item in config['data']['paths']]
            if 'skipthought_next' in tasknames and 'skipthought_previous' in tasknames:
                skipthought_idx = tasknames.index('skipthought_next')
                skipthought_backward_idx = tasknames.index('skipthought_previous')
                paired_tasks = {skipthought_idx: skipthought_backward_idx, skipthought_backward_idx: skipthought_idx}
            else:
                paired_tasks = None
                skipthought_idx = None
                skipthought_backward_idx = None
            train_iterator = BufferedDataIterator(train_src, train_trg, src_vocab_size, trg_vocab_size, tasknames, save_dir, buffer_size=1000000.0, lowercase=True, seed=(hvd.rank() + 1) * 12345)
            nli_iterator = NLIIterator(train=config['data']['nli_train'], dev=config['data']['nli_dev'], test=config['data']['nli_test'], vocab_size=-1, vocab=os.path.join(save_dir, 'src_vocab.pkl'), seed=(hvd.rank() + 1) * 12345)
            src_vocab_size = len(train_iterator.src[0]['word2id'])
            trg_vocab_size = len(train_iterator.trg[0]['word2id'])
            logging.info('Finished creating iterator ...')
            log_config(config)
            logging.info('Found %d words in source : ' % len(train_iterator.src[0]['id2word']))
            for (idx, taskname) in enumerate(tasknames):
                logging.info('Found %d target words in task %s ' % (len(train_iterator.trg[idx]['id2word']), taskname))
            logging.info('Found %d words in src ' % src_vocab_size)
            logging.info('Found %d words in trg ' % trg_vocab_size)
            weight_mask = torch.ones(trg_vocab_size).cuda()
            weight_mask[train_iterator.trg[0]['word2id']['<pad>']] = 0
            loss_criterion = nn.CrossEntropyLoss(weight=weight_mask).cuda()
            nli_criterion = nn.CrossEntropyLoss().cuda()
            model = MultitaskModel(src_emb_dim=config['model']['dim_word_src'], trg_emb_dim=config['model']['dim_word_trg'], src_vocab_size=src_vocab_size, trg_vocab_size=trg_vocab_size, src_hidden_dim=config['model']['dim_src'], trg_hidden_dim=config['model']['dim_trg'], bidirectional=config['model']['bidirectional'], pad_token_src=train_iterator.src[0]['word2id']['<pad>'], pad_token_trg=train_iterator.trg[0]['word2id']['<pad>'], nlayers_src=config['model']['n_layers_src'], dropout=config['model']['dropout'], num_tasks=len(train_iterator.src), paired_tasks=paired_tasks).cuda()
            optimizer = setup_horovod(model, learning_rate=learning_rate)
            logging.info(model)
            n_gpus = config['training']['n_gpus']
            model = torch.nn.DataParallel(model, device_ids=range(n_gpus))
            task_losses = [[] for _ in tasknames]
            task_idxs = [0 for _ in tasknames]
            nli_losses = []
            updates = 0
            nli_ctr = 0
            nli_epoch = 0
            monitor_epoch = 0
            nli_mbatch_ctr = 0
            mbatch_times = []
            min_val_loss = 10000000
            min_val_loss_epoch = -1
            rng_num_tasks = len(tasknames) - 1 if paired_tasks else len(tasknames)
            logging.info('OS Environ: \n {} \n\n'.format(os.environ))
            mlflow.log_param('learning_rate', learning_rate)
            logging.info('Commencing Training ...')
            start = time.time()
            while True:
                batch_start_time = time.time()
                if nli_ctr % 10 == 0:
                    minibatch = nli_iterator.get_parallel_minibatch(nli_mbatch_ctr, batch_size * n_gpus)
                    optimizer.zero_grad()
                    class_logits = model(minibatch, -1, return_hidden=False, paired_trg=None)
                    loss = nli_criterion(class_logits.contiguous().view(-1, class_logits.size(1)), minibatch['labels'].contiguous().view(-1))
                    nli_losses.append(loss.item())
                    loss.backward()
                    torch.nn.utils.clip_grad_norm(model.parameters(), 1.0)
                    optimizer.step()
                    nli_mbatch_ctr += batch_size * n_gpus
                    if nli_mbatch_ctr >= len(nli_iterator.train_lines):
                        nli_mbatch_ctr = 0
                        nli_epoch += 1
                else:
                    task_idx = np.random.randint(low=0, high=rng_num_tasks)
                    minibatch = train_iterator.get_parallel_minibatch(task_idx, task_idxs[task_idx], batch_size * n_gpus, max_len_src, max_len_trg)
                    'Increment pointer into task and if current buffer is\n                    exhausted, fetch new buffer. '
                    task_idxs[task_idx] += batch_size * n_gpus
                    if task_idxs[task_idx] >= train_iterator.buffer_size:
                        train_iterator.fetch_buffer(task_idx)
                        task_idxs[task_idx] = 0
                    if task_idx == skipthought_idx:
                        minibatch_back = train_iterator.get_parallel_minibatch(skipthought_backward_idx, task_idxs[skipthought_backward_idx], batch_size * n_gpus, max_len_src, max_len_trg)
                        task_idxs[skipthought_backward_idx] += batch_size * n_gpus
                        if task_idxs[skipthought_backward_idx] >= train_iterator.buffer_size:
                            train_iterator.fetch_buffer(skipthought_backward_idx)
                            task_idxs[skipthought_backward_idx] = 0
                        optimizer.zero_grad()
                        (decoder_logit, decoder_logit_2) = model(minibatch, task_idx, paired_trg=minibatch_back['input_trg'])
                        loss_f = loss_criterion(decoder_logit.contiguous().view(-1, decoder_logit.size(2)), minibatch['output_trg'].contiguous().view(-1))
                        loss_b = loss_criterion(decoder_logit_2.contiguous().view(-1, decoder_logit_2.size(2)), minibatch_back['output_trg'].contiguous().view(-1))
                        task_losses[task_idx].append(loss_f.data[0])
                        task_losses[skipthought_backward_idx].append(loss_b.data[0])
                        loss = loss_f + loss_b
                    else:
                        optimizer.zero_grad()
                        decoder_logit = model(minibatch, task_idx)
                        loss = loss_criterion(decoder_logit.contiguous().view(-1, decoder_logit.size(2)), minibatch['output_trg'].contiguous().view(-1))
                        task_losses[task_idx].append(loss.item())
                    loss.backward()
                    optimizer.synchronize()
                    torch.nn.utils.clip_grad_norm(model.parameters(), 1.0)
                    optimizer.step()
                end = time.time()
                mbatch_times.append(end - batch_start_time)
                if updates % config['management']['monitor_loss'] == 0 and updates != 0:
                    monitor_epoch += 1
                    for (idx, task) in enumerate(tasknames):
                        logging.info('Seq2Seq Examples Processed : %d %s Loss : %.5f Num %s minibatches : %d' % (updates, task, np.mean(task_losses[idx]), task, len(task_losses[idx])))
                        mlflow.log_metric('validation_loss', np.mean(task_losses[idx]), step=monitor_epoch)
                    logging.info('Round: %d NLI Epoch : %d NLI Examples Processed : %d NLI Loss : %.5f ' % (nli_ctr, nli_epoch, nli_mbatch_ctr, np.mean(nli_losses)))
                    mlflow.log_metric('nli_loss', np.mean(nli_losses), step=nli_epoch)
                    logging.info('Average time per minibatch : %.5f' % np.mean(mbatch_times))
                    mlflow.log_metric('minibatch_avg_duration', np.mean(mbatch_times))
                    task_losses = [[] for _ in tasknames]
                    mbatch_times = []
                    nli_losses = []
                    logging.info('############################')
                    logging.info('##### Evaluating model #####')
                    logging.info('############################')
                    (training_complete, min_val_loss_epoch, min_val_loss, model_state) = evaluate(config=config, train_iterator=train_iterator, model=model, loss_criterion=loss_criterion, monitor_epoch=monitor_epoch, min_val_loss=min_val_loss, min_val_loss_epoch=min_val_loss_epoch, save_dir=save_dir, starting_time=start, model_state=model_state, max_epoch=max_epoch)
                    if training_complete:
                        mlflow.log_metric('min_val_loss', float(min_val_loss))
                        mlflow.log_metric('learning_rate', learning_rate)
                        break
                    logging.info('Evaluating on NLI')
                    evaluate_nli(nli_iterator=nli_iterator, model=model, n_gpus=n_gpus, batch_size=batch_size)
                updates += batch_size * n_gpus
                nli_ctr += 1
                logging.info('Updates: %d' % updates)
    finally:
        os.chdir(owd)



def metaphone(term):
    """returns metaphone code for a given string"""
    code = ''
    i = 0
    term_length = len(term)
    if term_length == 0:
        return code
    term = string.lower(term)
    term = re.sub('[^a-z]', '', term)
    if len(term) == 0:
        return code
    firstChar = term[0]
    str2 = firstChar
    for x in term:
        if x != str2[-1]:
            str2 = str2 + x
    firstChar = str2[0]
    str3 = firstChar
    for x in str2[1:]:
        if re.search('[^aeiou]', x):
            str3 = str3 + x
    term = str3
    term_length = len(term)
    if term_length == 0:
        return code
    if term_length > 1:
        first_chars = term[0:2]
        table = {'ae': 'e', 'gn': 'n', 'kn': 'n', 'pn': 'n', 'wr': 'n', 'wh': 'w'}
        if first_chars in table.keys():
            term = term[2:]
            code = table[first_chars]
            term_length = len(term)
    elif term[0] == 'x':
        term = ''
        code = 's'
        term_length = 0
    st_trans = {'b': 'b', 'c': 'k', 'd': 't', 'g': 'k', 'h': 'h', 'k': 'k', 'p': 'p', 'q': 'k', 's': 's', 't': 't', 'v': 'f', 'w': 'w', 'x': 'ks', 'y': 'y', 'z': 's'}
    i = 0
    while i < term_length:
        add_char = ''
        part_n_2 = ''
        part_n_3 = ''
        part_n_4 = ''
        part_c_2 = ''
        part_c_3 = ''
        if i < term_length - 1:
            part_n_2 = term[i:i + 2]
            if i > 0:
                part_c_2 = term[i - 1:i + 1]
                part_c_3 = term[i - 1:i + 2]
        if i < term_length - 2:
            part_n_3 = term[i:i + 3]
        if i < term_length - 3:
            part_n_4 = term[i:i + 4]
        if term[i] == 'b':
            add_char = st_trans['b']
            if i == term_length - 1:
                if i > 0:
                    if term[i - 1] == 'm':
                        add_char = ''
        elif term[i] == 'c':
            add_char = st_trans['c']
            if part_n_2 == 'ch':
                add_char = 'x'
            elif re.search('c[iey]', part_n_2):
                add_char = 's'
            if part_n_3 == 'cia':
                add_char = 'x'
            if re.search('sc[iey]', part_c_3):
                add_char = ''
        elif term[i] == 'd':
            add_char = st_trans['d']
            if re.search('dg[eyi]', part_n_3):
                add_char = 'j'
        elif term[i] == 'g':
            add_char = st_trans['g']
            if part_n_2 == 'gh':
                if i == term_length - 2:
                    add_char = ''
            elif re.search('gh[aeiouy]', part_n_3):
                add_char = ''
            elif part_n_2 == 'gn':
                add_char = ''
            elif part_n_4 == 'gned':
                add_char = ''
            elif re.search('dg[eyi]', part_c_3):
                add_char = ''
            elif part_n_2 == 'gi':
                if part_c_3 != 'ggi':
                    add_char = 'j'
            elif part_n_2 == 'ge':
                if part_c_3 != 'gge':
                    add_char = 'j'
            elif part_n_2 == 'gy':
                if part_c_3 != 'ggy':
                    add_char = 'j'
            elif part_n_2 == 'gg':
                add_char = ''
        elif term[i] == 'h':
            add_char = st_trans['h']
            if re.search('[aeiouy]h[^aeiouy]', part_c_3):
                add_char = ''
            elif re.search('[csptg]h', part_c_2):
                add_char = ''
        elif term[i] == 'k':
            add_char = st_trans['k']
            if part_c_2 == 'ck':
                add_char = ''
        elif term[i] == 'p':
            add_char = st_trans['p']
            if part_n_2 == 'ph':
                add_char = 'f'
        elif term[i] == 'q':
            add_char = st_trans['q']
        elif term[i] == 's':
            add_char = st_trans['s']
            if part_n_2 == 'sh':
                add_char = 'x'
            if re.search('si[ao]', part_n_3):
                add_char = 'x'
        elif term[i] == 't':
            add_char = st_trans['t']
            if part_n_2 == 'th':
                add_char = '0'
            if re.search('ti[ao]', part_n_3):
                add_char = 'x'
        elif term[i] == 'v':
            add_char = st_trans['v']
        elif term[i] == 'w':
            add_char = st_trans['w']
            if re.search('w[^aeiouy]', part_n_2):
                add_char = ''
        elif term[i] == 'x':
            add_char = st_trans['x']
        elif term[i] == 'y':
            add_char = st_trans['y']
        elif term[i] == 'z':
            add_char = st_trans['z']
        else:
            add_char = term[i]
        code = code + add_char
        i += 1
    return code


def fill_linkedin(peoplelist):
    LinkedinfinderObject = linkedinfinder.Linkedinfinder(showbrowser)
    LinkedinfinderObject.doLogin(linkedin_username, linkedin_password)
    if args.waitafterlogin:
        input('Press Enter to continue after verifying you are logged in...')
    count = 1
    ammount = len(peoplelist)
    for person in peoplelist:
        if args.vv == True or args.debug == True:
            print('LinkedIn Check %i/%i : %s' % (count, ammount, person.full_name))
        else:
            sys.stdout.write('\rLinkedIn Check %i/%i : %s                                ' % (count, ammount, person.full_name))
            sys.stdout.flush()
        count = count + 1
        if person.person_image:
            try:
                target_image = face_recognition.load_image_file(person.person_image)
                target_encoding = face_recognition.face_encodings(target_image)[0]
                profilelist = LinkedinfinderObject.getLinkedinProfiles(person.first_name, person.last_name, linkedin_username, linkedin_password)
                if args.debug == True:
                    print(profilelist)
            except:
                continue
        else:
            continue
        early_break = False
        updatedlist = []
        for (profilelink, profilepic, distance) in profilelist:
            try:
                os.remove('potential_target_image.jpg')
            except:
                pass
            if early_break:
                break
            image_link = profilepic
            if image_link:
                try:
                    urllib.request.urlretrieve(image_link, 'potential_target_image.jpg')
                    potential_target_image = face_recognition.load_image_file('potential_target_image.jpg')
                    try:
                        potential_target_encoding = face_recognition.face_encodings(potential_target_image)[0]
                    except:
                        continue
                    results = face_recognition.face_distance([target_encoding], potential_target_encoding)
                    for result in results:
                        if args.mode == 'fast':
                            if result < threshold:
                                person.linkedin = encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
                                person.linkedinimage = encoding.smart_str(image_link, encoding='ascii', errors='ignore')
                                if args.vv == True:
                                    print('\tMatch found: ' + person.full_name)
                                    print('\tLinkedIn: ' + person.linkedin)
                                early_break = True
                                break
                        elif args.mode == 'accurate':
                            if result < threshold:
                                updatedlist.append([profilelink, image_link, result])
                except Exception as e:
                    print(e)
        if args.mode == 'accurate':
            highestdistance = 1.0
            bestprofilelink = ''
            bestimagelink = ''
            for (profilelink, image_link, distance) in updatedlist:
                if distance < highestdistance:
                    highestdistance = distance
                    bestprofilelink = profilelink
                    bestimagelink = image_link
            if highestdistance < threshold:
                person.linkedin = encoding.smart_str(bestprofilelink, encoding='ascii', errors='ignore')
                person.linkedinimage = encoding.smart_str(bestimagelink, encoding='ascii', errors='ignore')
                if args.vv == True:
                    print('\tMatch found: ' + person.full_name)
                    print('\tLinkedIn: ' + person.linkedin)
    try:
        LinkedinfinderObject.kill()
    except:
        print('Error Killing LinkedIn Selenium instance')
    return peoplelist



def post(self, request, *args, **kwargs):
    """
        called in post method calls.
        It only allows for the 'upload' command
        """
    u_id = str(uuid.uuid4())
    kwargs['u_id'] = u_id
    loginuser = kwargs.get('loginuser', None)
    if kwargs['optionset'] == 'sftp':
        server_object = get_object_or_404(ServerInfor, id=kwargs['start_path'])
        optinon_sets = self.get_optionset(**kwargs)
        optinon_sets['roots'][u_id][0]['alias'] = '{0}-{1}'.format(server_object.name, server_object.ip)
        key_label = '%s::%s' % (server_object.ip, loginuser)
        port = None
        method = None
        key = None
        password = None
        for credential in server_object.credentials.all():
            if credential.username == loginuser:
                port = credential.port
                method = credential.method
                if method == 'password':
                    password = credential.password
                else:
                    password = credential.password
                    key = credential.key
        if method == 'password':
            optinon_sets['roots'][u_id][0]['storageKwArgs'] = {'host': server_object.ip, 'params': {'port': port, 'username': loginuser, 'password': password, 'timeout': 30}, 'root_path': '/', 'interactive': False, 'key_label': key_label}
        else:
            private_key = StringIO(key)
            if 'RSA' in key:
                private_key = paramiko.RSAKey.from_private_key(private_key, password=password)
            elif 'DSA' in key:
                private_key = paramiko.DSSKey.from_private_key(private_key, password=password)
            elif 'EC' in key:
                private_key = paramiko.ECDSAKey.from_private_key(private_key, password=password)
            elif 'OPENSSH' in key:
                private_key = paramiko.Ed25519Key.from_private_key(private_key, password=password)
            optinon_sets['roots'][u_id][0]['storageKwArgs'] = {'host': server_object.ip, 'params': {'port': port, 'username': loginuser, 'pkey': private_key, 'timeout': 30}, 'root_path': '/', 'interactive': False, 'key_label': key_label}
        self.elfinder = ElfinderConnector(optinon_sets, u_id, request.session)
    else:
        optinon_sets = self.get_optionset(**kwargs)
        optinon_sets['roots'][u_id][0]['alias'] = '{0}_tmp_dir'.format(request.user.username)
        optinon_sets['roots'][u_id][0]['path'] = os.path.join(settings.MEDIA_ROOT, request.user.username, 'Download')
        optinon_sets['roots'][u_id][0]['URL'] = '{0}{1}/{2}/'.format(settings.MEDIA_URL, request.user.username, 'Download')
        self.elfinder = ElfinderConnector(optinon_sets, u_id, request.session)
    cmd = self.get_command(request.POST)
    if not cmd in ['upload']:
        self.render_to_response({'error': self.elfinder.error(ElfinderErrorMessages.ERROR_UPLOAD, ElfinderErrorMessages.ERROR_UPLOAD_TOTAL_SIZE)})
    return self.output(cmd, request.POST)


def test_brozzle_site(httpd):
    test_id = 'test_brozzle_site-%s' % datetime.datetime.utcnow().isoformat()
    rr = doublethink.Rethinker('localhost', db='brozzler')
    site = brozzler.Site(rr, {'seed': make_url(httpd, '/site1/'), 'warcprox_meta': {'captures-table-extra-fields': {'test_id': test_id}}})
    page1 = make_url(httpd, '/site1/')
    page2 = make_url(httpd, '/site1/file1.txt')
    robots = make_url(httpd, '/robots.txt')
    try:
        stop_service('brozzler-worker')
        assert site.id is None
        frontier = brozzler.RethinkDbFrontier(rr)
        brozzler.new_site(frontier, site)
        assert site.id is not None
        assert len(list(frontier.site_pages(site.id))) == 1
    finally:
        start_service('brozzler-worker')
    start = time.time()
    while site.status != 'FINISHED' and time.time() - start < 300:
        time.sleep(0.5)
        site.refresh()
    assert site.status == 'FINISHED'
    pages = list(frontier.site_pages(site.id))
    assert len(pages) == 2
    assert {page.url for page in pages} == {make_url(httpd, '/site1/'), make_url(httpd, '/site1/file1.txt')}
    time.sleep(2)
    captures = rr.table('captures').filter({'test_id': test_id}).run()
    captures_by_url = {c['url']: c for c in captures if c['http_method'] != 'HEAD'}
    assert robots in captures_by_url
    assert page1 in captures_by_url
    assert page2 in captures_by_url
    assert 'screenshot:%s' % page1 in captures_by_url
    assert 'thumbnail:%s' % page1 in captures_by_url
    t14 = captures_by_url[page2]['timestamp'].strftime('%Y%m%d%H%M%S')
    wb_url = 'http://localhost:8880/brozzler/%s/%s' % (t14, page2)
    expected_payload = open(os.path.join(os.path.dirname(__file__), 'htdocs', 'site1', 'file1.txt'), 'rb').read()
    assert requests.get(wb_url).content == expected_payload
    url = 'screenshot:%s' % page1
    t14 = captures_by_url[url]['timestamp'].strftime('%Y%m%d%H%M%S')
    wb_url = 'http://localhost:8880/brozzler/%s/%s' % (t14, url)
    response = requests.get(wb_url)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/jpeg'
    url = 'thumbnail:%s' % page1
    t14 = captures_by_url[url]['timestamp'].strftime('%Y%m%d%H%M%S')
    wb_url = 'http://localhost:8880/brozzler/%s/%s' % (t14, url)
    response = requests.get(wb_url)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/jpeg'



def test_brozzle_site(httpd):
    test_id = 'test_brozzle_site-%s' % datetime.datetime.utcnow().isoformat()
    rr = doublethink.Rethinker('localhost', db='brozzler')
    site = brozzler.Site(rr, {'seed': make_url(httpd, '/site1/'), 'warcprox_meta': {'captures-table-extra-fields': {'test_id': test_id}}})
    page1 = make_url(httpd, '/site1/')
    page2 = make_url(httpd, '/site1/file1.txt')
    robots = make_url(httpd, '/robots.txt')
    try:
        stop_service('brozzler-worker')
        assert site.id is None
        frontier = brozzler.RethinkDbFrontier(rr)
        brozzler.new_site(frontier, site)
        assert site.id is not None
        assert len(list(frontier.site_pages(site.id))) == 1
    finally:
        start_service('brozzler-worker')
    start = time.time()
    while site.status != 'FINISHED' and time.time() - start < 300:
        time.sleep(0.5)
        site.refresh()
    assert site.status == 'FINISHED'
    pages = list(frontier.site_pages(site.id))
    assert len(pages) == 2
    assert {page.url for page in pages} == {make_url(httpd, '/site1/'), make_url(httpd, '/site1/file1.txt')}
    time.sleep(2)
    captures = rr.table('captures').filter({'test_id': test_id}).run()
    captures_by_url = {c['url']: c for c in captures if c['http_method'] != 'HEAD'}
    assert robots in captures_by_url
    assert page1 in captures_by_url
    assert page2 in captures_by_url
    assert 'screenshot:%s' % page1 in captures_by_url
    assert 'thumbnail:%s' % page1 in captures_by_url
    t14 = captures_by_url[page2]['timestamp'].strftime('%Y%m%d%H%M%S')
    wb_url = 'http://localhost:8880/brozzler/%s/%s' % (t14, page2)
    expected_payload = open(os.path.join(os.path.dirname(__file__), 'htdocs', 'site1', 'file1.txt'), 'rb').read()
    assert requests.get(wb_url).content == expected_payload
    url = 'screenshot:%s' % page1
    t14 = captures_by_url[url]['timestamp'].strftime('%Y%m%d%H%M%S')
    wb_url = 'http://localhost:8880/brozzler/%s/%s' % (t14, url)
    response = requests.get(wb_url)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/jpeg'
    url = 'thumbnail:%s' % page1
    t14 = captures_by_url[url]['timestamp'].strftime('%Y%m%d%H%M%S')
    wb_url = 'http://localhost:8880/brozzler/%s/%s' % (t14, url)
    response = requests.get(wb_url)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/jpeg'


def main():
    import sys
    import getopt
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'td')
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print('usage: quopri [-t | -d] [file] ...')
        print('-t: quote tabs')
        print('-d: decode; default encode')
        sys.exit(2)
    deco = 0
    tabs = 0
    for (o, a) in opts:
        if o == '-t':
            tabs = 1
        if o == '-d':
            deco = 1
    if tabs and deco:
        sys.stdout = sys.stderr
        print('-t and -d are mutually exclusive')
        sys.exit(2)
    if not args:
        args = ['-']
    sts = 0
    for file in args:
        if file == '-':
            fp = sys.stdin.buffer
        else:
            try:
                fp = open(file, 'rb')
            except IOError as msg:
                sys.stderr.write("%s: can't open (%s)\n" % (file, msg))
                sts = 1
                continue
        try:
            if deco:
                decode(fp, sys.stdout.buffer)
            else:
                encode(fp, sys.stdout.buffer, tabs)
        finally:
            if file != '-':
                fp.close()
    if sts:
        sys.exit(sts)


def svg_nd(chunks, size=200):
    if len(chunks) % 3 == 1:
        chunks = ((1,),) + chunks
    shape = tuple(map(sum, chunks))
    sizes = draw_sizes(shape, size=size)
    chunks2 = chunks
    sizes2 = sizes
    out = []
    left = 0
    total_height = 0
    while chunks2:
        n = len(chunks2) % 3 or 3
        o = svg(chunks2[:n], sizes=sizes2[:n], offset=(left, 0))
        chunks2 = chunks2[n:]
        sizes2 = sizes2[n:]
        lines = o.split('\n')
        header = lines[0]
        height = float(re.search('height="(\\d*\\.?\\d*)"', header).groups()[0])
        total_height = max(total_height, height)
        width = float(re.search('width="(\\d*\\.?\\d*)"', header).groups()[0])
        left += width + 10
        o = '\n'.join(lines[1:-1])
        out.append(o)
    header = '<svg width="%d" height="%d" style="stroke:rgb(0,0,0);stroke-width:1" >\n' % (left, total_height)
    footer = '\n</svg>'
    return header + '\n\n'.join(out) + footer


def main(source_files, outpath, keywords=None):
    global default_keywords

    class Options:
        GNU = 1
        SOLARIS = 2
        extractall = 0
        escape = 0
        keywords = []
        outfile = 'messages.pot'
        writelocations = 1
        locationstyle = GNU
        verbose = 0
        width = 78
        excludefilename = ''
        docstrings = 0
        nodocstrings = {}
    options = Options()
    options.outfile = outpath
    if keywords:
        options.keywords = keywords
    make_escapes(options.escape)
    options.keywords.extend(default_keywords)
    if options.excludefilename:
        try:
            fp = open(options.excludefilename, encoding='utf-8')
            options.toexclude = fp.readlines()
            fp.close()
        except IOError:
            print("Can't read --exclude-file: %s" % options.excludefilename, file=sys.stderr)
            sys.exit(1)
    else:
        options.toexclude = []
    eater = TokenEater(options)
    for filename in source_files:
        if options.verbose:
            print('Working on %s' % filename)
        fp = open(filename, encoding='utf-8')
        closep = 1
        try:
            eater.set_filename(filename)
            try:
                tokens = tokenize.generate_tokens(fp.readline)
                for _token in tokens:
                    eater(*_token)
            except tokenize.TokenError as e:
                print('%s: %s, line %d, column %d' % (e.args[0], filename, e.args[1][0], e.args[1][1]), file=sys.stderr)
        finally:
            if closep:
                fp.close()
    fp = open(options.outfile, 'w', encoding='utf-8')
    closep = 1
    try:
        eater.write(fp)
    finally:
        if closep:
            fp.close()



def hexdiff(x, y):
    """Show differences between 2 binary strings"""
    x = any2b(x)[::-1]
    y = any2b(y)[::-1]
    SUBST = 1
    INSERT = 1
    d = {}
    d[-1, -1] = (0, (-1, -1))
    for j in range(len(y)):
        d[-1, j] = (d[-1, j - 1][0] + INSERT, (-1, j - 1))
    for i in range(len(x)):
        d[i, -1] = (d[i - 1, -1][0] + INSERT, (i - 1, -1))
    for j in range(len(y)):
        for i in range(len(x)):
            d[i, j] = min((d[i - 1, j - 1][0] + SUBST * (x[i] != y[j]), (i - 1, j - 1)), (d[i - 1, j][0] + INSERT, (i - 1, j)), (d[i, j - 1][0] + INSERT, (i, j - 1)))
    backtrackx = []
    backtracky = []
    i = len(x) - 1
    j = len(y) - 1
    while not i == j == -1:
        (i2, j2) = d[i, j][1]
        backtrackx.append(x[i2 + 1:i + 1])
        backtracky.append(y[j2 + 1:j + 1])
        (i, j) = (i2, j2)
    x = y = i = 0
    colorize = {0: lambda x: x, -1: conf.color_theme.left, 1: conf.color_theme.right}
    dox = 1
    doy = 0
    l = len(backtrackx)
    while i < l:
        separate = 0
        linex = backtrackx[i:i + 16]
        liney = backtracky[i:i + 16]
        xx = sum((len(k) for k in linex))
        yy = sum((len(k) for k in liney))
        if dox and (not xx):
            dox = 0
            doy = 1
        if dox and linex == liney:
            doy = 1
        if dox:
            xd = y
            j = 0
            while not linex[j]:
                j += 1
                xd -= 1
            print(colorize[doy - dox]('%04x' % xd), end=' ')
            x += xx
            line = linex
        else:
            print('    ', end=' ')
        if doy:
            yd = y
            j = 0
            while not liney[j]:
                j += 1
                yd -= 1
            print(colorize[doy - dox]('%04x' % yd), end=' ')
            y += yy
            line = liney
        else:
            print('    ', end=' ')
        print(' ', end=' ')
        cl = ''
        for j in range(16):
            if i + j < l:
                if line[j]:
                    col = colorize[(linex[j] != liney[j]) * (doy - dox)]
                    print(col('%02X' % line[j][0]), end=' ')
                    if linex[j] == liney[j]:
                        cl += sane_color(line[j])
                    else:
                        cl += col(sane(line[j]))
                else:
                    print('  ', end=' ')
                    cl += ' '
            else:
                print('  ', end=' ')
            if j == 7:
                print('', end=' ')
        print(' ', cl)
        if doy or not yy:
            doy = 0
            dox = 1
            i += 16
        elif yy:
            dox = 0
            doy = 1
        else:
            i += 16


def main():
    (options, leftovers) = parse_commandline()
    cli.setupLogging('virt-manager', options.debug, False, False)
    log.debug('virt-manager version: %s', BuildConfig.version)
    log.debug('virtManager import: %s', os.path.dirname(__file__))
    if BuildConfig.running_from_srcdir:
        _setup_gsettings_path(BuildConfig.gsettings_dir)
    if options.trace_libvirt:
        log.debug('Libvirt tracing requested')
        from .lib import module_trace
        import libvirt
        module_trace.wrap_module(libvirt, mainloop=options.trace_libvirt == 'mainloop', regex=None)
    CLITestOptions = CLITestOptionsClass(options.test_options)
    os.environ['GSETTINGS_SCHEMA_DIR'] = BuildConfig.gsettings_dir
    do_drop_stdio = False
    if not options.no_fork and (not options.debug):
        drop_tty()
        do_drop_stdio = True
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
    leftovers = _import_gtk(leftovers)
    Gtk = globals()['Gtk']
    if do_drop_stdio:
        drop_stdio()
    if leftovers:
        raise RuntimeError("Unhandled command line options '%s'" % leftovers)
    log.debug('PyGObject version: %d.%d.%d', gi.version_info[0], gi.version_info[1], gi.version_info[2])
    log.debug('GTK version: %d.%d.%d', Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version())
    from . import config
    config.vmmConfig.get_instance(BuildConfig, CLITestOptions)
    icon_theme = Gtk.IconTheme.get_default()
    icon_theme.prepend_search_path(BuildConfig.icon_dir)
    from .engine import vmmEngine
    Gtk.Window.set_default_icon_name('virt-manager')
    show_window = None
    domain = None
    if options.show_domain_creator:
        show_window = vmmEngine.CLI_SHOW_DOMAIN_CREATOR
    elif options.show_host_summary:
        show_window = vmmEngine.CLI_SHOW_HOST_SUMMARY
    elif options.show_domain_editor:
        show_window = vmmEngine.CLI_SHOW_DOMAIN_EDITOR
        domain = options.show_domain_editor
    elif options.show_domain_performance:
        show_window = vmmEngine.CLI_SHOW_DOMAIN_PERFORMANCE
        domain = options.show_domain_performance
    elif options.show_domain_console:
        show_window = vmmEngine.CLI_SHOW_DOMAIN_CONSOLE
        domain = options.show_domain_console
    elif options.show_domain_delete:
        show_window = vmmEngine.CLI_SHOW_DOMAIN_DELETE
        domain = options.show_domain_delete
    if show_window and options.uri is None:
        raise RuntimeError("can't use --show-* options without --connect")
    skip_autostart = False
    if show_window:
        skip_autostart = True
    LibvirtGLib.init(None)
    LibvirtGLib.event_register()
    engine = vmmEngine.get_instance()
    from gi.repository import GLib

    def _sigint_handler(user_data):
        ignore = user_data
        log.debug('Received KeyboardInterrupt. Exiting application.')
        engine.exit_app()
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, _sigint_handler, None)
    engine.start(options.uri, show_window, domain, skip_autostart)



def create_scanner_issues(self, view, callbacks, helpers, vuln_parameters, request_response):
    issues = self.issues
    json = self.json
    for vuln_parameter in vuln_parameters:
        issue_name = vuln_parameter['vuln_name']
        vuln_param = vuln_parameter['vuln_param']
        param_name = vuln_parameter['param']
        param_value = vuln_parameter['value']
        url = helpers.analyzeRequest(request_response).getUrl()
        url = urlparse.urlsplit(str(url))
        hostname = url.hostname
        path = url.path
        url = url.scheme + '://' + url.hostname + url.path
        http_service = request_response.getHttpService()
        http_messages = [callbacks.applyMarkers(request_response, None, None)]
        detail = json['issues'][issue_name]['detail']
        severity = 'Medium'
        scanner_issue = ScannerIssue(url, issue_name, param_name, vuln_param, param_value, hostname, path, http_service, http_messages, detail, severity, request_response)
        is_scanner_issue_dupe = self.check_duplicate_issue(scanner_issue)
        if is_scanner_issue_dupe:
            continue
        else:
            self.set_scanner_issues(scanner_issue)
        issue_count = self.set_issue_count(issue_name, vuln_param)
        total_count = self.total_count[issue_name]
        view.set_scanner_count(issue_name, vuln_param, issue_count, total_count)
        view.scanner_table_models.set_scanner_table_model(scanner_issue, issue_name, param_name, vuln_param)
def write(filename, mesh, float_fmt: str='.3f', stroke_width: str | None=None, image_width: int | float | None=100, fill: str='#c8c5bd', stroke: str='#000080'):
    if mesh.points.shape[1] == 3 and (not np.allclose(mesh.points[:, 2], 0.0, rtol=0.0, atol=1e-14)):
        raise WriteError(f'SVG can only handle flat 2D meshes (shape: {mesh.points.shape})')
    pts = mesh.points[:, :2].copy()
    min_x = np.min(pts[:, 0]) if len(pts) > 0 else 0.0
    max_x = np.max(pts[:, 0]) if len(pts) > 0 else 0.0
    min_y = np.min(pts[:, 1]) if len(pts) > 0 else 0.0
    max_y = np.max(pts[:, 1]) if len(pts) > 0 else 0.0
    pts[:, 1] = max_y + min_y - pts[:, 1]
    width = max_x - min_x
    height = max_y - min_y
    if image_width is not None and width != 0:
        scaling_factor = image_width / width
        min_x *= scaling_factor
        min_y *= scaling_factor
        width *= scaling_factor
        height *= scaling_factor
        pts *= scaling_factor
    if stroke_width is None:
        stroke_width = str(width / 100)
    fmt = ' '.join(4 * [f'{{:{float_fmt}}}'])
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', version='1.1', viewBox=fmt.format(min_x, min_y, width, height))
    style = ET.SubElement(svg, 'style')
    opts = [f'fill: {fill}', f'stroke: {stroke}', f'stroke-width: {stroke_width}', 'stroke-linejoin:bevel']
    style.text = 'path {' + '; '.join(opts) + '}'
    for cell_block in mesh.cells:
        if cell_block.type not in ['line', 'triangle', 'quad']:
            continue
        if cell_block.type == 'line':
            fmt = f'M {{:{float_fmt}}} {{:{float_fmt}}}' + f'L {{:{float_fmt}}} {{:{float_fmt}}}'
        elif cell_block.type == 'triangle':
            fmt = f'M {{:{float_fmt}}} {{:{float_fmt}}}' + f'L {{:{float_fmt}}} {{:{float_fmt}}}' + f'L {{:{float_fmt}}} {{:{float_fmt}}}' + 'Z'
        elif cell_block.type == 'quad':
            fmt = f'M {{:{float_fmt}}} {{:{float_fmt}}}' + f'L {{:{float_fmt}}} {{:{float_fmt}}}' + f'L {{:{float_fmt}}} {{:{float_fmt}}}' + f'L {{:{float_fmt}}} {{:{float_fmt}}}' + 'Z'
        for cell in cell_block.data:
            ET.SubElement(svg, 'path', d=fmt.format(*pts[cell].flatten()))
    tree = ET.ElementTree(svg)
    tree.write(filename)

def select_pars(qa_dct, docs_list, word_freqs, n_sents=100, n_context=3):
    question = qa_dct['title'][0]
    split_docs = [sentence_split(doc['text'][0], max_len=64) for doc in docs_list]
    q_ti_dct = tf_idf_vec(question, word_freqs['title'][0], word_freqs['title'][1])
    split_docs_pre = [
        (i, j, sen, tf_idf_vec(sen, word_freqs['doc'][0], word_freqs['doc'][1]))
        for i, doc in enumerate(split_docs)
        for j, sen in enumerate(doc)
    ]
    split_docs_sc = [
        (i, j, tf_idf_dist(q_ti_dct, dct))
        for k, (i, j, sen, dct) in enumerate(split_docs_pre)
        if len(sen.split()) >= 4 and sen not in [x[2] for x in split_docs_pre[:k]]
    ]
    split_docs_sort = sorted(split_docs_sc, key=lambda x: x[-1], reverse=True)[:n_sents]
    select_ids = sorted([(i, j) for i, j, _ in split_docs_sort])
    par_ids = []
    this_par = []
    last_seen = (-1, -1)
    for i, j in select_ids:
        if i > last_seen[0]:
            par_ids += [this_par]
            this_par = []
            for k in range(-n_context, n_context + 1):
                if j + k >= 0 and j + k < len(split_docs[i]):
                    this_par += [(i, j + k)]
                    last_seen = (i, j + k)
        else:
            if j - n_context > last_seen[1] + 1:
                par_ids += [this_par]
                this_par = []
            for k in range(-n_context, n_context + 1):
                if j + k > last_seen[1] and j + k >= 0 and j + k < len(split_docs[i]):
                    this_par += [(i, j + k)]
                    last_seen = (i, j + k)
    par_ids = par_ids[1:] + [this_par]
    extract_doc = ' <P> '.join(
        [''] + [' '.join([split_docs[i][j] for i, j in par]) for par in par_ids]
    ).strip()
    return extract_doc

    def _file_request_download(self, msg, i):

        log.add_transfer("Received file upload request %(request)s for file %(filename)s from user %(user)s", {
            "request": msg.req,
            "filename": i.filename,
            "user": i.user
        })

        incompletedir = self.config.sections["transfers"]["incompletedir"]
        needupdate = True

        if i.conn is None and i.size is not None:
            i.conn = msg.conn
            i.req = None

            if i in self.transfer_request_times:
                del self.transfer_request_times[i]

            if not incompletedir:
                if i.path:
                    incompletedir = i.path
                else:
                    incompletedir = self.get_default_download_folder(i.user)

            try:
                if not os.access(incompletedir, os.F_OK):
                    os.makedirs(incompletedir)
                if not os.access(incompletedir, os.R_OK | os.W_OK | os.X_OK):
                    raise OSError("Download directory %s Permissions error.\nDir Permissions: %s" %
                                  (incompletedir, oct(os.stat(incompletedir)[stat.ST_MODE] & 0o777)))

            except OSError as error:
                log.add(_("OS error: %s"), error)
                self.download_folder_error(i, error)

            else:
                file_handle = None
                try:
                    from hashlib import md5
                    md5sum = md5()
                    md5sum.update((i.filename + i.user).encode('utf-8'))

                    base_name = clean_file(i.filename.replace('/', '\\').split('\\')[-1])
                    incomplete_name = os.path.join(incompletedir, "INCOMPLETE" + md5sum.hexdigest() + base_name)
                    file_handle = open(incomplete_name, 'ab+')

                    if self.config.sections["transfers"]["lock"]:
                        try:
                            import fcntl
                            try:
                                fcntl.lockf(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                            except IOError as error:
                                log.add(_("Can't get an exclusive lock on file - I/O error: %s"), error)
                        except ImportError:
                            pass

                    file_handle.seek(0, 2)
                    offset = file_handle.tell()

                except IOError as error:
                    log.add(_("Download I/O error: %s"), error)

                    self.abort_transfer(i)
                    i.status = "Local file error"

                else:
                    i.file = file_handle
                    i.lastbytes = offset
                    i.place = 0

                    self.core.statistics.append_stat_value("started_downloads", 1)
                    self.core.pluginhandler.download_started_notification(i.user, i.filename, incomplete_name)

                    if i.size > offset:
                        i.status = "Transferring"
                        i.legacy_attempt = False
                        self.queue.append(slskmessages.DownloadFile(i.conn, file_handle))
                        self.queue.append(slskmessages.FileOffset(i.conn, i.size, offset))

                        log.add_download(
                            _("Download started: user %(user)s, file %(file)s"), {
                                "user": i.user,
                                "file": "%s" % file_handle.name
                            }
                        )
                    else:
                        self.download_finished(file_handle, i)
                        needupdate = False

            if self.downloadsview:
                self.downloadsview.new_transfer_notification()

                if needupdate:
                    self.downloadsview.update(i)

        else:
            log.add_transfer("Download error formally known as 'Unknown file request': %(req)s (%(user)s: %(file)s)", {
                'req': str(vars(msg)),
                'user': i.user,
                'file': i.filename
            })

            self.queue.append(slskmessages.ConnClose(msg.conn))

def select_pars(qa_dct, docs_list, word_freqs, n_sents=100, n_context=3):
    question = qa_dct['title'][0]
    split_docs = [sentence_split(doc['text'][0], max_len=64) for doc in docs_list]
    q_ti_dct = tf_idf_vec(question, word_freqs['title'][0], word_freqs['title'][1])
    split_docs_pre = [(i, j, sen, tf_idf_vec(sen, word_freqs['doc'][0], word_freqs['doc'][1])) for (i, doc) in enumerate(split_docs) for (j, sen) in enumerate(doc)]
    split_docs_sc = [(i, j, tf_idf_dist(q_ti_dct, dct)) for (k, (i, j, sen, dct)) in enumerate(split_docs_pre) if len(sen.split()) >= 4 and sen not in [x[2] for x in split_docs_pre[:k]]]
    split_docs_sort = sorted(split_docs_sc, key=lambda x: x[-1], reverse=True)[:n_sents]
    select_ids = sorted([(i, j) for (i, j, _) in split_docs_sort])
    par_ids = []
    this_par = []
    last_seen = (-1, -1)
    for (i, j) in select_ids:
        if i > last_seen[0]:
            par_ids += [this_par]
            this_par = []
            for k in range(-n_context, n_context + 1):
                if j + k >= 0 and j + k < len(split_docs[i]):
                    this_par += [(i, j + k)]
                    last_seen = (i, j + k)
        else:
            if j - n_context > last_seen[1] + 1:
                par_ids += [this_par]
                this_par = []
            for k in range(-n_context, n_context + 1):
                if j + k > last_seen[1] and j + k >= 0 and (j + k < len(split_docs[i])):
                    this_par += [(i, j + k)]
                    last_seen = (i, j + k)
    par_ids = par_ids[1:] + [this_par]
    extract_doc = ' <P> '.join([''] + [' '.join([split_docs[i][j] for (i, j) in par]) for par in par_ids]).strip()
    return extract_doc


def extract(self, **kwargs):
    for s in self.streams:
        self.streams[s]['size'] = urls_size(self.streams[s]['src'])
    master_m3u8s = []
    for m in self.master_m3u8:
        master_m3u8s.append(self.master_m3u8[m]['url'])
    master_content = None
    master_url = None
    for master_u in master_m3u8s:
        try:
            master_content = get_content(master_u).split('\n')
        except urllib.error.URLError:
            continue
        else:
            master_url = master_u
    if master_content is None:
        return
    lines = []
    for line in master_content:
        if len(line.strip()) > 0:
            lines.append(line.strip())
    pos = 0
    while pos < len(lines):
        if lines[pos].startswith('#EXT-X-STREAM-INF'):
            patt = 'RESOLUTION=(\\d+)x(\\d+)'
            hit = re.search(patt, lines[pos])
            if hit is None:
                continue
            width = hit.group(1)
            height = hit.group(2)
            if height in ('2160', '1440'):
                m3u8_url = urllib.parse.urljoin(master_url, lines[pos + 1])
                meta = dict(m3u8_url=m3u8_url, container='m3u8')
                if height == '1440':
                    meta['video_profile'] = '2560x1440'
                else:
                    meta['video_profile'] = '3840x2160'
                meta['size'] = 0
                meta['src'] = general_m3u8_extractor(m3u8_url)
                self.streams[height + 'p'] = meta
            pos += 2
        else:
            pos += 1
    self.streams_sorted = []
    for stream_type in self.stream_types:
        if stream_type['id'] in self.streams:
            item = [('id', stream_type['id'])] + list(self.streams[stream_type['id']].items())
            self.streams_sorted.append(dict(item))