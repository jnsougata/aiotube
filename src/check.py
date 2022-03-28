from aiotube import Channel, Video, Playlist, Extras, Search
import time

s = time.perf_counter()
d = Channel('UCh5HLPIDEDRAWocISKW_JKw')
print(d.info)
e = time.perf_counter()

print(f'Channel: {e-s:0.4f}s')
