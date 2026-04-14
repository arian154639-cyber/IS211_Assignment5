"""
I did my best to keep this similar to the textbook examples, though I changed 
the variable names a bit, and some of the structure, but the output is mostly 
the same. I used a file path for main instead of url because the assignment 
instructions mentioned file instead of url. I also used some things I came across
in my reaearch such as the use of "any" to avoid more verbose statements.
"""

from queue import Queue
import csv
import argparse


class Request:
    def __init__(self, arrival_time, user_request, process_time):
        self.arrival_time = arrival_time
        self.user_request = user_request
        self.process_time = process_time
    def wait_time(self, current_time):
        return current_time - self.arrival_time

class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0
    def tick(self):
        if self.current_request != None:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_request = None
    def busy(self):
        return self.current_request != None
    def start_next(self, request):
        self.current_request = request
        self.time_remaining = request.process_time

def simulateOneServer(input_csv):
    requests = []

    with open(input_csv, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            arrival_time = int(row[0])
            user_request = row[1]
            process_time = int(row[2])
            requests.append(Request(arrival_time, user_request, process_time))

    server = Server()
    request_queue = Queue()
    wait_times = []

    current_second = 0

    while requests or not request_queue.empty() or server.busy():

        arriving = [request for request in requests if request.arrival_time == current_second]

        for request in arriving:
            request_queue.put(request)
            requests.remove(request)

        if not server.busy() and not request_queue.empty():
            next_request = request_queue.get()
            wait_times.append(next_request.wait_time(current_second))
            server.start_next(next_request)

        server.tick()
        current_second += 1

    average_wait = sum(wait_times) / len(wait_times) if wait_times else 0
    print(f"Average Wait: {average_wait:.2f} seconds")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    args = parser.parse_args()
    simulateOneServer(args.file)

if __name__ == "__main__":
    main()