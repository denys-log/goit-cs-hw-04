import threading
import os
import time


def search_in_file(keyword, filepath, result):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                if keyword in line:
                    if keyword not in result:
                        result[keyword] = []
                    result[keyword].append((filepath, line_num))
    except Exception as e:
        print(f"Error {filepath}: {e}")


def process_files(thread_id, files, keywords, result):
    for file in files:
        for keyword in keywords:
            search_in_file(keyword, file, result)


def distribute_files(file_list, num_threads):
    files_per_thread = [[] for _ in range(num_threads)]
    for i, file in enumerate(file_list):
        files_per_thread[i % num_threads].append(file)
    return files_per_thread


def main(keywords, files, num_threads):
    start_time = time.time()

    result = {}

    files_per_thread = distribute_files(files, num_threads)

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=process_files, args=(
            i+1, files_per_thread[i], keywords, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Results:")
    for key, value in result.items():
        print(f"{key}: {value}")

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    keywords = ["слово", "перше", "друге", "третє"]
    files = ["file1.txt", "file2.txt", "file3.txt"]
    num_threads = len(files)

    main(keywords, files, num_threads)
