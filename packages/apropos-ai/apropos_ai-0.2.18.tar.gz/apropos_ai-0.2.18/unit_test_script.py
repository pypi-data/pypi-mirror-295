import unittest
import io


def test_code():
    path = "script.py"
    loader = unittest.TestLoader()
    suite = loader.discover("/app", pattern=path)

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    result_dict = {
        "errors": len(result.errors),
        "failures": len(result.failures),
        "testsRun": result.testsRun,
        "wasSuccessful": result.wasSuccessful(),
    }
    return result.wasSuccessful(), result_dict


if __name__ == "__main__":
    success, result = test_code()
    print("Success:", success)
    print(result)
