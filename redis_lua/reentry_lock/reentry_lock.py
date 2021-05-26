__author__ = 'weihao.lv'

from redis_lua.script_upload import script_upload

lock = script_upload("""
local lockKey = KEYS[1]
-- 代表重入请求的唯一 id
local requestId = ARGV[1]

if redis.call('EXISTS', lockKey) ~= 0 then
    local lockTable = redis.call("HMGET", lockKey, 'requestId', 'count')
    if (requestId ~= lockTable[1]) then
        return 0
    else
        redis.call('HMSET', lockKey, 'count', lockTable[2] + 1)
        return 1
    end
else
    redis.call("HMSET", lockKey, 'requestId', requestId, 'count', 1)
    redis.call("EXPIRE", lockKey, 30)
    return 1
end
""")


unlock = script_upload("""
local lockKey = KEYS[1]
-- 代表重入请求的唯一 id
local requestId = ARGV[1]

-- key 不存在说明已经过期或者被释放了，直接 return 1 标示解锁成功
if redis.call('EXISTS', lockKey) == 0 then
    return 1
end

-- 获取当前锁
local lockTable = redis.call("HMGET", lockKey, 'requestId', 'count')
if (requestId ~= lockTable[1]) then
    -- 请求唯一 id 不同说明不是同一次业务请求，无法解锁
    return 0
elseif (tonumber(lockTable[2]) <= 1) then
    -- 最后一次解锁，直接删除锁
    redis.call('DEL', lockKey)
    return 1
else
    -- 解锁一次
    redis.call("HINCRBY", lockKey, 'count', -1)
    return 1
end
""")

if __name__ == '__main__':
    print(lock(keys=['weihao'], args=[13]))
