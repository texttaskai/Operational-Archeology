import oa_runtime
import oa_provider
import oa_capsule


JUSTICE_PATH = "emotionless-analysis-justice-0.2.json"
CASES_PATH = "emotionless-analysis-justice-cases-0.2.json"


def load_json(path):
    return oa_capsule.load_json(path)


def validate_identity(justice, target):
    return oa_capsule.validate_identity(justice, target)


def build_reasoning_case(case, justice):
    return oa_capsule.build_reasoning_case(
        case,
        justice["capsule_contract"],
    )


def validate_reasoning_case(reasoning_case, justice):
    return oa_capsule.validate_reasoning_case(
        reasoning_case,
        justice["capsule_contract"],
    )


def build_reasoning_justice(justice):
    return oa_capsule.build_reasoning_justice(
        justice,
        justice["capsule_contract"],
    )


def validate_reasoning_justice(reasoning_justice, justice):
    return oa_capsule.validate_reasoning_justice(
        reasoning_justice,
        justice["capsule_contract"],
    )


def build_reasoning_packet(reasoning_justice, reasoning_case):
    return oa_capsule.build_reasoning_packet(
        reasoning_justice,
        reasoning_case,
    )


def validate_reasoning_packet(reasoning_packet):
    return oa_capsule.validate_reasoning_packet(
        reasoning_packet,
    )


def validate_reasoning_output(reasoning_output, output_contract):
    return oa_capsule.validate_reasoning_output(
        reasoning_output,
        output_contract,
    )


def self_test_reasoning_output_validator(output_contract):
    legal_output = {
        "truth_state": "SUPPORTED",
        "position": "Synthetic Emotionless Analysis validator self-test.",
        "citations": [],
    }
    validate_reasoning_output(legal_output, output_contract)

    illegal_extra_field = {
        "truth_state": "SUPPORTED",
        "position": "Synthetic Emotionless Analysis validator self-test.",
        "citations": [],
        "timing": "NOW",
    }

    try:
        validate_reasoning_output(
            illegal_extra_field,
            output_contract,
        )
    except ValueError:
        pass
    else:
        raise ValueError(
            "REASONING OUTPUT VALIDATOR SELF-TEST FAIL: "
            "extra field was accepted"
        )

    illegal_position_type = {
        "truth_state": "SUPPORTED",
        "position": ["not", "a", "string"],
        "citations": [],
    }

    try:
        validate_reasoning_output(
            illegal_position_type,
            output_contract,
        )
    except ValueError:
        pass
    else:
        raise ValueError(
            "REASONING OUTPUT VALIDATOR SELF-TEST FAIL: "
            "invalid position type was accepted"
        )

    illegal_citations_type = {
        "truth_state": "SUPPORTED",
        "position": "Synthetic Emotionless Analysis validator self-test.",
        "citations": "not-an-array",
    }

    try:
        validate_reasoning_output(
            illegal_citations_type,
            output_contract,
        )
    except ValueError:
        pass
    else:
        raise ValueError(
            "REASONING OUTPUT VALIDATOR SELF-TEST FAIL: "
            "invalid citations type was accepted"
        )

    illegal_truth_state = {
        "truth_state": "MAYBE",
        "position": "Synthetic Emotionless Analysis validator self-test.",
        "citations": [],
    }

    try:
        validate_reasoning_output(
            illegal_truth_state,
            output_contract,
        )
    except ValueError:
        pass
    else:
        raise ValueError(
            "REASONING OUTPUT VALIDATOR SELF-TEST FAIL: "
            "invalid truth state was accepted"
        )

    missing_truth_state = {
        "position": "Synthetic Emotionless Analysis validator self-test.",
        "citations": [],
    }

    try:
        validate_reasoning_output(
            missing_truth_state,
            output_contract,
        )
    except ValueError:
        pass
    else:
        raise ValueError(
            "REASONING OUTPUT VALIDATOR SELF-TEST FAIL: "
            "missing truth state was accepted"
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
    original_state = dict(oa_provider.PROVIDER_CONFIG)

    try:
        oa_provider.PROVIDER_CONFIG.update({
            "provider_name": None,
            "model_id": None,
            "configuration_version": None,
        })

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
        oa_provider.PROVIDER_CONFIG.clear()
        oa_provider.PROVIDER_CONFIG.update(original_state)


def self_test_provider_configured_without_transport():
    original_state = dict(oa_provider.PROVIDER_CONFIG)

    try:
        oa_provider.PROVIDER_CONFIG.update({
            "provider_name": "synthetic-provider",
            "model_id": "synthetic-model",
            "configuration_version": "test",
        })

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
        oa_provider.PROVIDER_CONFIG.clear()
        oa_provider.PROVIDER_CONFIG.update(original_state)

def main():
    justice = load_json(JUSTICE_PATH)["justice"]
    fixture = load_json(CASES_PATH)["test_fixture"]
    target = fixture["target_justice"]
    cases = fixture["cases"]

    print("EMOTIONLESS ANALYSIS JUSTICE LOAD: PASS")

    validate_identity(justice, target)
    print("JUSTICE BINDING: PASS")

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
    validate_reasoning_justice(reasoning_justice, justice)
    print("REASONING JUSTICE BOUNDARY: PASS")

    for case in cases:
        reasoning_case = build_reasoning_case(case, justice)
        validate_reasoning_case(reasoning_case, justice)

        reasoning_packet = build_reasoning_packet(
            reasoning_justice,
            reasoning_case,
        )
        validate_reasoning_packet(reasoning_packet)

    print("REASONING CASE BOUNDARY: PASS")
    print("REASONING PACKET BOUNDARY: PASS")


if __name__ == "__main__":
    main()
