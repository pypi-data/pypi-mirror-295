from pydantic import BaseModel
from apropos.src.core.utils.program_grounding import build_single_step_program
from apropos.src.core.programs.prompt import (
    PromptTemplate,
    SystemMessage,
    UserMessage,
    Topic,
)
from apropos.src.core.programs.dag import LM_DAG
import asyncio


class StepQualityScorer(BaseModel):
    score: int
    reasoning: str


def get_single_step_prm_dag_for_math_tree_search(
    model_name: str,
) -> LM_DAG:
    prompt = PromptTemplate(
        name="step_quality_scorer",
        system=SystemMessage(
            premise=[
                Topic(
                    topic_name="premise",
                    topic_template="You will be given a $MATH_QUESTION, a $COT, and a $CANDIDATE_STEP.",
                    instructions_fields={
                        "$MATH_QUESTION": "mathematics question",
                        "$COT": "chain of atomic reasoning steps",
                        "$CANDIDATE_STEP": "proposed next reasoning step",
                    },
                    input_fields=[],
                )
            ],
            objective=[
                Topic(
                    topic_name="objective",
                    topic_template="Your goal is to evaluate the quality of the $CANDIDATE_STEP and assign it a score from 0 to 10.",
                    instructions_fields={
                        "$CANDIDATE_STEP": "proposed next reasoning step"
                    },
                    input_fields=[],
                )
            ],
            constraints=[
                Topic(
                    topic_name="constraints",
                    topic_template="Consider the following criteria:\n- $RELEVANCE\n- $CORRECTNESS\n- $CLARITY\n- $PROGRESS\nProvide only the numerical score as output.",
                    instructions_fields={
                        "$RELEVANCE": "How relevant is the step to solving the problem?",
                        "$CORRECTNESS": "Is the step mathematically correct?",
                        "$CLARITY": "Is the step clear and easy to understand?",
                        "$PROGRESS": "Does the step make meaningful progress towards the solution?",
                    },
                    input_fields=[],
                )
            ],
        ),
        user=UserMessage(
            user=[
                Topic(
                    topic_name="user_input",
                    topic_template="$MATH_QUESTION: <<<MATHEMATICS_QUESTION>>>\n$COT:\n<<<CHAIN_OF_THOUGHT>>>\n$CANDIDATE_STEP: <<<CANDIDATE_STEP>>>\n\nQuality score (0-10):",
                    instructions_fields={},
                    input_fields=[
                        "<<<MATHEMATICS_QUESTION>>>",
                        "<<<CHAIN_OF_THOUGHT>>>",
                        "<<<CANDIDATE_STEP>>>",
                    ],
                )
            ],
        ),
        response_type="pydantic",
        response_model_scheme=StepQualityScorer.schema(),
        demonstrations=[],
    )

    single_step_prm_program = build_single_step_program(
        model_name=model_name,
        prompt=prompt,
        dag_input_names=[
            "<<<MATHEMATICS_QUESTION>>>",
            "<<<CHAIN_OF_THOUGHT>>>",
            "<<<CANDIDATE_STEP>>>",
        ],
        dag_input_aliases={
            "question": "<<<MATHEMATICS_QUESTION>>>",
            "cot": "<<<CHAIN_OF_THOUGHT>>>",
            "candidate_step": "<<<CANDIDATE_STEP>>>",
        },
        dag_output_aliases={"<<<FINAL_ANSWER>>>": "score"},
    )
    return single_step_prm_program


if __name__ == "__main__":
    model_name = "gpt-4o"
    single_step_prm_program = get_single_step_prm_dag_for_math_tree_search(model_name)
    inputs = {
        "<<<MATHEMATICS_QUESTION>>>": "What is the sum of 1 and 1?",
        "<<<CHAIN_OF_THOUGHT>>>": "1 + 1 = 2",
        "<<<CANDIDATE_STEP>>>": "2",
    }
    print(asyncio.run(single_step_prm_program.arun(inputs)))
