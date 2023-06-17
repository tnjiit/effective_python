from datetime import datetime, timedelta
import time, random

class Bucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return f'Bucket(quota={self.quota})'


class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return (f'NewBucket(max_quota={self.max_quota}, '
                f'quota_consumed={self.quota_consumed})')


    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reserved for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota eing filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # Quota being consumed during the period
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False # Bucket hasn't been filled this period
    if bucket.quota - amount < 0:
        return False # Bucket was filled but not enough
    bucket.quota -= amount
    return True


for _ in range(2):
    bucket = NewBucket(2)
    fill(bucket, 100)
    wait_time = random.randrange(0, 3)
    print(bucket)
    print(f'Will for {wait_time} seconds')
    time.sleep(wait_time)
    print(f'Waited for {wait_time} seconds')

    if deduct(bucket, 99):
        print(f'Had 99 quota {bucket}')
    else:
        print(f'Not enough for 99 quota {bucket}')
    print(bucket)
