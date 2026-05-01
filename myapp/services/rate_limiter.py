from myapp.redis_client.redis import redis_client

LIMIT = 5
WINDOW = 60  

def is_allowed(user_id):
    key = f"rate_limit:{user_id}"

    current = redis_client.get(key)

    if current and int(current) >= LIMIT:
        return False

    pipe = redis_client.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, WINDOW)
    pipe.execute()

    return True