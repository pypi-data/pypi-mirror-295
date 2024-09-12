### flexible_evaluation_example_script.py ###
# This script demonstrates how to create a flexible dataset and evaluation

# What is flexible dataset?

# A flexible dataset is a dataset that can be used to evaluate an application's performance against a set of test cases.
# Flexible datasets are able to perform anything a regular GENERATION dataset can do (covered by evaluation_example_script.py),
# but support a larger range of datatypes for both test case input and outputs.

# Flexible evaluation is only available for external/offline applications

# Schema for test case data:
# Input: Str | Dict[str, str | int | float | chunks | messages | list[any] | Dict[any, any]
# Expected_output: same as input but optional

# What is an evaluation?

# Evaluate an application variant against a rubric (question set) to determine how well the application variant performs.
# Depending on the evaluation type, either use a LLM, human, or mixed (LLM Benchmark) to answer questions comparing the
# response of an application variant to an expected response (test case expected output)
# The results of the evaluation can be used to help generate a report card for the application variant, benchmark performance, and compare variants.

# Required steps to perform a flexible evaluation:
# 1. Create a flexible evaluation dataset
# 2. Insert test cases into the flexible evaluation dataset and snapshot into a dataset version.
# 3. Create at question set with at least one question. The question set will be used to evaluate the the responses to the test cases.
# 4. Create an evaluation config using the question set and a desired evaluation type (human, llm or hybrid)
# 5. Create an offline application spec and variant.
# 6. Use the ExternalApplication class and a generator function which calls your offline application to generate outputs
# 7. Create an evaluation using the evaluation config, and the desired offline application variant.

import os
import time
from typing import Any, Dict
from datetime import datetime

from scale_gp import SGPClient
from scale_gp.lib.external_applications import ExternalApplication, ExternalApplicationOutputCompletion
from scale_gp.types.evaluation_datasets.test_case import TestCase

account_id = os.environ.get("SGP_ACCOUNT_ID", None)
api_key = os.environ.get("SGP_API_KEY", None)

# Either set these environment variables, or a default application variant and spec will be created
external_application_variant = os.environ.get("SGP_EXTERNAL_APPLICATION_VARIANT_ID", None)
external_application_spec = os.environ.get("SGP_EXTERNAL_APPLICATION_SPEC_ID", None)

assert (
    account_id is not None
), "You need to set the SGP_ACCOUNT_ID - you can find it at https://egp.dashboard.scale.com/admin/accounts"
assert api_key is not None, "You need to provide your API key - see https://egp.dashboard.scale.com/admin/api-key"

# Create an SGP Client
client = SGPClient(api_key=api_key)

# 1. Create a flexible evaluation dataset
flexible_evaluation_dataset = client.evaluation_datasets.create(
    account_id=account_id,
    name="flexible_evaluation_dataset",
    schema_type="FLEXIBLE",
    type="manual",
)

# 2. Batch insert test cases into the flexible evaluation dataset
TEST_CASES = [
    {
        "input": "Who is the first president of the united states?",
        "expected_output": "George Washington",
    },
    {
        "input": 1000000,
        "expected_output": "The number of dollars in a megadollar",
    },
    {
        "input": {
            "question_type": "who",
            "question": "Who is the second president of the united states?",
        },
        "expected_output": {
            "percieved_mode": "declaratory",
            "answer": "John Adams",
        },
    },
    {
        "input": [1, 2, 3, 4],
        "expected_output": [
            {"number": 1, "type": "integer"},
            {"number": 2, "type": "integer"},
            {"number": 3, "type": "integer"},
            {"number": 4, "type": "integer"},
        ],
    },
]

uploaded_test_cases = client.evaluation_datasets.test_cases.batch(
    evaluation_dataset_id=flexible_evaluation_dataset.id,
    items=[
        {"account_id": account_id, "schema_type": "FLEXIBLE", "test_case_data": test_case} for test_case in TEST_CASES
    ],
)
test_case_ids = [test_case.id for test_case in uploaded_test_cases]

# snapshot into a dataset version
flexible_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.create(
    evaluation_dataset_id=flexible_evaluation_dataset.id
)

# 3. Create at question set with at least one question. The question set will be used to evaluate the the responses to the test cases.
questions = [
    ("What is the answer?", "answer", "free_text", False),
    ("Is the answer good?", "isgood", "categorical", True),
]
question_ids = []
for question in questions:
    created_question = client.questions.create(
        account_id=account_id,
        prompt=question[0],
        title=question[1],
        type=question[2],
        choices=[
            {
                "label": "Yes",
                "value": 1,
            },
            {
                "label": "No",
                "value": 0,
            },
        ],
        required=question[3],
    )
    question_ids.append(created_question.id)

# create a question set using the desired questions
question_set = client.question_sets.create(
    account_id=account_id,
    name="US Presidents Question Set",
    question_ids=question_ids,
)

# 4. Create an evaluation config using the question set and a desired evaluation type (human, llm or hybrid)
evaluation_config = client.evaluation_configs.create(
    account_id=account_id,
    evaluation_type="human",  # ["llm_auto", "human", "llm_benchmark"]
    question_set_id=question_set.id,
)

# 5. Create an offline application spec and variant if no application spec id and variant id are provided
if not external_application_spec:
    application_spec = client.application_specs.create(
        account_id=account_id,
        description="Test application spec",
        name="test-application-spec" + str(time.time()),
    )
    external_application_spec = application_spec.id

if not external_application_variant:
    application_variant = client.application_variants.create(
        account_id=account_id,
        application_spec_id=external_application_spec,
        name="test offline application variant",
        version="OFFLINE",
        description="Test application variant",
        configuration={},
    )
    external_application_variant = application_variant.id


# 6. Use the ExternalApplication class and a generator function which calls your offline application to generate outputs
def application(prompt: Dict[str, Any], test_case: TestCase) -> ExternalApplicationOutputCompletion:
    response = "test response"  # Call your application with test case input here (test_case.test_case_data.input)
    print("prompt: ", prompt)
    print("test_case: ", test_case)
    print("generated output: ", response)
    metrics = {"accuracy": 0.9}  # whatever metrics you want to track
    traces = [  # whatever traces you want to track, such as what the output of each node inside the application was
        {
            "node_id": "completion",
            "operation_input": {
                "chunks": [
                    {
                        "text": "Hello world",
                    }
                ],
                "some_other_field": "some_other_value",
            },
            "operation_output": {
                "chunks": [
                    {
                        "text": "Hello world",
                    }
                ],
                "response": "Question: What is the answer?",
            },
            "start_timestamp": datetime.now(tz=None).isoformat(),
        },
    ]
    return ExternalApplicationOutputCompletion(generation_output=response, metrics=metrics, traces=traces)


external_application = ExternalApplication(client).initialize(
    application_variant_id=external_application_variant,
    application=application,
)

external_application.generate_outputs(
    evaluation_dataset_id=flexible_evaluation_dataset.id,
    evaluation_dataset_version=flexible_dataset_version.num,
)

generated_test_case_outputs = client.application_test_case_outputs.list(
    account_id=account_id,
    application_variant_id=external_application_variant,
    evaluation_dataset_id=flexible_evaluation_dataset.id,
    evaluation_dataset_version_num=flexible_dataset_version.num,
)
print("generated_test_case_outputs: ", generated_test_case_outputs.items)

# 7. Create an evaluation using the evaluation config, and the desired offline application variant.
# In this case, we are creating a human evaluation using the evaluation config created in step 4.
# Since this is a human evaluation, human annotators will be asked the questions defined in the question set about
# the test case outputs that we batch inserted in step 6. The results will be used to determine the performance of the application
# and generate repord cards and metrics
evaluation = client.evaluations.create(
    type="builder",
    account_id=account_id,
    application_spec_id=external_application_spec,
    application_variant_id=external_application_variant,
    description="description",
    evaluation_dataset_id=flexible_evaluation_dataset.id,
    name="Flexible eval",
    evaluation_config_id=evaluation_config.id,
)
