import streamlit as st

from modules.spt_corrections import (
    calculate_cn_liao_whitman,
    calculate_n60,
    calculate_n160,
)
from modules.validation import (
    validate_correction_factor,
    validate_positive,
)


st.set_page_config(
    page_title="SPT Soil Parameter Estimation",
    layout="wide",
)


st.title("SPT-Based Soil Parameter Estimation")
st.caption("Step 1: SPT correction calculations only")


st.sidebar.header("Project Settings")

unit_system = st.sidebar.radio(
    "Unit System",
    ["USCS", "SI"],
    horizontal=True,
)

st.header("SPT Input Data")

col1, col2 = st.columns(2)

with col1:
    n_field = st.number_input(
        "Measured SPT N-value",
        min_value=0.0,
        value=10.0,
        step=1.0,
    )

    energy_correction = st.number_input(
        "Energy correction factor, CE",
        min_value=0.01,
        value=1.00,
        step=0.05,
    )

    borehole_correction = st.number_input(
        "Borehole diameter correction factor, CB",
        min_value=0.01,
        value=1.00,
        step=0.05,
    )

with col2:
    rod_length_correction = st.number_input(
        "Rod length correction factor, CR",
        min_value=0.01,
        value=1.00,
        step=0.05,
    )

    sampler_correction = st.number_input(
        "Sampler correction factor, CS",
        min_value=0.01,
        value=1.00,
        step=0.05,
    )

    if unit_system == "SI":
        stress_label = "Effective overburden pressure, σ'vo (kPa)"
        default_stress = 100.0
    else:
        stress_label = "Effective overburden pressure, σ'vo (tsf)"
        default_stress = 1.0

    effective_overburden_pressure = st.number_input(
        stress_label,
        min_value=0.01,
        value=default_stress,
        step=0.1,
    )


run_calculation = st.button("Calculate SPT Corrections")


if run_calculation:
    errors = []

    checks = [
        validate_positive(n_field, "Measured SPT N-value"),
        validate_correction_factor(energy_correction, "CE"),
        validate_correction_factor(borehole_correction, "CB"),
        validate_correction_factor(rod_length_correction, "CR"),
        validate_correction_factor(sampler_correction, "CS"),
        validate_positive(effective_overburden_pressure, "Effective overburden pressure"),
    ]

    errors = [error for error in checks if error is not None]

    if errors:
        for error in errors:
            st.error(error)

    else:
        n60 = calculate_n60(
            n_field=n_field,
            energy_correction=energy_correction,
            borehole_correction=borehole_correction,
            rod_length_correction=rod_length_correction,
            sampler_correction=sampler_correction,
        )

        cn = calculate_cn_liao_whitman(
            effective_overburden_pressure=effective_overburden_pressure,
            unit_system=unit_system,
        )

        n160 = calculate_n160(
            n60=n60,
            cn=cn,
        )

        st.success("SPT correction calculation completed.")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric("N60", f"{n60:.1f}")

        with result_col2:
            st.metric("CN", f"{cn:.2f}")

        with result_col3:
            st.metric("(N1)60", f"{n160:.1f}")

        st.subheader("Calculation Summary")

        st.dataframe(
            {
                "Parameter": [
                    "Measured SPT N",
                    "CE",
                    "CB",
                    "CR",
                    "CS",
                    "N60",
                    "CN",
                    "(N1)60",
                ],
                "Value": [
                    n_field,
                    energy_correction,
                    borehole_correction,
                    rod_length_correction,
                    sampler_correction,
                    round(n60, 2),
                    round(cn, 2),
                    round(n160, 2),
                ],
            },
            use_container_width=True,
            hide_index=True,
        )
