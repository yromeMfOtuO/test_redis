import redis


def test_redis(name):
    with redis.Redis(host='host', port=6379, db=0, password='pwd') as r:
        r.set('name', 'test')


if __name__ == '__main__':
    test_redis('PyCharm')

