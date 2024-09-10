import unittest
from concurrent.futures import ThreadPoolExecutor
from apropos.src.core.lms.helpers import LLM
import concurrent.futures

class TestMultithreading(unittest.TestCase):
    def test_multithreading(self):
        def get_task(i: int):
            system = "Solve the math problem"
            user = f"What is the product of 2 and {i}"
            return i, LLM("gpt-4o-mini").sync_respond(
                system_prompt=system,
                user_prompt=user,
                multi_threaded=True
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(get_task, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        self.assertEqual(len(results), 10)
        for i, result in results:
            expected_product = 2 * i
            try:
                self.assertIn(str(expected_product), result)
            except AssertionError:
                print(f"Test failed for i={i}")
                print(f"Expected product: {expected_product}")
                print(f"Actual result: {result}")
                raise


def get_task(i: int):
    system = "Solve the math problem"
    user = f"What is the product of 2 and {i}"
    return i, LLM("gpt-4o-mini").sync_respond(
        system_prompt=system,
        user_prompt=user,
        multi_threaded=True
    )
if __name__ == "__main__":
    unittest.main()
