PROVIDER_CONFIG = {
    "provider_name": None,
    "model_id": None,
    "configuration_version": None,
}


def provider_configured():
    return all(
        PROVIDER_CONFIG[field] is not None
        for field in (
            "provider_name",
            "model_id",
            "configuration_version",
        )
    )


def transport(reasoning_packet):
    if not provider_configured():
        raise RuntimeError(
            "PROVIDER ADAPTER BLOCKED: no provider configured"
        )

    raise RuntimeError(
        "PROVIDER TRANSPORT BLOCKED: transport implementation not installed"
    )
