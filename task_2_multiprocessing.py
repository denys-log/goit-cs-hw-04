import os
from multiprocessing import Process, Queue
import time


def search_files(keywords, files, output):
    results = {}
    for keyword in keywords:
        keyword_results = []
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    for line_number, line in enumerate(f, 1):
                        if keyword in line:
                            keyword_results.append((file, line_number))
            except Exception as e:
                print(f"Error processing {file}: {e}")
        results[keyword] = keyword_results
    output.put(results)


if __name__ == "__main__":
    keywords = ["слово", "перше", "друге", "третє"]
    files = ["file1.txt", "file2.txt", "file3.txt"]

    num_processes = os.cpu_count()

    files_per_process = len(files) // num_processes
    processes = []
    output = Queue()

    start_time = time.time()

    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = (i + 1) * \
            files_per_process if i < num_processes - 1 else len(files)
        process_files = files[start_index:end_index]
        process = Process(target=search_files, args=(
            keywords, process_files, output))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = {}
    while not output.empty():
        result = output.get()
        results.update(result)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Results:")
    for key, value in results.items():
        print(f"{key}: {value}")

    print(f"Execution time: {execution_time} seconds")
