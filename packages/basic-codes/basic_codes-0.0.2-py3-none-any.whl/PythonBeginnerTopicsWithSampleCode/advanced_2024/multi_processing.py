import multiprocessing
import time

start = time.time()

def square_numbers(numbers, result_queue):
    results = []
    for number in numbers:
        results.append(number * number)
    result_queue.put(results)

if __name__ == "__main__":
    # Input data
    numbers = [1, 2, 3, 4, 5,6,7,8,9,10,181,12,13,14,15,16,
               17,18,19,34,2567,36905,457,24,9765,95421,43,
               667578,456,67,453253,423454,79,54,45657,7,7,
                17,18,19,34,2567,36905,457,24,9765,95421,43,
               667578,456,67,453253,423454,79,54,45657,7,7,
                17,18,19,34,2567,36905,457,24,9765,95421,43,
               667578,456,67,453253,423454,79,54,45657,7,7,
                17,18,19,34,2567,36905,457,24,9765,95421,43,
               667578,456,67,453253,423454,79,54,45657,7,7,
                17,18,19,34,2567,36905,457,24,9765,95421,43,
               667578,456,67,453253,423454,79,54,45657,7,7,
                17,18,19,34,2567,36905,457,24,9765,95421,43,
               67,657,57,567,6774,67464, 23423,3423,3424,3]

    # Number of processes to create
    num_processes = 1

    # Create a multiprocessing Queue to collect results
    result_queue = multiprocessing.Queue()

    # Divide the data into chunks for each process
    chunk_size = len(numbers) // num_processes
    chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]

    print(chunks)

    # Create and start processes
    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(target=square_numbers, args=(chunk, result_queue))
        processes.append(process)
        processes.append(process)
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Collect results from the Queue
    results = []
    for _ in range(num_processes):
        results.extend(result_queue.get())

    # Print the squared results
    print("Original numbers:", numbers)
    print("Squared numbers:", results)

end = time.time()
print(end-start)