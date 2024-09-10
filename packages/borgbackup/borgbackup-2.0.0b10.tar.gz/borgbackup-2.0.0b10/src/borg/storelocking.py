import datetime
import json
import random
import time

from borgstore.store import ObjectNotFound

from . import platform
from .checksums import xxh64
from .helpers import Error, ErrorWithTraceback, bin_to_hex
from .logger import create_logger

logger = create_logger(__name__)


class LockError(Error):
    """Failed to acquire the lock {}."""

    exit_mcode = 70


class LockErrorT(ErrorWithTraceback):
    """Failed to acquire the lock {}."""

    exit_mcode = 71


class LockFailed(LockErrorT):
    """Failed to create/acquire the lock {} ({})."""

    exit_mcode = 72


class LockTimeout(LockError):
    """Failed to create/acquire the lock {} (timeout)."""

    exit_mcode = 73


class NotLocked(LockErrorT):
    """Failed to release the lock {} (was not locked)."""

    exit_mcode = 74


class NotMyLock(LockErrorT):
    """Failed to release the lock {} (was/is locked, but not by me)."""

    exit_mcode = 75


class Lock:
    """
    A Lock for a resource that can be accessed in a shared or exclusive way.
    Typically, write access to a resource needs an exclusive lock (1 writer,
    no one is allowed reading) and read access to a resource needs a shared
    lock (multiple readers are allowed).

    If possible, try to use the contextmanager here like::

        with Lock(...) as lock:
            ...

    This makes sure the lock is released again if the block is left, no
    matter how (e.g. if an exception occurred).
    """

    def __init__(self, store, exclusive=False, sleep=None, timeout=1.0, stale=30 * 60, id=None):
        self.store = store
        self.is_exclusive = exclusive
        self.sleep = sleep
        self.timeout = timeout
        self.race_recheck_delay = 0.01  # local: 0.01, network/slow remote: >= 1.0
        self.other_locks_go_away_delay = 0.1  # local: 0.1, network/slow remote: >= 1.0
        self.retry_delay_min = 1.0
        self.retry_delay_max = 5.0
        self.stale_td = datetime.timedelta(seconds=stale)  # ignore/delete it if older
        self.refresh_td = datetime.timedelta(seconds=stale // 2)  # don't refresh it if younger
        self.last_refresh_dt = None
        self.id = id or platform.get_process_id()
        assert len(self.id) == 3

    def __enter__(self):
        return self.acquire()

    def __exit__(self, *exc):
        self.release()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id!r}>"

    def _create_lock(self, *, exclusive=None):
        assert exclusive is not None
        now = datetime.datetime.now(datetime.timezone.utc)
        timestamp = now.isoformat(timespec="milliseconds")
        lock = dict(exclusive=exclusive, hostid=self.id[0], processid=self.id[1], threadid=self.id[2], time=timestamp)
        value = json.dumps(lock).encode("utf-8")
        key = bin_to_hex(xxh64(value))
        self.store.store(f"locks/{key}", value)
        self.last_refresh_dt = now
        return key

    def _delete_lock(self, key, *, ignore_not_found=False):
        try:
            self.store.delete(f"locks/{key}")
        except ObjectNotFound:
            if not ignore_not_found:
                raise

    def _is_stale_lock(self, lock):
        now = datetime.datetime.now(datetime.timezone.utc)
        if lock["dt"] < now - self.stale_td:
            # lock is too old, it was not refreshed.
            return True
        if not platform.process_alive(lock["hostid"], lock["processid"], lock["threadid"]):
            # we KNOW that the lock owning process is dead.
            return True
        return False

    def _get_locks(self):
        locks = {}
        try:
            infos = list(self.store.list("locks"))
        except ObjectNotFound:
            return {}
        for info in infos:
            key = info.name
            content = self.store.load(f"locks/{key}")
            lock = json.loads(content.decode("utf-8"))
            lock["key"] = key
            lock["dt"] = datetime.datetime.fromisoformat(lock["time"])
            if self._is_stale_lock(lock):
                # ignore it and delete it (even if it is not from us)
                self._delete_lock(key, ignore_not_found=True)
            else:
                locks[key] = lock
        return locks

    def _find_locks(self, *, only_exclusive=False, only_mine=False):
        locks = self._get_locks()
        found_locks = []
        for key in locks:
            lock = locks[key]
            if (not only_exclusive or lock["exclusive"]) and (
                not only_mine or (lock["hostid"], lock["processid"], lock["threadid"]) == self.id
            ):
                found_locks.append(lock)
        return found_locks

    def acquire(self):
        # goal
        # for exclusive lock: there must be only 1 exclusive lock and no other (exclusive or non-exclusive) locks.
        # for non-exclusive lock: there can be multiple n-e locks, but there must not exist an exclusive lock.
        started = time.monotonic()
        while time.monotonic() - started < self.timeout:
            exclusive_locks = self._find_locks(only_exclusive=True)
            if len(exclusive_locks) == 0:
                # looks like there are no exclusive locks, create our lock.
                key = self._create_lock(exclusive=self.is_exclusive)
                # obviously we have a race condition here: other client(s) might have created exclusive
                # lock(s) at the same time in parallel. thus we have to check again.
                time.sleep(
                    self.race_recheck_delay
                )  # give other clients time to notice our exclusive lock, stop creating theirs
                exclusive_locks = self._find_locks(only_exclusive=True)
                if self.is_exclusive:
                    if len(exclusive_locks) == 1 and exclusive_locks[0]["key"] == key:
                        # success, we are the only exclusive lock! wait until the non-exclusive locks go away:
                        while time.monotonic() - started < self.timeout:
                            locks = self._find_locks(only_exclusive=False)
                            if len(locks) == 1 and locks[0]["key"] == key:
                                # success, we are alone!
                                return self
                            time.sleep(self.other_locks_go_away_delay)
                        break  # timeout
                    else:
                        # take back our lock as some other client(s) also created exclusive lock(s).
                        self._delete_lock(key, ignore_not_found=True)
                else:  # not is_exclusive
                    if len(exclusive_locks) == 0:
                        # success, noone else created an exclusive lock meanwhile!
                        # We don't care for other non-exclusive locks.
                        return self
                    else:
                        # take back our lock as some other client(s) also created exclusive lock(s).
                        self._delete_lock(key, ignore_not_found=True)
            # wait a random bit before retrying
            time.sleep(self.retry_delay_min + (self.retry_delay_max - self.retry_delay_min) * random.random())
        raise LockTimeout(str(self.store))

    def release(self):
        locks = self._find_locks(only_mine=True)
        if not locks:
            raise NotLocked(str(self.store))
        assert len(locks) == 1
        self._delete_lock(locks[0]["key"], ignore_not_found=True)
        self.last_refresh_dt = None

    def got_exclusive_lock(self):
        locks = self._find_locks(only_mine=True, only_exclusive=True)
        return len(locks) == 1

    def break_lock(self):
        """break ALL locks (not just ours)"""
        locks = self._get_locks()
        for key in locks:
            self._delete_lock(key, ignore_not_found=True)
        self.last_refresh_dt = None

    def migrate_lock(self, old_id, new_id):
        """migrate the lock ownership from old_id to new_id"""
        assert self.id == old_id
        assert len(new_id) == 3
        old_locks = self._find_locks(only_mine=True)
        assert len(old_locks) == 1
        self.id = new_id
        self._create_lock(exclusive=old_locks[0]["exclusive"])
        self._delete_lock(old_locks[0]["key"])
        now = datetime.datetime.now(datetime.timezone.utc)
        self.last_refresh_dt = now

    def refresh(self):
        """refresh the lock - call this frequently, but not later than every <stale> seconds"""
        now = datetime.datetime.now(datetime.timezone.utc)
        if self.last_refresh_dt is not None and now > self.last_refresh_dt + self.refresh_td:
            old_locks = self._find_locks(only_mine=True)
            if len(old_locks) == 0:
                # crap, my lock has been removed. :-(
                # this can happen e.g. if my machine has been suspended while doing a backup, so that the
                # lock will auto-expire. a borg client on another machine might then kill that lock.
                # if my machine then wakes up again, the lock will have vanished and we get here.
                # in this case, we need to abort the operation, because the other borg might have removed
                # repo objects we have written, but the referential tree was not yet full present, e.g.
                # no archive has been added yet to the manifest, thus all objects looked unused/orphaned.
                # another scenario when this can happen is a careless user running break-lock on another
                # machine without making sure there is no borg activity in that repo.
                raise LockTimeout(str(self.store))  # our lock was killed, there is no safe way to continue.
            assert len(old_locks) == 1  # there shouldn't be more than 1
            old_lock = old_locks[0]
            if old_lock["dt"] < now - self.refresh_td:
                self._create_lock(exclusive=old_lock["exclusive"])
                self._delete_lock(old_lock["key"])
                self.last_refresh_dt = now
