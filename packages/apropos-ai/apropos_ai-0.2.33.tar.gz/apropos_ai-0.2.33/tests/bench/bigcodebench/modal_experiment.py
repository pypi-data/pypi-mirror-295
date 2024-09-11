import asyncio
import unittest
import time
import json
from apropos.src.bench.bigcodebench.backends.modal import execute_code_remotely_modal_async, app
from apropos.src.bench.bigcodebench.main import BigCodeBenchComplete_Benchmark


async def run_question(index: int):
    benchmark = BigCodeBenchComplete_Benchmark()
    question = benchmark.train[index]
    result = await execute_code_remotely_modal_async(
        question.information, question.information["answer"]
    )
    return result

#@app.local_entrypoint()
async def main():
    benchmark = BigCodeBenchComplete_Benchmark()
    async def process_question(i):
        t0 = time.time()
        try:
            result = await run_question(i)
        except Exception as e:
            print(f"Index {i} hard failed with error: {e}")
            return None
        elapsed_time = time.time() - t0
        if result[0] and result[1]["errors"] == 0:
            #print(f"Index {i} completed successfully")
            pass
        else:
            print(f"Index {i} failed")
        return elapsed_time

    tasks = [process_question(i+1) for i in range(0, 10)]#range(0, len(benchmark.train))
    times_taken = await asyncio.gather(*tasks)

    print(f"Average time taken: {sum(times_taken) / len(times_taken)}")
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.hist(times_taken, bins=20, edgecolor='black')
    plt.title('Distribution of Time Taken for BigCodeBench Questions')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency')
    plt.savefig('time_distribution.png')
    plt.close()

    print(f"Distribution plot saved as 'time_distribution.png'")
    times_taken_by_index = {i: t for i, t in enumerate(times_taken)}
    sorted_times = sorted(times_taken_by_index.items(), key=lambda x: x[1], reverse=True)
    top_5_longest = sorted_times[:5]
    for index, time_taken in top_5_longest:
        print(f"Index {index}: {time_taken:.2f} seconds")

if __name__ == "__main__":
    
    asyncio.run(main())
    #ModuleNotFoundError: No module named 'pytz'