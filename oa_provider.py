PROVIDER_CONFIGURED = False


def transport(reasoning_packet):
    if not PROVIDER_CONFIGURED:
        raise RuntimeError(
            "PROVIDER ADAPTER BLOCKED: no provider configured"
        )

    raise RuntimeError(
        "PROVIDER TRANSPORT BLOCKED: transport implementation not installed"
    )
