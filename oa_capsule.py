import json


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



def validate_legal_states(justice, cases, capsule_contract):
    fixture_contract = capsule_contract["fixture_contract"]
    case_id_field = fixture_contract["case_id_field"]
    target_state_field = fixture_contract["target_state_field"]

    legal_states = set(justice["output"]["state_consistency"])

    for case in cases:
        target_state = case[target_state_field]

        if target_state not in legal_states:
            raise ValueError(
                f"ILLEGAL TARGET STATE: "
                f"{case[case_id_field]} -> {target_state!r}"
            )


def validate_fixture_consistency(cases, capsule_contract):
    fixture_contract = capsule_contract["fixture_contract"]
    case_id_field = fixture_contract["case_id_field"]
    target_state_field = fixture_contract["target_state_field"]
    required_state_path = fixture_contract["required_state_path"]

    for case in cases:
        target_state = case[target_state_field]

        required_state = case
        for field in required_state_path:
            required_state = required_state[field]

        if target_state != required_state:
            raise ValueError(
                f"FIXTURE CONSISTENCY FAIL: "
                f"{case[case_id_field]} -> "
                f"{target_state!r} != {required_state!r}"
            )


def build_reasoning_case(case, capsule_contract):
    fields = capsule_contract["reasoning_case_fields"]

    return {
        field: case[field]
        for field in fields
    }


def validate_reasoning_case(reasoning_case, capsule_contract):
    allowed_fields = set(capsule_contract["reasoning_case_fields"])
    actual_fields = set(reasoning_case)

    if actual_fields != allowed_fields:
        raise ValueError(
            f"REASONING CASE BOUNDARY FAIL: "
            f"expected {sorted(allowed_fields)!r}, "
            f"got {sorted(actual_fields)!r}"
        )


def build_reasoning_justice(justice, capsule_contract):
    fields = capsule_contract["reasoning_justice_fields"]

    return {
        field: justice[field]
        for field in fields
    }


def validate_reasoning_justice(reasoning_justice, capsule_contract):
    allowed_fields = set(capsule_contract["reasoning_justice_fields"])
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

    consistency_contract = output_contract.get("consistency_contract")

    if consistency_contract:
        selector = consistency_contract["selector"]
        constraints = consistency_contract["constraints"]
        state_consistency = output_contract["state_consistency"]

        selector_value = reasoning_output[selector]

        if selector_value not in state_consistency:
            raise ValueError(
                f"REASONING OUTPUT STATE FAIL: "
                f"illegal {selector} {selector_value!r}"
            )

        legal_state = state_consistency[selector_value]

        for field in constraints:
            if reasoning_output[field] not in legal_state[field]:
                raise ValueError(
                    f"REASONING OUTPUT STATE FAIL: "
                    f"illegal {field} {reasoning_output[field]!r} "
                    f"for {selector} {selector_value!r}"
                )

    for field, declaration in output_contract["schema"].items():
        value = reasoning_output[field]

        if declaration == "string":
            if not isinstance(value, str):
                raise ValueError(
                    f"REASONING OUTPUT TYPE FAIL: "
                    f"{field} must be a string"
                )
            continue

        if declaration == "array":
            if not isinstance(value, list):
                raise ValueError(
                    f"REASONING OUTPUT TYPE FAIL: "
                    f"{field} must be an array"
                )
            continue

        allowed_values = [
            item.strip()
            for item in declaration.split("|")
        ]

        if value not in allowed_values:
            raise ValueError(
                f"REASONING OUTPUT ENUM FAIL: "
                f"illegal {field} {value!r}"
            )
