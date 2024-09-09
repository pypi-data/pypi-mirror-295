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


if __name__ == "__main__":
    # test
    import asyncio

    from apropos.src.bench.bigcodebench.main import BigCodeBenchComplete_Benchmark

    question = BigCodeBenchComplete_Benchmark().train[0]
    print(
        asyncio.run(
            execute_code_remotely_modal(
                question.information, question.information["answer"]
            )
        )
    )
