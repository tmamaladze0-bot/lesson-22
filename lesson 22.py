import time
import threading

teas = [
    ("მწვანე ჩაი", 1.0),
    ("შავი ჩაი", 1.5),
    ("ბალახის ჩაი", 2.0),
]

def make_tea(name, seconds):
    print(f"{name}: იწყება")
    time.sleep(seconds)
    print(f"{name}: მზადაა")

start = time.perf_counter()

for name, seconds in teas:
    make_tea(name, seconds)

end = time.perf_counter()
sequential_time = end - start
print(f"თანმიმდევრულად: {sequential_time:.1f} წმ")
thread_start = time.perf_counter()

workers = []

for name, seconds in teas:
    worker = threading.Thread(target=make_tea, args=(name, seconds))
    workers.append(worker)

for worker in workers:
    worker.start()
for worker in workers:
    worker.join()
thread_end = time.perf_counter()
threaded_time = thread_end - thread_start
print(f"სრედებით: {threaded_time:.1f} წმ")

speedup = sequential_time / threaded_time
print(f"აჩქარება: {speedup:.1f}x")

# ჯერ სამივე ჩაის მომზადებას ვიწყებთ, შემდეგ join()-ით სამივეს ველოდებით.
# ამიტომ სულ დაახლოებით 2 წამი გვჭირდება — იმდენი, რამდენიც ყველაზე ნელ ჩაის.

import time
import threading
import multiprocessing

def countdown(n):
    while n > 0:
        n -= 1
def wait(seconds):
    time.sleep(seconds)

def run_sequential(func, args_list):
    for arg in args_list:
        func(arg)
def run_threads(func, args_list):
    workers = []
    for arg in args_list:
        worker = threading.Thread(target=func, args=(arg,))
        workers.append(worker)
    for worker in workers:
            worker.start()
    for worker in workers:
            worker.join()
def run_processes(func, args_list):
    workers = []
    for arg in args_list:
        worker = multiprocessing.Process(target=func, args=(arg,))
        workers.append(worker)
    for worker in workers:
                worker.start()
    for worker in workers:
                worker.join()
def measure(runner, func, args_list):
    start = time.perf_counter()
    runner(func, args_list)
    end = time.perf_counter()
    return end - start

if __name__ == "__main__":

    wait_times = [1.0, 1.0, 1.0, 1.0]
    sequential_time = measure(run_sequential, wait, wait_times)
    threaded_time = measure(run_threads, wait, wait_times)

    print(f"თანმიმდევრულად: {sequential_time:.1f} წმ")
    print(f"სრედებით: {threaded_time:.1f} წმ")

    process_time = measure(run_processes, wait, wait_times)
    print(f"პროცესებით: {process_time:.1f} წმ")

    countdown_values = [10_000_000] * 4
    cpu_sequential_time = measure(run_sequential, countdown, countdown_values)
    print(f"ათვლა თანმიმდევრულად: {cpu_sequential_time:.1f} წმ")
    cpu_threaded_time = measure(run_threads, countdown, countdown_values)
    print(f"ათვლა სრედებით: {cpu_threaded_time:.1f} წმ")
    cpu_process_time = measure(run_processes, countdown, countdown_values)
    print(f"ათვლა პროცესებით: {cpu_process_time:.1f} წმ")
    print(f"ლოდინის აჩქარება სრედებით: {sequential_time / threaded_time:.1f}x")
    print(f"ლოდინის აჩქარება პროცესებით: {sequential_time / process_time:.1f}x")
    print(f"ათვლის აჩქარება სრედებით: {cpu_sequential_time / cpu_threaded_time:.1f}x")
    print(f"ათვლის აჩქარება პროცესებით: {cpu_sequential_time / cpu_process_time:.1f}x")

# ლოდინისას სრედების ლოდინის დრო ერთმანეთს ემთხვევა.
# ხოლო ათვლისას, როცა CPython-ში GIL ჩართულია,
# სრედები Python-ის კოდს ერთდროულად ვერ ასრულებენ.
# პროცესებს შეუძლიათ სხვადასხვა ბირთვზე იმუშაონ, თუმცა მათ გაშვებას თავისი დრო სჭირდება.