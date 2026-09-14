import json

import oa_runtime
import oa_provider


JUSTICE_PATH = "risk-justice-0.1.json"
CASES_PATH = "risk-justice-cases-0.1.json"

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_identity(justice, target):
    fields = ("name", "id", "version")

    for field in fields:
        if justice[field] != target[field]:
            raise ValueError(
                f"JUSTICE BINDING FAIL: {field} "
                f"{justice[field]!r} != {target[field]!r}"
            )



def validate_legal_states(justice, cases):
    legal_states = set(justice["output"]["state_consistency"])

    for case in cases:
        if case["target_state"] not in legal_states:
            raise ValueError(
                f"ILLEGAL TARGET STATE: {case['case_id']} -> {case['target_state']!r}"
            )


def validate_fixture_consistency(cases):
    for case in cases:
        target_state = case["target_state"]
        required_state = case["validation"]["required_finding_status"]

        if target_state != required_state:
            raise ValueError(
                f"FIXTURE CONSISTENCY FAIL: {case['case_id']} -> "
                f"{target_state!r} != {required_state!r}"
            )


def build_reasoning_case(case):
    return {
        "case_id": case["case_id"],
        "problem": case["problem"],
    }


def validate_reasoning_case(reasoning_case):
    allowed_fields = {"case_id", "problem"}
    actual_fields = set(reasoning_case)

    if actual_fields != allowed_fields:
        raise ValueError(
            f"REASONING CASE BOUNDARY FAIL: "
            f"expected {sorted(allowed_fields)!r}, "
            f"got {sorted(actual_fields)!r}"
        )


def build_reasoning_justice(justice):
    allowed_fields = (
        "name",
        "id",
        "version",
        "jurisdiction",
        "authority",
        "evidence_doctrine",
        "pillars",
        "scope",
        "must_not",
        "inputs",
        "output",
        "behavior",
    )

    return {
        field: justice[field]
        for field in allowed_fields
    }


def validate_reasoning_justice(reasoning_justice):
    allowed_fields = {
        "name",
        "id",
        "version",
        "jurisdiction",
        "authority",
        "evidence_doctrine",
        "pillars",
        "scope",
        "must_not",
        "inputs",
        "output",
        "behavior",
    }

    actual_fields = set(reasoning_justice)

    if actual_fields != allowed_fields:
        raise ValueError(
            f"REASONING JUSTICE BOUNDARY FAIL: "
            f"expected {sorted(allowed_fields)!r}, "
            f"got {sorted(actual_fields)!r}"
        )


def build_reasoning_packet(reasoning_justice, reasoning_case):
    return {
        "justice": reasoning_justice,
        "case": reasoning_case,
    }


def validate_reasoning_packet(reasoning_packet):
    allowed_fields = {"justice", "case"}
    actual_fields = set(reasoning_packet)

    if actual_fields != allowed_fields:
        raise ValueError(
            f"REASONING PACKET BOUNDARY FAIL: "
            f"expected {sorted(allowed_fields)!r}, "
            f"got {sorted(actual_fields)!r}"
        )


def validate_reasoning_output(reasoning_output, output_contract):
    expected_fields = set(output_contract["schema"])
    actual_fields = set(reasoning_output)

    if actual_fields != expected_fields:
        raise ValueError(
            f"REASONING OUTPUT SHAPE FAIL: "
            f"expected {sorted(expected_fields)!r}, "
            f"got {sorted(actual_fields)!r}"
        )

    finding_status = reasoning_output["finding_status"]
    state_consistency = output_contract["state_consistency"]

    if finding_status not in state_consistency:
        raise ValueError(
            f"REASONING OUTPUT STATE FAIL: "
            f"illegal finding_status {finding_status!r}"
        )

    legal_state = state_consistency[finding_status]

    if reasoning_output["risk_type"] not in legal_state["risk_type"]:
        raise ValueError(
            f"REASONING OUTPUT STATE FAIL: "
            f"illegal risk_type {reasoning_output['risk_type']!r} "
            f"for {finding_status!r}"
        )

    if reasoning_output["timing"] not in legal_state["timing"]:
        raise ValueError(
            f"REASONING OUTPUT STATE FAIL: "
            f"illegal timing {reasoning_output['timing']!r} "
            f"for {finding_status!r}"
        )

    if not isinstance(reasoning_output["position"], str):
        raise ValueError(
            "REASONING OUTPUT TYPE FAIL: position must be a string"
        )

    if not isinstance(reasoning_output["citations"], list):
        raise ValueError(
            "REASONING OUTPUT TYPE FAIL: citations must be an array"
        )


def self_test_reasoning_output_validator(output_contract):
    legal_output = {
        "finding_status": "NO MATERIAL RISK",
        "risk_type": "NONE",
        "timing": "NO RISK",
        "position": "Synthetic validator self-test.",
        "citations": [],
    }
    validate_reasoning_output(legal_output, output_contract)

    illegal_output = {
        "finding_status": "INSUFFICIENT EVIDENCE",
        "risk_type": "FINANCIAL",
        "timing": "NOW",
        "position": "Synthetic validator self-test.",
        "citations": [],
    }

    try:
        validate_reasoning_output(illegal_output, output_contract)
    except ValueError:
        return

    raise ValueError(
        "REASONING OUTPUT VALIDATOR SELF-TEST FAIL: "
        "illegal state combination was accepted"
    )




def self_test_blocked_provider_adapter():
    synthetic_packet = {
        "justice": {},
        "case": {},
    }

    expected_message = (
        "PROVIDER ADAPTER BLOCKED: no provider configured"
    )

    try:
        oa_provider.transport(synthetic_packet)
    except RuntimeError as exc:
        if str(exc) == expected_message:
            return

        raise ValueError(
            f"BLOCKED PROVIDER ADAPTER SELF-TEST FAIL: "
            f"unexpected message {str(exc)!r}"
        ) from exc

    raise ValueError(
        "BLOCKED PROVIDER ADAPTER SELF-TEST FAIL: "
        "provider transport was not blocked"
    )

def self_test_authorized_executor_reaches_blocked_adapter():
    synthetic_packet = {
        "justice": {},
        "case": {},
    }

    expected_message = (
        "PROVIDER ADAPTER BLOCKED: no provider configured"
    )

    original_authorization = oa_runtime.EXECUTION_AUTHORIZED

    try:
        oa_runtime.EXECUTION_AUTHORIZED = True

        try:
            oa_runtime.execute_reasoning(synthetic_packet)
        except RuntimeError as exc:
            if str(exc) == expected_message:
                return

            raise ValueError(
                "AUTHORIZED HANDOFF SELF-TEST FAIL: "
                f"unexpected message {str(exc)!r}"
            ) from exc

        raise ValueError(
            "AUTHORIZED HANDOFF SELF-TEST FAIL: "
            "provider adapter did not block transport"
        )
    finally:
        oa_runtime.EXECUTION_AUTHORIZED = original_authorization


def self_test_blocked_executor():
    synthetic_packet = {
        "justice": {},
        "case": {},
    }

    expected_message = (
        "REASONING EXECUTION BLOCKED: execution not authorized"
    )

    try:
        oa_runtime.execute_reasoning(synthetic_packet)
    except RuntimeError as exc:
        if str(exc) == expected_message:
            return

        raise ValueError(
            f"BLOCKED EXECUTOR SELF-TEST FAIL: "
            f"unexpected message {str(exc)!r}"
        ) from exc

    raise ValueError(
        "BLOCKED EXECUTOR SELF-TEST FAIL: execution was not blocked"
    )


def self_test_provider_unconfigured():
    original_state = oa_provider.PROVIDER_CONFIGURED

    try:
        oa_provider.PROVIDER_CONFIGURED = False

        expected_message = (
            "PROVIDER ADAPTER BLOCKED: no provider configured"
        )

        try:
            oa_provider.transport({
                "justice": {},
                "case": {},
            })
        except RuntimeError as exc:
            if str(exc) == expected_message:
                return

            raise ValueError(
                "PROVIDER UNCONFIGURED BAT FAIL: "
                f"unexpected message {str(exc)!r}"
            ) from exc

        raise ValueError(
            "PROVIDER UNCONFIGURED BAT FAIL: transport was not blocked"
        )
    finally:
        oa_provider.PROVIDER_CONFIGURED = original_state


def self_test_provider_configured_without_transport():
    original_state = oa_provider.PROVIDER_CONFIGURED

    try:
        oa_provider.PROVIDER_CONFIGURED = True

        expected_message = (
            "PROVIDER TRANSPORT BLOCKED: "
            "transport implementation not installed"
        )

        try:
            oa_provider.transport({
                "justice": {},
                "case": {},
            })
        except RuntimeError as exc:
            if str(exc) == expected_message:
                return

            raise ValueError(
                "PROVIDER CONFIGURED BAT FAIL: "
                f"unexpected message {str(exc)!r}"
            ) from exc

        raise ValueError(
            "PROVIDER CONFIGURED BAT FAIL: "
            "transport unexpectedly succeeded"
        )
    finally:
        oa_provider.PROVIDER_CONFIGURED = original_state

def main():
    justice = load_json(JUSTICE_PATH)["justice"]
    fixture = load_json(CASES_PATH)["test_fixture"]
    target = fixture["target_justice"]
    cases = fixture["cases"]

    print("RISK JUSTICE LOAD: PASS")

    validate_identity(justice, target)
    print("JUSTICE BINDING: PASS")

    validate_legal_states(justice, cases)
    print("LEGAL STATE ENFORCEMENT: PASS")

    validate_fixture_consistency(cases)
    print("FIXTURE CONSISTENCY: PASS")

    self_test_blocked_provider_adapter()
    print("BLOCKED PROVIDER ADAPTER SELF-TEST: PASS")

    self_test_provider_unconfigured()
    print("PROVIDER UNCONFIGURED BAT: PASS")

    self_test_provider_configured_without_transport()
    print("PROVIDER CONFIGURED / TRANSPORT BLOCKED BAT: PASS")

    self_test_authorized_executor_reaches_blocked_adapter()
    print("AUTHORIZED EXECUTOR HANDOFF SELF-TEST: PASS")

    self_test_blocked_executor()
    print("BLOCKED EXECUTOR SELF-TEST: PASS")

    self_test_reasoning_output_validator(justice["output"])
    print("REASONING OUTPUT VALIDATOR SELF-TEST: PASS")

    reasoning_justice = build_reasoning_justice(justice)
    validate_reasoning_justice(reasoning_justice)
    print("REASONING JUSTICE BOUNDARY: PASS")

    for case in cases:
        reasoning_case = build_reasoning_case(case)
        validate_reasoning_case(reasoning_case)

        reasoning_packet = build_reasoning_packet(
            reasoning_justice,
            reasoning_case,
        )
        validate_reasoning_packet(reasoning_packet)

    print("REASONING CASE BOUNDARY: PASS")
    print("REASONING PACKET BOUNDARY: PASS")


if __name__ == "__main__":
    main()
