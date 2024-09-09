import asyncio
import unittest

from apropos.src.bench.bigcodebench.backends.modal import execute_code_remotely_modal_async
from apropos.src.bench.bigcodebench.main import BigCodeBenchComplete_Benchmark

class TestModalBackend(unittest.TestCase):
    def test_execute_code_remotely_modal(self):
        benchmark = BigCodeBenchComplete_Benchmark()
        
        for question in benchmark.train[3:4]:
            with self.subTest(question=question):
                print(question.information)
                print("----------------------------------")
                print(question.information["answer"])
                result = asyncio.run(
                    execute_code_remotely_modal_async(
                        question.information, question.information["answer"]
                    )
                )
                
                self.assertIsInstance(result, tuple)
                self.assertEqual(len(result), 2)
                
                success, result_dict = result
                
                self.assertIsInstance(success, bool)
                self.assertEqual(success, True)
                self.assertIsInstance(result_dict, dict)
                
                expected_keys = {"errors", "failures", "testsRun", "wasSuccessful"}
                self.assertTrue(set(result_dict.keys()).issuperset(expected_keys))

if __name__ == "__main__":
    unittest.main()