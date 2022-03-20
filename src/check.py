from aiotube import Channel, Video, Playlist, Extras, Search
import time


ts = time.perf_counter()
ch = Channel('GYROOO')
print(ch.livestreams)
te = time.perf_counter()
print(f'Time: {te - ts}seconds')
