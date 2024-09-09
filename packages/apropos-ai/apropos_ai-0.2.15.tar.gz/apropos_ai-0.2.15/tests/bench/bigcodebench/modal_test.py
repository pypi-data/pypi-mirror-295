import asyncio
import unittest

from apropos.src.bench.bigcodebench.backends.modal import execute_code_remotely_modal
from apropos.src.bench.bigcodebench.main import BigCodeBenchComplete_Benchmark

class TestModalBackend(unittest.TestCase):
    def test_execute_code_remotely_modal(self):
        benchmark = BigCodeBenchComplete_Benchmark()
        question = benchmark.train[0]
        
        result = asyncio.run(
            execute_code_remotely_modal(
                question.information, question.information["answer"]
            )
        )
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        
        success, result_dict = result
        
        self.assertIsInstance(success, bool)
        self.assertIsInstance(result_dict, dict)
        
        expected_keys = {"errors", "failures", "testsRun", "wasSuccessful"}
        self.assertTrue(set(result_dict.keys()).issuperset(expected_keys))

if __name__ == "__main__":
    unittest.main()