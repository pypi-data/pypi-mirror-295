import asyncio
import unittest
from typing import List

import numpy as np

from apropos.src.bench.bigcodebench.backends.docker import execute_code_remotely_docker_sync
from apropos.src.bench.bigcodebench.main import BigCodeBenchComplete_Benchmark, BigCodeBench_Question


class TestGoldOnSplit(unittest.TestCase):
    async def test_gold_on_split(self):
        bcb = BigCodeBenchComplete_Benchmark(mode="docker")
        splits = ["train", "dev", "test"]

        for split in splits:
            with self.subTest(split=split):
                if split == "train":
                    questions = bcb.train[:10]  # Limit to 10 questions for faster testing
                elif split == "dev":
                    questions = bcb.dev[:10]
                elif split == "test":
                    questions = bcb.test[:10]

                async def score_gold(question: BigCodeBench_Question):
                    answer = question.information["answer"]
                    correctness, result_dict, container = execute_code_remotely_docker_sync(
                        question.information, answer
                    )
                    return correctness, result_dict

                gold_scores = await asyncio.gather(
                    *[score_gold(question) for question in questions]
                )
                gold_scores = [score for score, _ in gold_scores]

                self.assertIsInstance(gold_scores, List)
                self.assertEqual(len(gold_scores), len(questions))
                self.assertTrue(all(isinstance(score, bool) for score in gold_scores))

                mean_score = np.mean(gold_scores)
                num_correct = np.sum(gold_scores)

                print(f"Gold scores for {split}: {gold_scores}")
                print(f"Mean gold score for {split}: {mean_score}")
                print(f"Num correct for {split}: {num_correct}")
                print(f"Num total for {split}: {len(gold_scores)}")

                self.assertGreaterEqual(mean_score, 0)
                self.assertLessEqual(mean_score, 1)
                self.assertGreaterEqual(num_correct, 0)
                self.assertLessEqual(num_correct, len(questions))

if __name__ == "__main__":
    unittest.main()