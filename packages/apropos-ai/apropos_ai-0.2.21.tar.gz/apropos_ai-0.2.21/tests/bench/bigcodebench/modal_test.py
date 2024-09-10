import asyncio
import unittest

from apropos.src.bench.bigcodebench.backends.modal import execute_code_remotely_modal_async
from apropos.src.bench.bigcodebench.main import BigCodeBenchComplete_Benchmark

class TestModalBackend(unittest.TestCase):
    async def run_single_test(self, i, question):
        try:
            result = await execute_code_remotely_modal_async(
                question.information, question.information["answer"]
            )
            
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            
            success, result_dict = result
            
            self.assertIsInstance(success, bool)
            self.assertEqual(success, True)
            self.assertIsInstance(result_dict, dict)
            
            expected_keys = {"errors", "failures", "testsRun", "wasSuccessful"}
            self.assertTrue(set(result_dict.keys()).issuperset(expected_keys))
        except AssertionError as e:
            print(f"Subtest {i + 1} failed: {str(e)}")
            raise
        else:
            pass
        finally:
            pass

    def test_execute_code_remotely_modal(self):
        benchmark = BigCodeBenchComplete_Benchmark()
        
        async def run_tests():
            tasks = [self.run_single_test(i, question) for i, question in enumerate(benchmark.train[0:10])]
            await asyncio.gather(*tasks)

        asyncio.run(run_tests())

if __name__ == "__main__":
    unittest.main()
