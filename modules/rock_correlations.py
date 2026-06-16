ROCK_ELASTIC_MODULUS_TABLE_USCS = {
    "Granite": {
        "number_of_values": 26,
        "number_of_rock_types": 26,
        "er_max_ksi_x_1000": 14.5,
        "er_min_ksi_x_1000": 0.93,
        "er_mean_ksi_x_1000": 7.64,
        "standard_deviation_ksi_x_1000": 3.55,
    },
    "Diorite": {
        "number_of_values": 3,
        "number_of_rock_types": 3,
        "er_max_ksi_x_1000": 16.2,
        "er_min_ksi_x_1000": 2.48,
        "er_mean_ksi_x_1000": 7.45,
        "standard_deviation_ksi_x_1000": 6.19,
    },
    "Gabbro": {
        "number_of_values": 3,
        "number_of_rock_types": 3,
        "er_max_ksi_x_1000": 12.2,
        "er_min_ksi_x_1000": 9.8,
        "er_mean_ksi_x_1000": 11.0,
        "standard_deviation_ksi_x_1000": 0.97,
    },
    "Diabase": {
        "number_of_values": 7,
        "number_of_rock_types": 7,
        "er_max_ksi_x_1000": 15.1,
        "er_min_ksi_x_1000": 10.0,
        "er_mean_ksi_x_1000": 12.8,
        "standard_deviation_ksi_x_1000": 1.78,
    },
    "Basalt": {
        "number_of_values": 12,
        "number_of_rock_types": 12,
        "er_max_ksi_x_1000": 12.2,
        "er_min_ksi_x_1000": 4.20,
        "er_mean_ksi_x_1000": 8.14,
        "standard_deviation_ksi_x_1000": 2.60,
    },
    "Quartzite": {
        "number_of_values": 7,
        "number_of_rock_types": 7,
        "er_max_ksi_x_1000": 12.8,
        "er_min_ksi_x_1000": 5.29,
        "er_mean_ksi_x_1000": 9.59,
        "standard_deviation_ksi_x_1000": 2.32,
    },
    "Marble": {
        "number_of_values": 14,
        "number_of_rock_types": 13,
        "er_max_ksi_x_1000": 10.7,
        "er_min_ksi_x_1000": 0.58,
        "er_mean_ksi_x_1000": 6.18,
        "standard_deviation_ksi_x_1000": 2.49,
    },
    "Gneiss": {
        "number_of_values": 13,
        "number_of_rock_types": 13,
        "er_max_ksi_x_1000": 11.9,
        "er_min_ksi_x_1000": 4.13,
        "er_mean_ksi_x_1000": 8.86,
        "standard_deviation_ksi_x_1000": 2.31,
    },
    "Slate": {
        "number_of_values": 11,
        "number_of_rock_types": 2,
        "er_max_ksi_x_1000": 3.79,
        "er_min_ksi_x_1000": 0.35,
        "er_mean_ksi_x_1000": 1.39,
        "standard_deviation_ksi_x_1000": 0.96,
    },
    "Schist": {
        "number_of_values": 13,
        "number_of_rock_types": 12,
        "er_max_ksi_x_1000": 10.0,
        "er_min_ksi_x_1000": 0.86,
        "er_mean_ksi_x_1000": 4.97,
        "standard_deviation_ksi_x_1000": 3.18,
    },
    "Phyllite": {
        "number_of_values": 3,
        "number_of_rock_types": 3,
        "er_max_ksi_x_1000": 2.51,
        "er_min_ksi_x_1000": 1.25,
        "er_mean_ksi_x_1000": 1.71,
        "standard_deviation_ksi_x_1000": 0.57,
    },
    "Sandstone": {
        "number_of_values": 27,
        "number_of_rock_types": 19,
        "er_max_ksi_x_1000": 5.68,
        "er_min_ksi_x_1000": 0.09,
        "er_mean_ksi_x_1000": 2.13,
        "standard_deviation_ksi_x_1000": 1.19,
    },
    "Siltstone": {
        "number_of_values": 5,
        "number_of_rock_types": 5,
        "er_max_ksi_x_1000": 4.76,
        "er_min_ksi_x_1000": 0.38,
        "er_mean_ksi_x_1000": 2.39,
        "standard_deviation_ksi_x_1000": 1.65,
    },
    "Shale": {
        "number_of_values": 30,
        "number_of_rock_types": 14,
        "er_max_ksi_x_1000": 5.60,
        "er_min_ksi_x_1000": 0.001,
        "er_mean_ksi_x_1000": 1.42,
        "standard_deviation_ksi_x_1000": 1.45,
    },
    "Limestone": {
        "number_of_values": 30,
        "number_of_rock_types": 30,
        "er_max_ksi_x_1000": 13.0,
        "er_min_ksi_x_1000": 0.65,
        "er_mean_ksi_x_1000": 5.7,
        "standard_deviation_ksi_x_1000": 3.73,
    },
    "Dolostone": {
        "number_of_values": 17,
        "number_of_rock_types": 16,
        "er_max_ksi_x_1000": 11.4,
        "er_min_ksi_x_1000": 0.83,
        "er_mean_ksi_x_1000": 4.22,
        "standard_deviation_ksi_x_1000": 3.44,
    },
}


def get_rock_types() -> list[str]:
    return list(ROCK_ELASTIC_MODULUS_TABLE_USCS.keys())


def ksi_x_1000_to_ksf(value: float) -> float:
    """
    Convert elastic modulus from ksi x 1000 to ksf.

    1 ksi = 144 ksf
    Therefore, 1 ksi x 1000 = 144,000 ksf.
    """
    return value * 1000.0 * 144.0


def ksi_x_1000_to_gpa(value: float) -> float:
    """
    Convert elastic modulus from ksi x 1000 to GPa.

    1 ksi = 0.006894757 GPa
    Therefore, 1 ksi x 1000 = 6.894757 GPa.
    """
    return value * 1000.0 * 0.006894757


def get_rock_elastic_modulus_reference(rock_type: str, unit_system: str) -> dict:
    """
    Return max, min, mean, and standard deviation of intact rock elastic modulus.

    Source table units are ksi x 1000.
    USCS app output is ksf.
    SI app output is kPa.
    """
    if rock_type not in ROCK_ELASTIC_MODULUS_TABLE_USCS:
        raise ValueError(f"Unsupported rock type: {rock_type}")

    data = ROCK_ELASTIC_MODULUS_TABLE_USCS[rock_type]

    if unit_system == "USCS":
        conversion = ksi_x_1000_to_ksf
        unit = "ksf"
    elif unit_system == "SI":
        conversion = ksi_x_1000_to_gpa
        unit = "GPa"
    else:
        raise ValueError("unit_system must be either 'USCS' or 'SI'.")

    return {
        "rock_type": rock_type,
        "er_max": conversion(data["er_max_ksi_x_1000"]),
        "er_min": conversion(data["er_min_ksi_x_1000"]),
        "er_mean": conversion(data["er_mean_ksi_x_1000"]),
        "er_standard_deviation": conversion(data["standard_deviation_ksi_x_1000"]),
        "unit": unit,
        "number_of_values": data["number_of_values"],
        "number_of_rock_types": data["number_of_rock_types"],
        "source_unit": "ksi x 1000",
    }
