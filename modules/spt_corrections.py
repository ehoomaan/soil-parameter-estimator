import math


PA_KPA = 100.0
PA_TSF = 1.0


def calculate_n60(
    n_field: float,
    energy_correction: float,
    borehole_correction: float,
    rod_length_correction: float,
    sampler_correction: float,
) -> float:
    """
    Calculate energy-corrected SPT blow count N60.

    N60 = N * CE * CB * CR * CS
    """
    return (
        n_field
        * energy_correction
        * borehole_correction
        * rod_length_correction
        * sampler_correction
    )


def calculate_cn_liao_whitman(
    effective_overburden_pressure: float,
    unit_system: str,
    cn_max: float = 1.7,
) -> float:
    """
    Calculate overburden correction factor CN using a common square-root form.

    CN = sqrt(Pa / sigma_vo_eff)

    Parameters
    ----------
    effective_overburden_pressure:
        Effective vertical overburden pressure at the SPT depth.
        Use kPa for SI and tsf for USCS.

    unit_system:
        "SI" or "USCS".

    cn_max:
        Maximum allowed CN value.
    """
    if effective_overburden_pressure <= 0:
        raise ValueError("Effective overburden pressure must be greater than zero.")

    if unit_system == "SI":
        pa = PA_KPA
    elif unit_system == "USCS":
        pa = PA_TSF
    else:
        raise ValueError("unit_system must be either 'SI' or 'USCS'.")

    cn = math.sqrt(pa / effective_overburden_pressure)
    return min(cn, cn_max)


def calculate_n160(n60: float, cn: float) -> float:
    """
    Calculate overburden-corrected SPT blow count.

    (N1)60 = CN * N60
    """
    return cn * n60
