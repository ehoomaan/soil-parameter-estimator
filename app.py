import streamlit as st

from modules.spt_corrections import (
    calculate_cn_liao_whitman,
    calculate_n60,
)


st.set_page_config(
    page_title="SPT Soil Parameter Estimation",
    layout="wide",
)


st.title("SPT-Based Soil Parameter Estimation")
st.caption("Single SPT N-value correction calculator")


st.sidebar.header("Project Settings")

unit_system = st.sidebar.radio(
    "Unit System",
    ["USCS", "SI"],
    horizontal=True,
)


# Create a narrower working area inside the wide page
left_margin, main_col, right_margin = st.columns([1, 2.2, 1])

with main_col:
    st.header("SPT Input and Corrections")
    
    spt_col, correction_col = st.columns([1, 3])
    
    with spt_col:
        n_field_text = st.text_input(
            "Measured SPT N-value",
            value="10",
        )
    
    with correction_col:
        selected_corrections = st.multiselect(
            "Corrections to apply",
            [
                "Hammer energy correction, CE",
                "Borehole diameter correction, CB",
                "Rod length correction, CR",
                "Sampler correction, CS",
                "Overburden correction, CN",
            ],
            default=[],
        )
    
    try:
        n_field = float(n_field_text)
    except ValueError:
        n_field = None

    ce = 1.0
    cb = 1.0
    cr = 1.0
    cs = 1.0
    cn = 1.0

    st.header("Correction Inputs")

    input_col1, input_col2 = st.columns(2)

    with input_col1:
        if "Hammer energy correction, CE" in selected_corrections:
            energy_ratio = st.number_input(
                "Hammer energy ratio, ER (%)",
                min_value=1.0,
                max_value=200.0,
                value=60.0,
                step=5.0,
            )

            ce = energy_ratio / 60.0
            st.caption(f"CE = {ce:.2f}")

        if "Borehole diameter correction, CB" in selected_corrections:
            if unit_system == "USCS":
                borehole_diameter = st.selectbox(
                    "Borehole diameter",
                    [
                        "2.5 to 4.5 in",
                        "6 in",
                        "8 in",
                    ],
                )
            else:
                borehole_diameter = st.selectbox(
                    "Borehole diameter",
                    [
                        "65 to 115 mm",
                        "150 mm",
                        "200 mm",
                    ],
                )

            if borehole_diameter in ["2.5 to 4.5 in", "65 to 115 mm"]:
                cb = 1.00
            elif borehole_diameter in ["6 in", "150 mm"]:
                cb = 1.05
            elif borehole_diameter in ["8 in", "200 mm"]:
                cb = 1.15

            st.caption(f"CB = {cb:.2f}")

        if "Rod length correction, CR" in selected_corrections:
            if unit_system == "USCS":
                rod_length = st.selectbox(
                    "Rod length",
                    [
                        "Less than 10 ft",
                        "10 to 13 ft",
                        "13 to 20 ft",
                        "20 to 30 ft",
                        "More than 30 ft",
                    ],
                )
            else:
                rod_length = st.selectbox(
                    "Rod length",
                    [
                        "Less than 3 m",
                        "3 to 4 m",
                        "4 to 6 m",
                        "6 to 10 m",
                        "More than 10 m",
                    ],
                )

            if rod_length in ["Less than 10 ft", "Less than 3 m"]:
                cr = 0.75
            elif rod_length in ["10 to 13 ft", "3 to 4 m"]:
                cr = 0.80
            elif rod_length in ["13 to 20 ft", "4 to 6 m"]:
                cr = 0.85
            elif rod_length in ["20 to 30 ft", "6 to 10 m"]:
                cr = 0.95
            elif rod_length in ["More than 30 ft", "More than 10 m"]:
                cr = 1.00

            st.caption(f"CR = {cr:.2f}")

    with input_col2:
        if "Sampler correction, CS" in selected_corrections:
            sampler_type = st.selectbox(
                "Sampler type",
                [
                    "Standard sampler with liners",
                    "Standard sampler without liners",
                ],
            )

            if sampler_type == "Standard sampler with liners":
                cs = 1.00
            elif sampler_type == "Standard sampler without liners":
                cs = 1.20

            st.caption(f"CS = {cs:.2f}")

        if "Overburden correction, CN" in selected_corrections:
            if unit_system == "SI":
                stress_label = "Effective vertical overburden pressure, σ'vo (kPa)"
                default_stress = 100.0
            else:
                stress_label = "Effective vertical overburden pressure, σ'vo (tsf)"
                default_stress = 1.0

            effective_overburden_pressure = st.number_input(
                stress_label,
                min_value=0.01,
                value=default_stress,
                step=0.1,
            )

            cn = calculate_cn_liao_whitman(
                effective_overburden_pressure=effective_overburden_pressure,
                unit_system=unit_system,
            )

            st.caption(f"CN = {cn:.2f}")

    st.divider()

    run_calculation = st.button("Calculate Corrected SPT N-Value")

    if run_calculation:
        if n_field is None:
            st.error("Measured SPT N-value must be numeric.")
        
        elif n_field <= 0:
            st.error("Measured SPT N-value must be greater than zero.")
        
        else:
            n60 = calculate_n60(
                n_field=n_field,
                energy_correction=ce,
                borehole_correction=cb,
                rod_length_correction=cr,
                sampler_correction=cs,
            )

            n_corrected = n60 * cn

            result_col1, result_col2, result_col3 = st.columns(3)

            with result_col1:
                st.metric("Measured N", f"{n_field:.1f}")

            with result_col2:
                st.metric("N60", f"{n60:.1f}")

            with result_col3:
                if "Overburden correction, CN" in selected_corrections:
                    st.metric("(N1)60", f"{n_corrected:.1f}")
                else:
                    st.metric("Corrected N", f"{n_corrected:.1f}")

            st.subheader("Correction Summary")

            st.dataframe(
                {
                    "Correction": [
                        "Measured SPT N",
                        "CE",
                        "CB",
                        "CR",
                        "CS",
                        "CN",
                        "N60 = N × CE × CB × CR × CS",
                        "Corrected N = N60 × CN",
                    ],
                    "Value": [
                        round(n_field, 2),
                        round(ce, 2),
                        round(cb, 2),
                        round(cr, 2),
                        round(cs, 2),
                        round(cn, 2),
                        round(n60, 2),
                        round(n_corrected, 2),
                    ],
                },
                use_container_width=True,
                hide_index=True,
            )
