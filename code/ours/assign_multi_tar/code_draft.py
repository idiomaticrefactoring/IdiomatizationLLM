(self.fc0, self.fc1, self.vel_fc0, self.vel_fc1, scope_name) = \
(layers.fc(size=hid0_size, act='tanh', param_attr=ParamAttr(name='{}/h0/W'.format(scope_name)),
bias_attr=ParamAttr(name='{}/h0/b'.format(scope_name))),
layers.fc(size=hid1_size, act='tanh', param_attr=ParamAttr(name='{}/h1/W'.format(scope_name)),
bias_attr=ParamAttr(name='{}/h1/b'.format(scope_name))),
layers.fc(size=vel_hid0_size, act='tanh',
param_attr=ParamAttr(name='{}/vel_h0/W'.format(scope_name)),
bias_attr=ParamAttr(name='{}/vel_h0/b'.format(scope_name))),
layers.fc(size=hid0_size0, act='tanh',
param_attr=ParamAttr(name=hid0_size1),
bias_attr=ParamAttr(name=hid0_size2)), hid0_size3)



def train(self, train_dataset, output_dir, show_running_loss=True, eval_data=None, additional_eval_passages=None, verbose=True, **kwargs):
    """
        Trains the model on train_dataset.

        Utility function to be used by the train_model() method. Not intended to be used directly.
        """
    context_model = self.context_encoder
    query_model = self.query_encoder
    args = self.args
    tb_writer = SummaryWriter(logdir=args.tensorboard_dir)
    train_sampler = RandomSampler(train_dataset)
    train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=args.train_batch_size, num_workers=self.args.dataloader_num_workers)
    if args.max_steps > 0:
        t_total = args.max_steps
        args.num_train_epochs = args.max_steps // (len(train_dataloader) // args.gradient_accumulation_steps) + 1
    else:
        t_total = len(train_dataloader) // args.gradient_accumulation_steps * args.num_train_epochs
    optimizer_grouped_parameters = self.get_optimizer_parameters(context_model, query_model, args)
    warmup_steps = math.ceil(t_total * args.warmup_ratio)
    args.warmup_steps = warmup_steps if args.warmup_steps == 0 else args.warmup_steps
    if args.optimizer == 'AdamW':
        optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adam_epsilon, betas=args.adam_betas)
    elif args.optimizer == 'Adafactor':
        optimizer = Adafactor(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adafactor_eps, clip_threshold=args.adafactor_clip_threshold, decay_rate=args.adafactor_decay_rate, beta1=args.adafactor_beta1, weight_decay=args.weight_decay, scale_parameter=args.adafactor_scale_parameter, relative_step=args.adafactor_relative_step, warmup_init=args.adafactor_warmup_init)
    else:
        raise ValueError("{} is not a valid optimizer class. Please use one of ('AdamW', 'Adafactor') instead.".format(args.optimizer))
    scheduler = self.get_scheduler(optimizer, args, t_total)
    criterion = torch.nn.NLLLoss(reduction='mean')
    if args.model_name and os.path.isfile(os.path.join(args.model_name, 'optimizer.pt')) and os.path.isfile(os.path.join(args.model_name, 'scheduler.pt')):
        optimizer.load_state_dict(torch.load(os.path.join(args.model_name, 'optimizer.pt')))
        scheduler.load_state_dict(torch.load(os.path.join(args.model_name, 'scheduler.pt')))
    if args.n_gpu > 1:
        context_model = torch.nn.DataParallel(context_model)
        query_model = torch.nn.DataParallel(query_model)
    logger.info(' Training started')
    global_step = 0
    training_progress_scores = None
    (tr_loss, logging_loss) = (0.0, 0.0)
    context_model.zero_grad()
    query_model.zero_grad()
    train_iterator = trange(int(args.num_train_epochs), desc='Epoch', disable=args.silent, mininterval=0)
    epoch_number = 0
    best_eval_metric = None
    early_stopping_counter = 0
    steps_trained_in_current_epoch = 0
    epochs_trained = 0
    if args.model_name and os.path.exists(args.model_name):
        try:
            checkpoint_suffix = args.model_name.split('/')[-1].split('-')
            if len(checkpoint_suffix) > 2:
                checkpoint_suffix = checkpoint_suffix[1]
            else:
                checkpoint_suffix = checkpoint_suffix[-1]
            global_step = int(checkpoint_suffix)
            epochs_trained = global_step // (len(train_dataloader) // args.gradient_accumulation_steps)
            steps_trained_in_current_epoch = global_step % (len(train_dataloader) // args.gradient_accumulation_steps)
            logger.info('   Continuing training from checkpoint, will skip to saved global_step')
            logger.info('   Continuing training from epoch %d', epochs_trained)
            logger.info('   Continuing training from global step %d', global_step)
            logger.info('   Will skip the first %d steps in the current epoch', steps_trained_in_current_epoch)
        except ValueError:
            logger.info('   Starting fine-tuning.')
    if args.evaluate_during_training:
        training_progress_scores = self._create_training_progress_scores(**kwargs)
    if args.wandb_project:
        wandb.init(project=args.wandb_project, config={**asdict(args)}, **args.wandb_kwargs)
        wandb.run._label(repo='simpletransformers')
        wandb.watch(context_model)
        wandb.watch(query_model)
    if args.fp16:
        from torch.cuda import amp
        scaler = amp.GradScaler()
    for current_epoch in train_iterator:
        if args.train_context_encoder:
            context_model.train()
        else:
            context_model.eval()
        if args.train_query_encoder:
            query_model.train()
        else:
            query_model.eval()
        if epochs_trained > 0:
            epochs_trained -= 1
            continue
        train_iterator.set_description(f'Epoch {epoch_number + 1} of {args.num_train_epochs}')
        batch_iterator = tqdm(train_dataloader, desc=f'Running Epoch {epoch_number} of {args.num_train_epochs}', disable=args.silent, mininterval=0)
        for (step, batch) in enumerate(batch_iterator):
            if steps_trained_in_current_epoch > 0:
                steps_trained_in_current_epoch -= 1
                continue
            (context_inputs, query_inputs, labels) = self._get_inputs_dict(batch)
            if args.fp16:
                with amp.autocast():
                    (loss, *_, correct_count) = self._calculate_loss(context_model, query_model, context_inputs, query_inputs, labels, criterion)
            else:
                (loss, *_, correct_count) = self._calculate_loss(context_model, query_model, context_inputs, query_inputs, labels, criterion)
            if args.n_gpu > 1:
                loss = loss.mean()
            current_loss = loss.item()
            if show_running_loss:
                batch_iterator.set_description(f'Epochs {epoch_number}/{args.num_train_epochs}. Running Loss: {current_loss:9.4f} Correct count: {correct_count}')
            if args.gradient_accumulation_steps > 1:
                loss = loss / args.gradient_accumulation_steps
            if args.fp16:
                scaler.scale(loss).backward()
            else:
                loss.backward()
            tr_loss += loss.item()
            if (step + 1) % args.gradient_accumulation_steps == 0:
                if args.fp16:
                    scaler.unscale_(optimizer)
                if args.optimizer == 'AdamW':
                    torch.nn.utils.clip_grad_norm_(context_model.parameters(), args.max_grad_norm)
                    torch.nn.utils.clip_grad_norm_(query_model.parameters(), args.max_grad_norm)
                if args.fp16:
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    optimizer.step()
                scheduler.step()
                context_model.zero_grad()
                query_model.zero_grad()
                global_step += 1
                if args.logging_steps > 0 and global_step % args.logging_steps == 0:
                    tb_writer.add_scalar('lr', scheduler.get_last_lr()[0], global_step)
                    tb_writer.add_scalar('loss', (tr_loss - logging_loss) / args.logging_steps, global_step)
                    logging_loss = tr_loss
                    if args.wandb_project or self.is_sweeping:
                        wandb.log({'Training loss': current_loss, 'lr': scheduler.get_last_lr()[0], 'global_step': global_step})
                if args.save_steps > 0 and global_step % args.save_steps == 0:
                    output_dir_current = os.path.join(output_dir, 'checkpoint-{}'.format(global_step))
                    self.save_model(output_dir_current, optimizer, scheduler, context_model=context_model, query_model=query_model)
                if args.evaluate_during_training and (args.evaluate_during_training_steps > 0 and global_step % args.evaluate_during_training_steps == 0):
                    (results, *_) = self.eval_model(eval_data, additional_passages=additional_eval_passages, verbose=verbose and args.evaluate_during_training_verbose, silent=args.evaluate_during_training_silent, **kwargs)
                    for (key, value) in results.items():
                        try:
                            tb_writer.add_scalar('eval_{}'.format(key), value, global_step)
                        except (NotImplementedError, AssertionError):
                            pass
                    output_dir_current = os.path.join(output_dir, 'checkpoint-{}'.format(global_step))
                    if args.save_eval_checkpoints:
                        self.save_model(output_dir_current, optimizer, scheduler, context_model=context_model, query_model=query_model, results=results)
                    training_progress_scores['global_step'].append(global_step)
                    training_progress_scores['train_loss'].append(current_loss)
                    for key in results:
                        training_progress_scores[key].append(results[key])
                    report = pd.DataFrame(training_progress_scores)
                    report.to_csv(os.path.join(args.output_dir, 'training_progress_scores.csv'), index=False)
                    if args.wandb_project or self.is_sweeping:
                        wandb.log(self._get_last_metrics(training_progress_scores))
                    if not best_eval_metric:
                        best_eval_metric = results[args.early_stopping_metric]
                        if args.save_best_model:
                            self.save_model(args.best_model_dir, optimizer, scheduler, context_model=context_model, query_model=query_model, results=results)
                    if best_eval_metric and args.early_stopping_metric_minimize:
                        if results[args.early_stopping_metric] - best_eval_metric < args.early_stopping_delta:
                            best_eval_metric = results[args.early_stopping_metric]
                            if args.save_best_model:
                                self.save_model(args.best_model_dir, optimizer, scheduler, context_model=context_model, query_model=query_model, results=results)
                            early_stopping_counter = 0
                        elif args.use_early_stopping:
                            if early_stopping_counter < args.early_stopping_patience:
                                early_stopping_counter += 1
                                if verbose:
                                    logger.info(f' No improvement in {args.early_stopping_metric}')
                                    logger.info(f' Current step: {early_stopping_counter}')
                                    logger.info(f' Early stopping patience: {args.early_stopping_patience}')
                            else:
                                if verbose:
                                    logger.info(f' Patience of {args.early_stopping_patience} steps reached')
                                    logger.info(' Training terminated.')
                                    train_iterator.close()
                                return (global_step, tr_loss / global_step if not self.args.evaluate_during_training else training_progress_scores)
                    elif results[args.early_stopping_metric] - best_eval_metric > args.early_stopping_delta:
                        best_eval_metric = results[args.early_stopping_metric]
                        if args.save_best_model:
                            self.save_model(args.best_model_dir, optimizer, scheduler, context_model=context_model, query_model=query_model, results=results)
                        early_stopping_counter = 0
                    elif args.use_early_stopping:
                        if early_stopping_counter < args.early_stopping_patience:
                            early_stopping_counter += 1
                            if verbose:
                                logger.info(f' No improvement in {args.early_stopping_metric}')
                                logger.info(f' Current step: {early_stopping_counter}')
                                logger.info(f' Early stopping patience: {args.early_stopping_patience}')
                        else:
                            if verbose:
                                logger.info(f' Patience of {args.early_stopping_patience} steps reached')
                                logger.info(' Training terminated.')
                                train_iterator.close()
                            return (global_step, tr_loss / global_step if not self.args.evaluate_during_training else training_progress_scores)
                    context_model.train()
                    query_model.train()
        epoch_number += 1
        output_dir_current = os.path.join(output_dir, 'checkpoint-{}-epoch-{}'.format(global_step, epoch_number))
        if args.save_model_every_epoch or args.evaluate_during_training:
            os.makedirs(output_dir_current, exist_ok=True)
        if args.save_model_every_epoch:
            self.save_model(output_dir_current, optimizer, scheduler, context_model=context_model, query_model=query_model)
        if args.evaluate_during_training and args.evaluate_each_epoch:
            (results, *_) = self.eval_model(eval_data, additional_passages=additional_eval_passages, verbose=verbose and args.evaluate_during_training_verbose, silent=args.evaluate_during_training_silent, **kwargs)
            if args.save_eval_checkpoints:
                self.save_model(output_dir_current, optimizer, scheduler, results=results)
            training_progress_scores['global_step'].append(global_step)
            training_progress_scores['train_loss'].append(current_loss)
            for key in results:
                training_progress_scores[key].append(results[key])
            report = pd.DataFrame(training_progress_scores)
            report.to_csv(os.path.join(args.output_dir, 'training_progress_scores.csv'), index=False)
            if args.wandb_project or self.is_sweeping:
                wandb.log(self._get_last_metrics(training_progress_scores))
            if not best_eval_metric:
                best_eval_metric = results[args.early_stopping_metric]
                if args.save_best_model:
                    self.save_model(args.best_model_dir, optimizer, scheduler, context_model=context_model, query_model=query_model, results=results)
            if best_eval_metric and args.early_stopping_metric_minimize:
                if results[args.early_stopping_metric] - best_eval_metric < args.early_stopping_delta:
                    best_eval_metric = results[args.early_stopping_metric]
                    if args.save_best_model:
                        self.save_model(args.best_model_dir, optimizer, scheduler, context_model=context_model, query_model=query_model, results=results)
                    early_stopping_counter = 0
                elif args.use_early_stopping and args.early_stopping_consider_epochs:
                    if early_stopping_counter < args.early_stopping_patience:
                        early_stopping_counter += 1
                        if verbose:
                            logger.info(f' No improvement in {args.early_stopping_metric}')
                            logger.info(f' Current step: {early_stopping_counter}')
                            logger.info(f' Early stopping patience: {args.early_stopping_patience}')
                    else:
                        if verbose:
                            logger.info(f' Patience of {args.early_stopping_patience} steps reached')
                            logger.info(' Training terminated.')
                            train_iterator.close()
                        return (global_step, tr_loss / global_step if not self.args.evaluate_during_training else training_progress_scores)
            elif results[args.early_stopping_metric] - best_eval_metric > args.early_stopping_delta:
                best_eval_metric = results[args.early_stopping_metric]
                if args.save_best_model:
                    self.save_model(args.best_model_dir, optimizer, scheduler, context_model=context_model, query_model=query_model, results=results)
                early_stopping_counter = 0
            elif args.use_early_stopping and args.early_stopping_consider_epochs:
                if early_stopping_counter < args.early_stopping_patience:
                    early_stopping_counter += 1
                    if verbose:
                        logger.info(f' No improvement in {args.early_stopping_metric}')
                        logger.info(f' Current step: {early_stopping_counter}')
                        logger.info(f' Early stopping patience: {args.early_stopping_patience}')
                else:
                    if verbose:
                        logger.info(f' Patience of {args.early_stopping_patience} steps reached')
                        logger.info(' Training terminated.')
                        train_iterator.close()
                    return (global_step, tr_loss / global_step if not self.args.evaluate_during_training else training_progress_scores)
    return (global_step, tr_loss / global_step if not self.args.evaluate_during_training else training_progress_scores)

