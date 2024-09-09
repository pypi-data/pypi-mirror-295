import asyncio
import unittest

from apropos.src.bench.bigcodebench.backends.docker import execute_code_remotely_docker
from apropos.src.bench.bigcodebench.main import BigCodeBenchComplete_Benchmark

class TestDockerBackend(unittest.TestCase):
    async def test_execute_code_remotely_docker(self):
        benchmark = BigCodeBenchComplete_Benchmark()
        question = benchmark.train[0]
        
        success, result_dict, container = await execute_code_remotely_docker(
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

    def test_execute_code_remotely_docker_sync(self):
        benchmark = BigCodeBenchComplete_Benchmark()
        question = benchmark.train[0]
        
        success, result_dict, container = asyncio.run(execute_code_remotely_docker(
            question.information, question.information["answer"]
        ))
        
        self.assertIsInstance(success, bool)
        self.assertIsInstance(result_dict, dict)
        self.assertIsNotNone(container)
        
        expected_keys = {"errors", "failures", "testsRun", "wasSuccessful"}
        self.assertTrue(set(result_dict.keys()).issuperset(expected_keys))
        
        self.assertIsInstance(result_dict["errors"], int)
        self.assertIsInstance(result_dict["failures"], int)
        self.assertIsInstance(result_dict["testsRun"], int)
        self.assertIsInstance(result_dict["wasSuccessful"], bool)

if __name__ == "__main__":
    unittest.main()