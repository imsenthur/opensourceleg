import pytest

from opensourceleg.hardware import thermal

# Initializing the ThermalModel objects
test_model_default = thermal.ThermalModel()
test_model_specified = thermal.ThermalModel(
    ambient=10,
    temp_limit_windings=100,
    soft_border_C_windings=25,
    temp_limit_case=50,
    soft_border_C_case=10,
)


# Testing the ThermalModel constructor
@pytest.mark.parametrize(
    ("test_model", "class_variable", "expected_value"),
    [
        (test_model_default, "C_w", 0.20 * 81.46202695970649),
        (test_model_default, "R_WC", 1.0702867186480716),
        (test_model_default, "C_c", 512.249065845453),
        (test_model_default, "R_CA", 1.9406620046327363),
        (test_model_default, "α", 0.393 * 1 / 100),
        (test_model_default, "R_T_0", 65),
        (test_model_default, "T_w", 21),
        (test_model_default, "T_c", 21),
        (test_model_default, "T_a", 21),
        (test_model_default, "soft_max_temp_windings", 115 - 15),
        (test_model_default, "abs_max_temp_windings", 115),
        (test_model_default, "soft_border_windings", 15),
        (test_model_default, "soft_max_temp_case", 80 - 5),
        (test_model_default, "abs_max_temp_case", 80),
        (test_model_default, "soft_border_case", 5),
        (test_model_specified, "C_w", 0.20 * 81.46202695970649),
        (test_model_specified, "R_WC", 1.0702867186480716),
        (test_model_specified, "C_c", 512.249065845453),
        (test_model_specified, "R_CA", 1.9406620046327363),
        (test_model_specified, "α", 0.393 * 1 / 100),
        (test_model_specified, "R_T_0", 65),
        (test_model_specified, "T_w", 10),
        (test_model_specified, "T_c", 10),
        (test_model_specified, "T_a", 10),
        (test_model_specified, "soft_max_temp_windings", 100 - 25),
        (test_model_specified, "abs_max_temp_windings", 100),
        (test_model_specified, "soft_border_windings", 25),
        (test_model_specified, "soft_max_temp_case", 50 - 10),
        (test_model_specified, "abs_max_temp_case", 50),
        (test_model_specified, "soft_border_case", 10),
    ],
)
def test_init(test_model, class_variable, expected_value):
    """
    Tests the ThermalModel constructor\n
    Asserts the class variables of the ThermalModel object are equal to the expected values.
    """

    assert getattr(test_model, class_variable) == expected_value


def test_update():
    """
    Tests the ThermalModel update method\n
    Calls the update method with no arguments and asserts the class variables are equal to the expected values.
    Then calls the update method with a motor_current argument and asserts the class variables are equal to the expected values.
    This is repeated once more to test the update method with a motor_current argument.
    """

    # Testing the default ThermalModel update method with no args
    test_model_default.update()
    assert test_model_default.T_w == 21
    assert test_model_default.T_c == 21
    assert test_model_default.T_a == 21
    # Testing the default ThermalModel update method with motor_current arg
    test_model_default.update(motor_current=1000)
    default_T_w_update1 = (
        21
        + (
            ((1000 * 1e-3) ** 2)
            * 0.376
            * (1 + (0.393 * 1 / 100) * (21 - 65))
            / (16.292405391941298)
        )
        / 200
    )
    assert test_model_default.T_w == default_T_w_update1
    assert test_model_default.T_c == 21
    assert test_model_default.T_a == 21
    # Testing the default ThermalModel update method with motor_current arg once more
    test_model_default.update(motor_current=1000)
    default_T_w_update2 = (
        default_T_w_update1
        + (
            (
                ((1000 * 1e-3) ** 2)
                * 0.376
                * (1 + (0.393 * 1 / 100) * (default_T_w_update1 - 65))
                + (21 - default_T_w_update1) / 1.0702867186480716
            )
            / (16.292405391941298)
        )
        / 200
    )
    assert test_model_default.T_w == default_T_w_update2
    assert (
        test_model_default.T_c
        == (((default_T_w_update1 - 21) / 1.0702867186480716) / 512.249065845453)
        * 1
        / 200
        + 21
    )
    assert test_model_default.T_a == 21
