import oa_provider


EXECUTION_AUTHORIZED = False


def execute_reasoning(reasoning_packet):
    if not EXECUTION_AUTHORIZED:
        raise RuntimeError(
            "REASONING EXECUTION BLOCKED: execution not authorized"
        )

    return oa_provider.transport(reasoning_packet)
