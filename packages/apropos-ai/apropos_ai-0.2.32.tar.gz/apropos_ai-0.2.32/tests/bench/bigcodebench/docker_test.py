import asyncio
import unittest

from apropos.src.bench.bigcodebench.backends.docker import execute_code_remotely_docker_sync
from apropos.src.bench.bigcodebench.main import BigCodeBenchComplete_Benchmark
import concurrent.futures

class TestDockerBackend(unittest.TestCase):
    def run_single_test(self, question, index):
        try:
            success, result_dict, container = execute_code_remotely_docker_sync(
                question.information, question.information["answer"]
            )
            
            self.assertIsInstance(success, bool)
            self.assertIsInstance(result_dict, dict)
            self.assertIsNotNone(container)
            
            expected_keys = {"errors", "failures", "testsRun", "wasSuccessful"}
            self.assertTrue(set(result_dict.keys()).issuperset(expected_keys))
            
            self.assertIsInstance(result_dict["errors"], int)
            self.assertIsInstance(result_dict["failures"], int)
            self.assertIsInstance(result_dict["testsRun"], int)
            self.assertIsInstance(result_dict["wasSuccessful"], bool)
        except Exception as e:
            return index, str(e)
        return None

    def test_execute_code_remotely_docker_sync(self):
        benchmark = BigCodeBenchComplete_Benchmark()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.run_single_test, question, i) for i, question in enumerate(benchmark.train[:10])]
            results = concurrent.futures.wait(futures)

        failed_indices = [result.result() for result in results.done if result.result() is not None]
        
        if failed_indices:
            failed_indices_str = ", ".join(f"Index {index}: {error}" for index, error in failed_indices)
            self.fail(f"Tests failed at the following indices:\n{failed_indices_str}")

if __name__ == "__main__":
    unittest.main()