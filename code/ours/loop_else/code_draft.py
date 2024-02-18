def do_kill_unit_from(self, conf):
    started = time.time()
    doSendSIGKILL = self.get_SendSIGKILL(conf)
    doSendSIGHUP = self.get_SendSIGHUP(conf)
    useKillMode = self.get_KillMode(conf)
    useKillSignal = self.get_KillSignal(conf)
    kill_signal = getattr(signal, useKillSignal)
    timeout = self.get_TimeoutStopSec(conf)
    status_file = self.get_status_file_from(conf)
    size = os.path.exists(status_file) and os.path.getsize(status_file)
    logg.info("STATUS %s %s", status_file, size)
    mainpid = self.read_mainpid_from(conf)
    self.clean_status_from(conf)  # clear RemainAfterExit and TimeoutStartSec
    if not mainpid:
        if useKillMode in ["control-group"]:
            logg.warning("no main PID %s", strQ(conf.filename()))
            logg.warning("and there is no control-group here")
        else:
            logg.info("no main PID %s", strQ(conf.filename()))
        return False
    if not pid_exists(mainpid) or pid_zombie(mainpid):
        logg.debug("ignoring children when mainpid is already dead")
        # because we list child processes, not processes in control-group
        return True
    pidlist = self.pidlist_of(mainpid)  # here
    if pid_exists(mainpid):
        logg.info("stop kill PID %s", mainpid)
        self._kill_pid(mainpid, kill_signal)
    if useKillMode in ["control-group"]:
        if len(pidlist) > 1:
            logg.info("stop control-group PIDs %s", pidlist)
        for pid in pidlist:
            if pid != mainpid:
                self._kill_pid(pid, kill_signal)
    if doSendSIGHUP:
        logg.info("stop SendSIGHUP to PIDs %s", pidlist)
        for pid in pidlist:
            self._kill_pid(pid, signal.SIGHUP)
    # wait for the processes to have exited
    while True:
        dead = True
        for pid in pidlist:
            if pid_exists(pid) and not pid_zombie(pid):
                dead = False
                break
        if dead:
            break
        if time.time() > started + timeout:
            logg.info("service PIDs not stopped after %s", timeout)
            break
        time.sleep(1)  # until TimeoutStopSec
    if dead or not doSendSIGKILL:
        logg.info("done kill PID %s %s", mainpid, dead and "OK")
        return dead
    if useKillMode in ["control-group", "mixed"]:
        logg.info("hard kill PIDs %s", pidlist)
        for pid in pidlist:
            if pid != mainpid:
                self._kill_pid(pid, signal.SIGKILL)
        time.sleep(MinimumYield)
    # useKillMode in [ "control-group", "mixed", "process" ]
    if pid_exists(mainpid):
        logg.info("hard kill PID %s", mainpid)
        self._kill_pid(mainpid, signal.SIGKILL)
        time.sleep(MinimumYield)
    dead = not pid_exists(mainpid) or pid_zombie(mainpid)
    logg.info("done hard kill PID %s %s", mainpid, dead and "OK")
    return dead