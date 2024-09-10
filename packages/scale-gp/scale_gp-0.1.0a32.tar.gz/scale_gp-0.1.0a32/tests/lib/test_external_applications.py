from __future__ import annotations

import os

import pytest

from scale_gp import SGPClient
from tests.utils import assert_matches_type
from scale_gp.lib.external_applications import ExternalApplication, ExternalApplicationOutputCompletion
from scale_gp.types.evaluation_datasets.test_case import TestCase

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExternalApplicationsLibrary:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_initialize(self, client: SGPClient) -> None:
        ExternalApplication(client).initialize(
            application_variant_id="application_variant_id",
            application=lambda prompt: ExternalApplicationOutputCompletion(generation_output=prompt),
        )

    @parametrize
    def test_generate_application_with_prompt(self, client: SGPClient) -> None:
        def application(prompt: str) -> ExternalApplicationOutputCompletion:
            assert_matches_type(str, prompt, path=["application", "prompt"])
            return ExternalApplicationOutputCompletion(generation_output=prompt)

        external_application = ExternalApplication(client).initialize(
            application_variant_id="application_variant_id",
            application=application,
        )
        external_application.generate_outputs(
            evaluation_dataset_id="evaluation_dataset_id",
            evaluation_dataset_version=int(),
        )

    @parametrize
    def test_generate_application_with_prompt_and_test_case(self, client: SGPClient) -> None:
        def application(prompt: str, test_case: TestCase) -> ExternalApplicationOutputCompletion:
            assert_matches_type(str, prompt, path=["application", "prompt"])
            assert_matches_type(TestCase, test_case, path=["application", "test_case"])
            return ExternalApplicationOutputCompletion(generation_output=prompt)

        external_application = ExternalApplication(client).initialize(
            application_variant_id="application_variant_id",
            application=application,
        )
        external_application.generate_outputs(
            evaluation_dataset_id="evaluation_dataset_id",
            evaluation_dataset_version=int(),
        )
