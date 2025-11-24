import threading

def add_range(indx, val1, val2, result):
    sum_result = sum(range(val1, val2 + 1))
    result.insert(indx, sum_result)
    return result
        

def main():
    THREAD_COUNT = 5
    result = [] * THREAD_COUNT
    threads = []
    
    ranges = [
                [10, 20],
                [1, 5],
                [70, 80],
                [27, 92],
                [0, 16]
            ] 

    for indx in range(THREAD_COUNT):
        t = threading.Thread(target=add_range, args=(indx, ranges[indx][0], ranges[indx][1], result))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    print(f'thread results: {result}')

main()

#extension
#I used sum() to add up the range of numbers. Sum() uses a for loop to iterate through the range of numbers so its O(n) complexity
