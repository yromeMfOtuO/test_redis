__author__ = 'weihao.lv'

import redis

conn = redis.Redis(host='host', port=6379, db=0, password='pwd')


def script_upload(script):
    sha = None

    def call(conn=conn, keys=[], args=[], force_evel=False):
        """

        :param conn:
        :param keys: keys 参数记录的是脚本可能会读取或者写入的所有的键， 将键集中在 keys 参数的做法
            有利于在使用多服务器分片的时候能够方便地对所有的 key 是否分片在当期那服务器做出检查
        :param args:
        :param force_evel:
        :return:
        """
        nonlocal sha # 测试 nonlocal 的变量被闭包持有，不会因为外部函数的再次执行被覆盖，每个闭包持有自己的 nonlocal 变量
        if not force_evel:
            if sha is None:
                sha = conn.execute_command("SCRIPT", 'LOAD', script, parse='LOAD')
        try:
            print(sha)
            return conn.execute_command("EVALSHA", sha, len(keys), *(keys + args))
        except redis.exceptions.ResponseError as msg:
            if not msg.args[0].startswith("NOSCRIPT"):
                raise

        return conn.execute_command("EVAL", script, len(keys), *(keys+args))
    return call


if __name__ == '__main__':

    ...
