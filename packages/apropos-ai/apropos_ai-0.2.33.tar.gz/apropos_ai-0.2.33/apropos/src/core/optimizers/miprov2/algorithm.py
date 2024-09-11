import random
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Literal, Tuple, Type, Callable

from apropos.src.bench.base import Benchmark,Question
from apropos.src.core.optimizers.base import DAGOptimizer
from apropos.src.core.programs.dag import LM_DAG, DagRecord
from apropos.src.core.programs.prompt import Demonstration, PromptTemplate, Topic
from apropos.src.core.optimizers.miprov2.instruction_gen_dags import (
    identify_problems_dag,
    plan_search_dag,
    resolve_deltas_dag,
    ProblemsResponse,
    InterventionConceptsResponse
)
from apropos.src.core.optimizers.miprov2.search_backends import SearchSpace, TPE_Optimizer, RandomSearch_Optimizer, PromptDelta
import asyncio

import optuna
random.seed(42)




# class ProblemsResponse(BaseModel):
#     problem_descriptions: List[str]
#     failure_modes: List[str]
#     example_questions: List[List[str]]
#     nodes_responsible: List[List[str]]

# class InterventionConceptsResponse(BaseModel):
#     intervention_concepts_by_node: Dict[str, List[str]]

# Core idea behind MIPRO-v2: test variations for solving the same problem

class MIPrO_V2p1_DAG(DAGOptimizer):
    student_program: LM_DAG
    teacher_program: LM_DAG
    dataset_handler: Type[Benchmark]
    search_space: SearchSpace

    def __init__(
        self,
        student_program: LM_DAG,
        dataset_handler: Type[Benchmark],
        teacher_program: LM_DAG = None,
        cfg: Dict = None,
    ):
        self.student_program = student_program
        self.dataset_handler = dataset_handler
        self.teacher_program = teacher_program or student_program
        self.search_space = SearchSpace(
            prompt_delta_variations_by_problem_by_node={},
            demos_by_problem_by_node={},
        )
        self.cfg = cfg
    
    
    def curate_questions_for_bootstrapping(self):
        pass

    def get_learnable_questions(self) -> Tuple[List[Question], List[List[DagRecord]], List[List[DagRecord]], List[float]]:
        learnable_questions = []
        successes = []
        failures = []
        pass_at_ks = []
        question_index_to_sample = 0
        while len(learnable_questions) < self.cfg["learnable_questions"]["max_n_to_obtain"] and question_index_to_sample < self.cfg["learnable_questions"]["max_n_to_sample"]:
            question = self.dataset_handler.train[question_index_to_sample]
            question_index_to_sample += 1
            temp_schedule = [self.cfg["learnable_questions"]["base_temp"] + 0.01 * _ for _ in range(self.cfg["learnable_questions"]["k_for_pass_at_k"])]
            temp_scheduled_programs = [deepcopy(self.student_program) for _ in range(self.cfg["learnable_questions"]["k_for_pass_at_k"])]
            for program, temperature in zip(temp_scheduled_programs, temp_schedule):
                for node in program.nodes.values():
                    node.transform.llm_config["temperature"] = temperature

            correctnesses_with_records = [
                question.compute_and_score_attempt_sync(program) for program in temp_scheduled_programs
            ]
            correctnesses = [correctness for correctness, _ in correctnesses_with_records]
            if sum(correctnesses) not in [0, len(correctnesses)]:
                learnable_questions.append(question)
                successes.append([record for correctness, record in correctnesses_with_records if correctness])
                failures.append([record for correctness, record in correctnesses_with_records if not correctness])
                pass_at_ks.append(sum(correctnesses)/len(correctnesses))
        return learnable_questions, successes, failures, pass_at_ks

    # Propose prompt instruction components (Simple => Plan Search)
    def propose_prompt_instruction_components_sync(self):
        # random.seed(42)
        # # changes can either be to the template + adding/removing instructions (later)
        # problems_response: ProblemsResponse = identify_problems_dag.run_standard(
        #     inputs = {
        #         "<<<HIGHLY_LEARNABLE_QUESTIONS>>>": learnable_questions,
        #         "<<<SUCCESS_RATES>>>": pass_at_ks,
        #         "<<<SUCCESS_TRACES>>>": [random.choice(successes)] if successes else [],
        #         "<<<FAILURE_TRACES>>>": [random.choice(failures)] if failures else []
        #     }
        # )
        # # or simply substitutions for instructions (now)
        # intervention_concepts_response: InterventionConceptsResponse = plan_search_dag.run_standard(
        # # step to scope which instructions etc to change
        # prompt_deltas_by_node = {}
        # #for problem_description
        # filter bootstrapped demos by node
        pass

    async def propose_prompt_instruction_components_example(self):
        #TODO: simple bootstrap for demos
        #Hard-code a few deltas
        #Test out for plan-execute gpt-4o-mini

        prompt_delta_variations_by_problem_by_node = {
            "plan_lacks_precision": {
                "Plan Solution": [PromptDelta(
    description="Enhance plan precision",
    message="system",
    subcomponent="objective",
    topic_name="objective",
    instructions_fields_edits={
        "$OBJECTIVE": "Please provide an extremely detailed, step-by-step plan to solve the given mathematics problem. Break down each step into smaller sub-steps, specifying exact formulas, equations, and calculations to be performed. Include precise instructions for handling intermediate results and clearly define how to arrive at the final answer."
    }
)],
                "Solve Problem": [PromptDelta(
    description="Request clarification for imprecise plans",
    message="system",
    subcomponent="premise",
    topic_name="premise",
    instructions_fields_edits={
        "$MAIN_INSTRUCTIONS": "You will be given the problem statement together with a high-level plan to solve it. Your task is to implement this plan, verifying its correctness at each step."
    }
)],
            },
            "execution_ignores_plan": {
                "Plan Solution": [PromptDelta(
    description="Emphasize plan adherence",
    message="user",
    subcomponent="user",
    topic_name="user",
    instructions_fields_edits={
        "$ENJOINDER": "Your plan should include:\n1. A clear statement of the given information and problem to be solved\n2. Identification of relevant mathematical concepts and techniques\n3. Definition of variables and known relationships\n4. A detailed step-by-step approach to solving the problem, including specific formulas or calculations needed for each step\n5. Explanation of the reasoning behind each step\n6. Explicit instructions for the execution phase, emphasizing the importance of following this plan precisely\n7. Verification steps to ensure correct implementation of the plan\n8. Description of how to present the final answer\n\nPlease provide your comprehensive and detailed plan below:"
    }
)],
                "Solve Problem": [
                    PromptDelta(
    description="Enforce strict plan adherence",
    message="system",
    subcomponent="objective",
    topic_name="objective",
    instructions_fields_edits={
        "$OBJECTIVE": "Solve the math problem by meticulously following the provided plan. For each step in your solution, explicitly reference the corresponding step in the plan. If you need to deviate from the plan, clearly explain why and how it affects the solution. Ensure that every aspect of the plan is addressed in your solution. Leave your answer at the very end of your response in the format \\boxed\\{YOUR_ANSWER\\}."
    }
)
                ],
            }
        }
        #TODO: filter demos by node
        bootstrapped_demos_by_node = await self.bootstrap_demonstrations(
            n=50,
            patches=["A", "B"]
        )
        bootstrapped_demos_by_problem_by_node = {
            "plan_lacks_precision": {
                "Plan Solution": bootstrapped_demos_by_node["Plan Solution"][0:5],
                "Solve Problem": bootstrapped_demos_by_node["Solve Problem"][0:5],
            },
            "execution_ignores_plan": {
                "Plan Solution": bootstrapped_demos_by_node["Plan Solution"][5:10],
                "Solve Problem": bootstrapped_demos_by_node["Solve Problem"][5:10],
            }
        }
        self.search_space = SearchSpace(
            prompt_delta_variations_by_problem_by_node=prompt_delta_variations_by_problem_by_node,
            demos_by_problem_by_node=bootstrapped_demos_by_problem_by_node,
        )

    def prepare_candidate_dag(self, prompt_deltas_by_node: Dict[str, List[PromptDelta]], demos_by_node: Dict[str, List[Demonstration]]):
        candidate_dag = deepcopy(self.student_program)
        for node_name, prompt_deltas in prompt_deltas_by_node.items():
            for prompt_delta in prompt_deltas:
                candidate_dag.nodes[node_name].transform.prompt = prompt_delta.apply(candidate_dag.nodes[node_name].transform.prompt)
        for node_name, demos in demos_by_node.items():
            candidate_dag.nodes[node_name].demonstrations = demos
        return candidate_dag

    # Evaluate a program
    def evaluate_program(self, dag: LM_DAG, questions: List[Question]) -> Tuple[float, int]:
        results = [
            question.evaluate(dag) for question in questions
        ]
        return sum([result for result in results])/len(results), len(results)

    # TPE sampler over demos + instructions
    def search(self, algorithm: Literal["TPE", "RandomSearch"] = "TPE"):
        if algorithm == "TPE":
            optimizer = TPE_Optimizer(seed=self.cfg["seed"], n_optuna_trials=self.cfg["n_optuna_trials"], questions_for_val=self.dataset_handler.dev[0:self.cfg["dev_size"]])
        elif algorithm == "RandomSearch":
            optimizer = RandomSearch_Optimizer(seed=self.cfg["seed"], n_optuna_trials=self.cfg["n_optuna_trials"], questions_for_val=self.dataset_handler.dev[0:self.cfg["dev_size"]])
        return optimizer.search(
            baseline_program=self.student_program,
            search_space=self.search_space,
        )

    def choose_best_program(self, programs: List[LM_DAG], scores: List[float]):
        return programs[scores.index(max(scores))]

    def optimize_program(self) -> LM_DAG:
        learnable_questions, successes, failures, pass_at_ks = self.get_learnable_questions()
        print("Got N learnable questions: ", len(learnable_questions))
        # questions_for_bootstrapping, questions_for_train, questions_for_val = self.curate_questions_for_bootstrapping()
        # bootstrapped_demos_by_node = self.bootstrap_demonstrations(questions_for_bootstrapping)

        # instruction_deltas_by_node = self.propose_instruction_deltas_by_node(bootstrapped_demos_by_node)
        asyncio.run(self.propose_prompt_instruction_components_example())
        best_program, scored_attempts = self.search(
            algorithm="TPE"
        )
        print("Scores: ", [score for score, _, _ in scored_attempts])
        return best_program





if __name__ == "__main__":
    from apropos.src.bench.hendryks_math.main import HendryksMath_Benchmark
    from apropos.src.bench.hendryks_math.dags.plan_execute import (
        hendryks_math_plan_execute_example,
    )
    benchmark = HendryksMath_Benchmark()
    plan_execute_dag = hendryks_math_plan_execute_example(
        model_names=["gpt-4o-mini"] * 2
    )
    mipro = MIPrO_V2p1_DAG(
        student_program=plan_execute_dag,
        dataset_handler=benchmark,
        teacher_program=plan_execute_dag,
        cfg={
            "seed": 42,
            "n_optuna_trials": 3,
            "dev_size": 30,
            "learnable_questions": {
                "max_n_to_obtain": 10,
                "max_n_to_sample": 20,
                "base_temp": 0.0,
                "k_for_pass_at_k": 5,
            }
        }
    )
    best_program = mipro.optimize_program()
    pass