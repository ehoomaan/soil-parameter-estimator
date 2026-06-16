import streamlit as st
def format_engineering_value(value: float, unit_system: str, unit: str):
    """
    Format output values for engineering readability.

    For USCS rock modulus values in ksf, use scientific notation
    when the value has more than 6 digits.
    """
    if unit_system == "USCS" and unit == "ksf" and abs(value) >= 1_000_000:
        return f"{value:.3e}"

    if unit_system == "SI" and unit == "GPa":
        return f"{value:.2f}"

    return round(value, 0)
    
from modules.spt_corrections import (
    calculate_cn_liao_whitman,
    calculate_n60,
)
from modules.rock_correlations import (
    get_rock_elastic_modulus_reference,
    get_rock_types,
)

st.set_page_config(
    page_title="SPT Soil Parameter Estimation",
    layout="wide",
)


st.title("SPT-Based Soil Parameter Estimation")
st.caption("Single-point soil parameter estimation from physical properties and in-situ test data")


st.sidebar.header("Project Settings")

unit_system = st.sidebar.radio(
    "Unit System",
    ["USCS", "SI"],
    horizontal=True,
)


if unit_system == "SI":
    stress_unit = "kPa"
    density_unit = "kg/m³"
    length_unit = "m"
    spt_overburden_unit = "kPa"
    qc_unit = "kPa"
else:
    stress_unit = "psf"
    density_unit = "pcf"
    length_unit = "ft"
    spt_overburden_unit = "tsf"
    qc_unit = "ksf"


left_margin, main_col, right_margin = st.columns([0.6, 3.0, 0.6])


with main_col:

    # ------------------------------------------------------------
    # Section 1: Soil Physical Properties
    # ------------------------------------------------------------
    with st.container(border=True):
        st.subheader("1. Soil Physical Properties")

        soil_type = st.radio(
            "Soil Type",
            [
                "Cohesionless",
                "Cohesive",
            ],
            horizontal=True,
        )

        if unit_system == "SI":
            default_overburden = "100"
            overburden_label = "Effective vertical overburden pressure, σ'vo (kPa)"
        else:
            default_overburden = "1.0"
            overburden_label = "Effective vertical overburden pressure, σ'vo (tsf)"

        if soil_type == "Cohesionless":
            soil_col1, soil_col2 = st.columns([2, 1])

            with soil_col1:
                soil_description = st.selectbox(
                    "Cohesionless Soil Description",
                    [
                        "Silts, sandy silts, slightly cohesive mixtures",
                        "Clean fine to medium sands, slightly silty sands",
                        "Coarse sands and sands with little gravel",
                        "Sandy gravel and gravels",
                    ],
                )

            with soil_col2:
                effective_overburden_text = st.text_input(
                    overburden_label,
                    value=default_overburden,
                )

            moisture_content = None
            liquid_limit = None
            plastic_limit = None
            initial_void_ratio = None
            specific_gravity = None

        else:
            soil_description = None

            prop_col1, prop_col2, prop_col3 = st.columns(3)

            with prop_col1:
                effective_overburden_text = st.text_input(
                    overburden_label,
                    value=default_overburden,
                )

            with prop_col2:
                moisture_content = st.text_input(
                    "Moisture content, w (%)",
                    value="",
                )

            with prop_col3:
                liquid_limit = st.text_input(
                    "Liquid limit, LL (%)",
                    value="",
                )

            prop_col4, prop_col5, prop_col6 = st.columns(3)

            with prop_col4:
                plastic_limit = st.text_input(
                    "Plastic limit, PL (%)",
                    value="",
                )

            with prop_col5:
                initial_void_ratio = st.text_input(
                    "Initial void ratio, e₀",
                    value="",
                )

            with prop_col6:
                specific_gravity = st.text_input(
                    "Specific gravity, Gs",
                    value="",
                )

        try:
            effective_overburden_pressure = float(effective_overburden_text)
        except ValueError:
            effective_overburden_pressure = None

    # ------------------------------------------------------------
    # Section 2: Rock Properties
    # ------------------------------------------------------------
    with st.container(border=True):
        st.subheader("2. Rock Properties")

        rock_col1, rock_col2 = st.columns([1, 1])

        with rock_col1:
            rock_type = st.selectbox(
                "Rock type",
                ["Not applicable"] + get_rock_types(),
            )

        with rock_col2:
            if unit_system == "SI":
                qu_label = "Unconfined compressive strength, qu (kPa)"
            else:
                qu_label = "Unconfined compressive strength, qu (ksf)"

            rock_qu = st.text_input(
                qu_label,
                value="",
            )

    # ------------------------------------------------------------
    # Section 3: In-Situ Test Results
    # ------------------------------------------------------------
    with st.container(border=True):
        st.subheader("3. In-Situ Test Results")

        spt_col, correction_col = st.columns([1, 3])

        with spt_col:
            n_field_text = st.text_input(
                "Field SPT N-value",
                value="10",
            )

        with correction_col:
            selected_corrections = st.multiselect(
                "SPT corrections to apply",
                [
                    "Hammer energy correction, CE",
                    "Borehole diameter correction, CB",
                    "Rod length correction, CR",
                    "Sampler correction, CS",
                    "Overburden correction, CN",
                ],
                default=[],
            )

        ce = 1.0
        cb = 1.0
        cr = 1.0
        cs = 1.0
        cn = 1.0

        correction_input_col1, correction_input_col2, correction_input_col3 = st.columns(3)

        with correction_input_col1:
            if "Hammer energy correction, CE" in selected_corrections:
                energy_ratio_text = st.text_input(
                    "Hammer energy ratio, ER (%)",
                    value="60",
                )

                try:
                    energy_ratio = float(energy_ratio_text)
                    ce = energy_ratio / 60.0
                    st.caption(f"CE = {ce:.2f}")
                except ValueError:
                    st.caption("CE = invalid input")

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

        with correction_input_col2:
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

        with correction_input_col3:
            if "Overburden correction, CN" in selected_corrections:
                if effective_overburden_pressure is None:
                    st.warning("Enter a valid σ'vo in Section 1.")
                elif effective_overburden_pressure <= 0:
                    st.warning("σ'vo in Section 1 must be greater than zero.")
                else:
                    cn = calculate_cn_liao_whitman(
                        effective_overburden_pressure=effective_overburden_pressure,
                        unit_system=unit_system,
                    )
                    st.caption(
                        f"CN = {cn:.2f} using σ'vo = "
                        f"{effective_overburden_pressure:g} {spt_overburden_unit}"
                    )

        cpt_col1, cpt_col2 = st.columns(2)

        with cpt_col1:
            qc_text = st.text_input(
                f"CPT uncorrected tip resistance, qc ({qc_unit})",
                value="",
            )

        with cpt_col2:
            cpt_nk_text = st.text_input(
                "CPT Nk",
                value="",
            )


    # ------------------------------------------------------------
    # Section 4: Correlated Parameters
    # ------------------------------------------------------------
    with st.container(border=True):
        st.subheader("4. Correlated Parameters")

        run_calculation = st.button("Estimate Soil Parameters")

        if run_calculation:
            try:
                n_field = float(n_field_text)
            except ValueError:
                n_field = None

            errors = []

            if n_field is None:
                errors.append("Field SPT N-value must be numeric.")
            elif n_field <= 0:
                errors.append("Field SPT N-value must be greater than zero.")

            if "Overburden correction, CN" in selected_corrections:
                if effective_overburden_pressure is None:
                    errors.append("Effective vertical overburden pressure in Section 1 must be numeric.")
                elif effective_overburden_pressure <= 0:
                    errors.append("Effective vertical overburden pressure in Section 1 must be greater than zero.")

            if errors:
                for error in errors:
                    st.error(error)

            else:
                n60 = calculate_n60(
                    n_field=n_field,
                    energy_correction=ce,
                    borehole_correction=cb,
                    rod_length_correction=cr,
                    sampler_correction=cs,
                )

                n_corrected = n60 * cn

                if "Overburden correction, CN" in selected_corrections:
                    final_spt_label = "(N1)60"
                else:
                    final_spt_label = "Corrected SPT N"

                spt_results = [
                    {
                        "Parameter": "Measured SPT N",
                        "Estimated Value": round(n_field, 2),
                        "Unit": "-",
                        "Reference No.": "-",
                        "Notes": "User input",
                    },
                    {
                        "Parameter": "N60",
                        "Estimated Value": round(n60, 2),
                        "Unit": "-",
                        "Reference No.": "SPT-1",
                        "Notes": "N × CE × CB × CR × CS",
                    },
                    {
                        "Parameter": final_spt_label,
                        "Estimated Value": round(n_corrected, 2),
                        "Unit": "-",
                        "Reference No.": "SPT-2",
                        "Notes": "N60 × CN" if "Overburden correction, CN" in selected_corrections else "CN not applied",
                    },
                    {
                        "Parameter": "Unit weight, γ",
                        "Estimated Value": "Pending",
                        "Unit": density_unit,
                        "Reference No.": "-",
                        "Notes": "Correlation to be added",
                    },
                ]

                if soil_type == "Cohesive":
                    spt_results.extend(
                        [
                            {
                                "Parameter": "Undrained shear strength, cu",
                                "Estimated Value": "Pending",
                                "Unit": stress_unit,
                                "Reference No.": "-",
                                "Notes": "Correlation to be added",
                            },
                            {
                                "Parameter": "Soil consistency",
                                "Estimated Value": "Pending",
                                "Unit": "-",
                                "Reference No.": "-",
                                "Notes": "Based on estimated undrained shear strength, cu",
                            },
                            {
                                "Parameter": "Drained shear strength, c′",
                                "Estimated Value": "Pending",
                                "Unit": stress_unit,
                                "Reference No.": "-",
                                "Notes": "Correlation to be added",
                            },
                            {
                                "Parameter": "Drained friction angle for cohesive soils, φu",
                                "Estimated Value": "Pending",
                                "Unit": "deg",
                                "Reference No.": "-",
                                "Notes": "Correlation to be added",
                            },
                        ]
                    )

                else:
                    spt_results.extend(
                        [
                            {
                                "Parameter": "Drained friction angle for cohesionless soils, φ′",
                                "Estimated Value": "Pending",
                                "Unit": "deg",
                                "Reference No.": "-",
                                "Notes": "Correlation to be added",
                            },
                        ]
                    )

                spt_results.extend(
                    [
                        {
                            "Parameter": "Soil constrained modulus, Ms",
                            "Estimated Value": "Pending",
                            "Unit": "kPa" if unit_system == "SI" else "ksf",
                            "Reference No.": "-",
                            "Notes": "Correlation to be added",
                        },
                        {
                            "Parameter": "Soil elastic modulus, Es",
                            "Estimated Value": "Pending",
                            "Unit": "kPa" if unit_system == "SI" else "ksf",
                            "Reference No.": "-",
                            "Notes": "Correlation to be added",
                        },
                        {
                            "Parameter": "Compression index, Cc",
                            "Estimated Value": "Pending",
                            "Unit": "-",
                            "Reference No.": "-",
                            "Notes": "Correlation to be added",
                        },
                        {
                            "Parameter": "Recompression index, Cr",
                            "Estimated Value": "Pending",
                            "Unit": "-",
                            "Reference No.": "-",
                            "Notes": "Correlation to be added",
                        },
                        {
                            "Parameter": "Secondary compression index, Cα",
                            "Estimated Value": "Pending",
                            "Unit": "-",
                            "Reference No.": "-",
                            "Notes": "Correlation to be added",
                        },
                        {
                            "Parameter": "Coefficient of consolidation, Cv",
                            "Estimated Value": "Pending",
                            "Unit": "m²/year" if unit_system == "SI" else "ft²/year",
                            "Reference No.": "-",
                            "Notes": "Correlation to be added",
                        },
                    ]
                )

                    if rock_type != "Not applicable":
                    rock_er = get_rock_elastic_modulus_reference(
                        rock_type=rock_type,
                        unit_system=unit_system,
                    )

                    spt_results.extend(
                        [
                            {
              {
                "Parameter": "Rock elastic modulus, ER - minimum",
                "Estimated Value": format_engineering_value(
                    rock_er["er_min"],
                    unit_system,
                    rock_er["unit"],
                ),
                "Unit": rock_er["unit"],
                "Reference No.": "R-1",
                "Notes": f"{rock_type}; intact rock reference value",
            },
            {
                "Parameter": "Rock elastic modulus, ER - mean",
                "Estimated Value": format_engineering_value(
                    rock_er["er_mean"],
                    unit_system,
                    rock_er["unit"],
                ),
                "Unit": rock_er["unit"],
                "Reference No.": "R-1",
                "Notes": f"{rock_type}; n = {rock_er['number_of_values']}",
            },
            {
                "Parameter": "Rock elastic modulus, ER - maximum",
                "Estimated Value": format_engineering_value(
                    rock_er["er_max"],
                    unit_system,
                    rock_er["unit"],
                ),
                "Unit": rock_er["unit"],
                "Reference No.": "R-1",
                "Notes": f"{rock_type}; intact rock reference value",
            },
            {
                "Parameter": "Rock elastic modulus, ER - standard deviation",
                "Estimated Value": format_engineering_value(
                    rock_er["er_standard_deviation"],
                    unit_system,
                    rock_er["unit"],
                ),
                "Unit": rock_er["unit"],
                "Reference No.": "R-1",
                "Notes": "Statistical standard deviation from source table",
            },
                        ]
                    ) 
                st.dataframe(
                    spt_results,
                    use_container_width=True,
                    hide_index=True,
                )

        with st.expander("Equations and References", expanded=False):
            st.markdown(
                """
                **SPT-1. Energy and equipment correction**

                \\[
                N_{60} = N \\times C_E \\times C_B \\times C_R \\times C_S
                \\]

                **SPT-2. Overburden correction**

                \\[
                (N_1)_{60} = C_N \\times N_{60}
                \\]

                where:

                \\[
                C_N = \\sqrt{\\frac{P_a}{\\sigma'_{v0}}}
                \\]

                with an upper limit currently set in the code.

                Additional soil parameter correlations will be added after you provide the equations, tables, and references.
                """
            )
