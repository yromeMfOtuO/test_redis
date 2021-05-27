# 加锁脚本测试，eval 第一个参数为 加锁脚本的 sha 值
# -c 标示客户端数量
# -n 标示总请求次数

/usr/local/redis-6.0.8/src/redis-benchmark \
-h 47.104.248.216 \
-p 6379 \
-a weihao.lv@redis \
-c 50 \
-n 100000 \
-t evalsha "0a70120a05fd06408cbd7ddf343dfc42e74ec4c8" 1 "weihao" 13

