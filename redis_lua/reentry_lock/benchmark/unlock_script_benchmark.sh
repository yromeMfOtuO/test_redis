# 解锁脚本测试，eval 第一个参数为 解锁脚本的 sha 值
# -c 标示客户端数量
# -n 标示总请求次数

/usr/local/redis-6.0.8/src/redis-benchmark \
-h 47.104.248.216 \
-p 6379 \
-a weihao.lv@redis \
-c 50 \
-n 100000 \
-t evalsha "fa23ede5c337053507dbe90f32f30b033db16c17" 1 "weihao" 13

