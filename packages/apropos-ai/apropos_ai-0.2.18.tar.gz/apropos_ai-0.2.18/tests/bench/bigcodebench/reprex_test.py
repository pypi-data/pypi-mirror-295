import asyncio
import unittest

import io

import modal
from modal import App, Sandbox
from modal.exception import SandboxTimeoutError

from apropos.src.bench.bigcodebench.backends.shared import get_imports

app = App("bigcodebench")

async def execute_code_remotely_modal(
    question_dict, code_solution
):
    solution = question_dict["eval_info"]["code_prompt"] + code_solution
    packages, _ = get_imports(solution)
    test = question_dict["eval_info"]["test"]
    complete = solution + "\n" + test

    unit_test_script = """
import unittest
import io
def test_code():
    path = "script.py"
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern=path)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Convert result to a serializable format
    result_dict = {
        "errors": len(result.errors),
        "failures": len(result.failures),
        "testsRun": result.testsRun,
        "wasSuccessful": result.wasSuccessful()
    }
    return result.wasSuccessful(), result_dict

if __name__ == "__main__":
    success,result = test_code()
    print("Success:", success)
    print(result)
"""

    image = modal.Image.debian_slim(python_version="3.9")
    if packages:
        image = image.pip_install("uv")
        package_install_command = " ".join(packages)
        execution_image = image.run_commands(
            f"uv pip install --system --compile-bytecode {package_install_command}"
        )
    else:
        execution_image = image.run_commands("uv pip install --system --compile-bytecode")
    try:
        with modal.NetworkFileSystem.ephemeral() as nfs:
            await nfs.write_file.aio("script.py", io.BytesIO(complete.encode()))
            await nfs.write_file.aio(
                "unit_test_script.py", io.BytesIO(unit_test_script.encode())
            )
            sb = Sandbox.create(
                "bash",
                "-c",
                f"cd /vol && python -W ignore unit_test_script.py",
                image=execution_image,
                timeout=60,
                cloud="aws",
                network_file_systems={"/vol": nfs},
            )
            await sb.wait.aio()
            stdout = await sb.stdout.read.aio()
            stderr = await sb.stderr.read.aio()
            print(stdout)
            print(stderr)
            success = stdout.split("Success: ")[1].split("\n")[0] == "True"
            result_dict = eval(stdout.split("Success: ")[1].split("\n")[1])
            return success, result_dict
    except SandboxTimeoutError:
        return False, {
            "errors": 1,
            "failures": 0,
            "testsRun": 0,
            "wasSuccessful": False,
            "timeout": True,
        }

class TestModalReprex(unittest.TestCase):
    def test_reprex(self):
        question_information = {'question': 'from collections import Counter\nimport re\n\ndef task_func(word: str) -> list:\n    """\n    Finds the most common two-letter combination in a given, cleaned word (lowercased and alphabetic characters only) \n    and returns its frequency. The search is case-insensitive and ignores non-alphabetic characters.\n    \n    Requirements:\n    - collections.Counter\n    - re\n    \n    Parameters:\n    - word (str): The input string containing the word to analyze. The word should have a length of at least 2 to form pairs.\n    \n    Returns:\n    - list: A list containing a single tuple. The tuple consists of the most frequent two-letter combination (str) \n      and its frequency (int). Returns an empty list if the word has fewer than 2 letters, or after cleaning, \n      the word has fewer than 2 alphabetic characters.\n    \n    Examples:\n    >>> task_func("aaBBcc")\n    [(\'aa\', 1)]\n    >>> task_func("abc!abc")\n    [(\'ab\', 2)]\n    >>> task_func("a")\n    []\n    >>> task_func("abcd")\n    [(\'ab\', 1)]\n    >>> task_func("a1b2c3")\n    [(\'ab\', 1)]\n    """\n', 'answer': "    # Clean the word: lowercase and keep alphabetic characters only\n    clean_word = re.sub('[^a-z]', '', word.lower())\n    \n    if len(clean_word) < 2:\n        return []\n    \n    pairs = [clean_word[i:i+2] for i in range(len(clean_word) - 1)]\n    pair_counter = Counter(pairs)\n    most_common = pair_counter.most_common(1)\n    \n    # This check ensures we return the result directly from most_common without additional filtering\n    return most_common", 'gold_reasoning': "    # Clean the word: lowercase and keep alphabetic characters only\n    clean_word = re.sub('[^a-z]', '', word.lower())\n    \n    if len(clean_word) < 2:\n        return []\n    \n    pairs = [clean_word[i:i+2] for i in range(len(clean_word) - 1)]\n    pair_counter = Counter(pairs)\n    most_common = pair_counter.most_common(1)\n    \n    # This check ensures we return the result directly from most_common without additional filtering\n    return most_common", 'eval_info': {'code_prompt': 'from collections import Counter\nimport re\ndef task_func(word: str) -> list:\n', 'test': 'import unittest\nclass TestCases(unittest.TestCase):\n    def test_repeating_pairs(self):\n        self.assertEqual(task_func("aabbcc"), [(\'aa\', 1)], "Should identify single repeating pair")\n        \n    def test_mixed_repeating_pairs(self):\n        self.assertEqual(task_func("abcabc"), [(\'ab\', 2)], "Should identify most frequent pair in mixed sequence")\n        \n    def test_single_character(self):\n        self.assertEqual(task_func("a"), [], "Should return empty list for single character")\n        \n    def test_unique_pairs(self):\n        self.assertEqual(task_func("abcdef"), [(\'ab\', 1)], "Should handle all unique pairs")\n        \n    def test_empty_string(self):\n        self.assertEqual(task_func(""), [], "Should return empty list for empty string")\n    def test_case_insensitive(self):\n        # Corrected the expected count to match the correct behavior of the function\n        self.assertEqual(task_func("aAaAbbBB"), [(\'aa\', 3)], "Should be case-insensitive")\n    def test_ignore_non_alphabetic(self):\n        self.assertEqual(task_func("abc123abc!"), [(\'ab\', 2)], "Should ignore non-alphabetic characters")'}, 'topic': 'Text and String Processing'}
        answer = """
    # Clean the word: lowercase and keep alphabetic characters only
    clean_word = re.sub('[^a-z]', '', word.lower())
    
    if len(clean_word) < 2:
        return []
    
    pairs = [clean_word[i:i+2] for i in range(len(clean_word) - 1)]
    pair_counter = Counter(pairs)
    most_common = pair_counter.most_common(1)
    
    # This check ensures we return the result directly from most_common without additional filtering
    return most_common
"""
        result = asyncio.run(
            execute_code_remotely_modal_async(
                question_information, answer
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