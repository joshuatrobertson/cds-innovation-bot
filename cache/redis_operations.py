import redis

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def store_slack_interaction(user_name, session_id, data):
    redis_key = f"slack_interaction:{user_name}:{session_id}"
    redis_client.hset(redis_key, mapping=data)
    redis_client.expire(redis_key, 600)  # Key expires after 10 minutes


def retrieve_slack_interaction(user_name, session_id):
    redis_key = f"slack_interaction:{user_name}:{session_id}"
    return redis_client.hgetall(redis_key)
