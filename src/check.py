from aiotube import Channel, Video, Playlist, Extras, Search
import time


ts = time.perf_counter()
ch = Channel('GYROOO')
print(ch.name)
print(ch.views)
print(ch.created_at)
print(ch.country)
print(ch.subscribers)
print(ch.description)
print(ch.custom_url)
print(ch.url)
print(ch.banner)
print(ch.avatar)
te = time.perf_counter()
print(f'Individual attr taken: {te - ts}seconds')
print('\n-----------------------------\n')
new_ts = time.perf_counter()
print(ch.info)
new_te = time.perf_counter()
print(f'Info attr taken: {new_te - new_ts}seconds')
