import re
import aiotube
import locale

# simpleText":"Streamed live
# [{"gridRenderer":{"items":[{"gridVideoRenderer":{"videoId":"I1pvsCjyQC8"

ch = aiotube.Channel("UCYPvAwZP8pZhSMW8qs7cVCw")
print(ch.latest.url)
