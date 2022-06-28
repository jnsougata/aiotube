from src.aiotube import Search, Channel, Video


if __name__ == '__main__':
    ch = Channel('UCeY0bbntWzzVIaj2z3QigXg')
    print(ch.recent_uploaded.info)
