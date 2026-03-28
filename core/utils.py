def retry(func, retries=3, delay=2):
    def wrapper(*args, **kwargs):
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if i == retries - 1:
                    raise e
                time.sleep(delay)
    return wrapper

