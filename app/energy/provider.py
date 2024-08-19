from app.energy.providers import mock, energiemissie, joulz, kenter


def get_platform(provider_name: str, api_key: str):
    match provider_name:
        case "mock":  # test / demo adapter
            return mock.MockAdapter(api_key)
        case "energiemissie":
            return energiemissie.EnergiemissieAdapter(api_key)
        case "joulz":
            return joulz.JoulzAdapter(api_key)
        # case "fudura":
        #     return fudura.FuduraAdapter(allation.api_api_key)
        # case "tums":
        #     return tums.TumsAdapter(allation.api_api_key)
        case "kenter":
            return kenter.KenterAdapter(api_key)
        case _:
            raise RuntimeError(
                f"We do not support: {provider_name} as energy provider",
            )