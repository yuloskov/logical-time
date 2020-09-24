from multiprocessing import Process, Pipe
from datetime import datetime


def local_time(counter):
    return f'(LOGICAL_TIME_VECTOR={counter}, LOCAL_TIME={datetime.now()})'


def calc_recv_timestamp(recv_time_stamp, counter):
    for id in range(len(counter)):
        counter[id] = max(recv_time_stamp[id], counter[id])
    return counter


def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print(f'Message sent from {pid} {local_time(counter)}')
    return counter


def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    counter[pid] += 1
    print(f'Message received at {pid} {local_time(counter)}')
    return counter


def event(pid, counter):
    counter[pid] += 1
    print(f'Event in {pid} {local_time(counter)}!')
    return counter


def process_one(pipe12):
    pid = 0
    counter = [0, 0, 0]
    counter = send_message(pipe12, pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)


def process_two(pipe21, pipe23):
    pid = 1
    counter = [0, 0, 0]
    counter = recv_message(pipe21, pid, counter)
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = recv_message(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = send_message(pipe23, pid, counter)


def process_three(pipe32):
    pid = 2
    counter = [0, 0, 0]
    counter = send_message(pipe32, pid, counter)
    counter = recv_message(pipe32, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe32, pid, counter)


if __name__ == '__main__':
    one_two, two_one = Pipe()
    two_three, three_two = Pipe()

    process1 = Process(target=process_one, args=(one_two,))
    process2 = Process(target=process_two, args=(two_one, two_three))
    process3 = Process(target=process_three, args=(three_two,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
