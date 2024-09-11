#   #!/usr/bin/env python
#   -*- coding: utf-8 -*-
#   ******************************************************************************
#     Copyright (c) 2024.
#     Developed by Yifei Lu
#     Last change on 8/21/24, 11:12 AM
#     Last change by yifei
#    *****************************************************************************

# **********************************************************************************************************************
# This script contains a comprehensive set of unit tests designed to validate the functionalities and calculations
# within the GasNetSim components. The tests primarily focus on the GasMixtureGERG2008 class found in the gas_mixture
# module of GasNetSim. These tests aim to ensure accurate and reliable performance of critical methods related to gas
# mixture properties and calculations.

# The script includes test cases for various functions within the GasMixtureGERG2008 class, such as the hyperbolic
# tangent, hyperbolic sine, and hyperbolic cosine functions, as well as methods like CalculateHeatingValue,
# ConvertCompositionGERG, MolarMassGERG, PressureGERG, DensityGERG, Alpha0GERG, ReducingParametersGERG,
# PropertiesGERG, PseudoCriticalPointGERG, and AlpharGERG.

# Each test is designed to assert the correctness and consistency of calculations involved in determining properties
# like heating value, molar mass, pressure, density, ideal gas Helmholtz energy, reducing parameters,
# pseudo-critical point, and residual Helmholtz energy.
# **********************************************************************************************************************

from scipy.constants import bar
from numpy.testing import assert_almost_equal, assert_allclose
from GasNetSim.components.gas_mixture.GERG2008 import *


def test_heating_value_100iter():
    """
    Test the numba version of the CalculateHeatingValue function of GasMixtureGERG2008 class.
    """
    for _ in range(100):
        # Generate random composition with sum equal to 1
        random_b = np.random.dirichlet(np.ones(21), size=1)[0]
        #print(random_b, sum(random_b))

        # Create the NIST gas mixture dictionary
        nist_gas_mixture = {}
        a = ['methane', 'nitrogen', 'carbon dioxide', 'ethane', 'propane', 'isobutane',
             'butane', 'isopentane', 'pentane', 'hexane', 'heptane', 'octane', 'nonane',
             'decane', 'hydrogen', 'oxygen', 'carbon monoxide', 'water', 'hydrogen sulfide',
             'helium', 'argon']

        for _i in range(21):
            nist_gas_mixture[a[_i]] = random_b[_i]

        gerg_composition = convert_to_gerg2008_composition(nist_gas_mixture)

        # Create an instance of the GasMixtureGERG2008 class with the random gas mixture
        gas_mixture = GasMixtureGERG2008(500 * bar, 400, gerg_composition, use_numba=False)

        # Test the CalculateHeatingValue function
        expected_heating_value = gas_mixture.CalculateHeatingValue(comp=gerg_composition, hhv=True, parameter="volume")
        molarmass = gas_mixture.MolarMass
        molardensity = gas_mixture.MolarDensity
        calculated_heating_value = CalculateHeatingValue_numba(MolarMass=molarmass, MolarDensity=molardensity, comp=gerg_composition, hhv=True, parameter="volume")

        # assert_almost_equal(calculated_heating_value, expected_heating_value, decimal=5)
        np.testing.assert_allclose(calculated_heating_value, expected_heating_value, rtol=1e-5)


# def test_convert_composition_gerg_100iter():
#     """
#     Test the numba version of the ConvertCompositionGERG method of GasMixtureGERG2008 class.
#     """
#     for _ in range(100):
#         # Generate random composition with sum equal to 1
#         random_b = np.random.dirichlet(np.ones(21), size=1)[0]
#         #print(random_b, sum(random_b))
#
#         # Create the NIST gas mixture dictionary
#         nist_gas_mixture = {}
#
#         a = ['methane', 'nitrogen', 'carbon dioxide', 'ethane', 'propane', 'isobutane',
#              'butane', 'isopentane', 'pentane', 'hexane', 'heptane', 'octane', 'nonane',
#              'decane', 'hydrogen', 'oxygen', 'carbon monoxide', 'water', 'hydrogen sulfide',
#              'helium', 'argon']
#         for ii in range(21):
#             nist_gas_mixture[a[ii]] = random_b[ii]
#
#         gerg_gas_composition = convert_to_gerg2008_composition(nist_gas_mixture)
#
#         # Create an instance of the GasMixtureGERG2008 class with the NIST gas mixture
#         gas_mixture = GasMixtureGERG2008(500 * bar, 400, gerg_gas_composition, use_numba=False)
#
#         # Test the ConvertCompositionGERG function
#         expected_result = gas_mixture.x[1:]
#
#         # Calculate the converted composition using ConvertCompositionGERG method
#         converted_composition = CovertCompositionGERG_numba(nist_gas_mixture)
#         assert_almost_equal(converted_composition, expected_result)


def test_molarmass_gerg_100iter():
    """
        Test the numba version of the MolarMassGERG method of GasMixtureGERG2008 class.
    """
    for _ in range(100):
        # Generate random composition with sum equal to 1
        random_b = np.random.dirichlet(np.ones(21), size=1)[0]
        #print(random_b, sum(random_b))

        # Create the NIST gas mixture dictionary
        nist_gas_mixture = {}
        a = ['methane', 'nitrogen', 'carbon dioxide', 'ethane', 'propane', 'isobutane',
             'butane', 'isopentane', 'pentane', 'hexane', 'heptane', 'octane', 'nonane',
             'decane', 'hydrogen', 'oxygen', 'carbon monoxide', 'water', 'hydrogen sulfide',
             'helium', 'argon']

        for ii in range(21):
            nist_gas_mixture[a[ii]] = random_b[ii]

        gerg_gas_composition = convert_to_gerg2008_composition(nist_gas_mixture)

        # Create an instance of the GasMixtureGERG2008 class with the NIST gas mixture
        gas_mixture = GasMixtureGERG2008(500 * bar, 400, gerg_gas_composition, use_numba=False)

        # Calculate the expected molar mass manually based on the given mixture
        expected_molar_mass = gas_mixture.MolarMassGERG()

        # Get the calculated molar mass from the MolarMassGERG method
        calculated_molar_mass = MolarMassGERG_numba(random_b)
        assert_almost_equal(expected_molar_mass, calculated_molar_mass)


def test_pressure_gerg_100iter():
    """
        Test the numba version of the PressureGERG method of GasMixtureGERG2008 class.
    """
    for iter in range(100):
        # Create the NIST gas mixture dictionary
        nist_gas_mixture = {}
        a = ['methane', 'nitrogen', 'carbon dioxide', 'ethane', 'propane', 'isobutane',
             'butane', 'isopentane', 'pentane', 'hexane', 'heptane', 'octane', 'nonane',
             'decane', 'hydrogen', 'oxygen', 'carbon monoxide', 'water', 'hydrogen sulfide',
             'helium', 'argon']
        random_b = np.random.dirichlet(np.ones(21), size=1)[0]
        for _i in range(21):
            nist_gas_mixture[a[_i]] = random_b[_i]

        gerg_composition = convert_to_gerg2008_composition(nist_gas_mixture)

        # Create an instance of the GasMixtureGERG2008 class with the NIST gas mixture
        gas_mixture = GasMixtureGERG2008(500 * bar, 400, gerg_composition, use_numba=False)

        # Define the density input for PressureGERG method
        #d = 10
        _, _, d = DensityGERG_numba(P=gas_mixture.P, T=gas_mixture.T, x=random_b, iFlag=0)

        # Calculate the expected pressure using an example formula or method
        expected_values = gas_mixture.PressureGERG(d)

        Temp = gas_mixture.T
        AR = np.array(gas_mixture.AlpharGERG(itau=0, idelta=0, D=d))
        # Call the PressureGERG method with the given diameter
        calculated_values = PressureGERG_numba(Temp, d, random_b)
        assert_almost_equal(expected_values, calculated_values)


def test_alpha0_gerg_100iter():
    """
        Test the numba version of the Alpha0GERG() function of GasMixtureGERG2008 class.
    """
    for _ in range(100):
        # Generate random composition with sum equal to 1
        random_b = np.random.dirichlet(np.ones(21), size=1)[0]
        #print(random_b, sum(random_b))

        # Create the NIST gas mixture dictionary
        nist_gas_mixture = {}
        a = ['methane', 'nitrogen', 'carbon dioxide', 'ethane', 'propane', 'isobutane',
             'butane', 'isopentane', 'pentane', 'hexane', 'heptane', 'octane', 'nonane',
             'decane', 'hydrogen', 'oxygen', 'carbon monoxide', 'water', 'hydrogen sulfide',
             'helium', 'argon']
        for ii in range(21):
            nist_gas_mixture[a[ii]] = random_b[ii]

        gerg_composition = convert_to_gerg2008_composition(nist_gas_mixture)

        # Create an instance of the GasMixtureGERG2008 class with the NIST gas mixture
        gas_mixture = GasMixtureGERG2008(500 * bar, 400, gerg_composition, use_numba=False)

        # Expected value calculated from the function call
        # a0(0) - Ideal gas Helmholtz energy (all dimensionless [i.e., divided by RT])
        # a0(1) - tau*partial(a0)/partial(tau)
        # a0(2) - tau^2*partial^2(a0)/partial(tau)^2
        expected_alpha0 = gas_mixture.Alpha0GERG()

        Temp = gas_mixture.T
        MolarDensity = gas_mixture.MolarDensity
        X = random_b

        # Call the Alpha0GERG function
        actual_alpha0 = Alpha0GERG_numba(Temp, MolarDensity, X)
        assert_almost_equal(actual_alpha0, expected_alpha0)


def test_reducing_parameters_gerg_100iter():
    """
        Test the numba version of the ReducingParametersGERG() function of GasMixtureGERG2008 class.
    """
    for _ in range(100):
        # Generate random composition with sum equal to 1
        random_b = np.random.dirichlet(np.ones(21), size=1)[0]
        #print(random_b, sum(random_b))

        # Create the NIST gas mixture dictionary
        nist_gas_mixture = {}
        a = ['methane', 'nitrogen', 'carbon dioxide', 'ethane', 'propane', 'isobutane',
             'butane', 'isopentane', 'pentane', 'hexane', 'heptane', 'octane', 'nonane',
             'decane', 'hydrogen', 'oxygen', 'carbon monoxide', 'water', 'hydrogen sulfide',
             'helium', 'argon']

        for ii in range(21):
            nist_gas_mixture[a[ii]] = random_b[ii]

        gerg_composition = convert_to_gerg2008_composition(nist_gas_mixture)

        # Create an instance of the GasMixtureGERG2008 class with the NIST gas mixture
        gas_mixture = GasMixtureGERG2008(500 * bar, 400, gerg_composition, use_numba=False)

        # Expected value calculated from the function call
        expected_reducingparametersgerg = gas_mixture.ReducingParametersGERG()

        # Call the ReducingParametersGERG function
        # Tr - Reducing temperature(K)
        # Dr - Reducing density(mol / l)
        actual_reducingparametersgerg = ReducingParametersGERG_numba(random_b)
        assert_almost_equal(actual_reducingparametersgerg, expected_reducingparametersgerg)


def test_pseudo_critical_point_gerg_100iter():
    """
            Test the numba version of the PseudoCriticalPointGERG() function of GasMixtureGERG2008 class.
    """
    for _ in range(100):
        # Generate random composition with sum equal to 1
        random_b = np.random.dirichlet(np.ones(21), size=1)[0]
        #print(random_b, sum(random_b))

        # Create the NIST gas mixture dictionary
        nist_gas_mixture = {}
        a = ['methane', 'nitrogen', 'carbon dioxide', 'ethane', 'propane', 'isobutane',
             'butane', 'isopentane', 'pentane', 'hexane', 'heptane', 'octane', 'nonane',
             'decane', 'hydrogen', 'oxygen', 'carbon monoxide', 'water', 'hydrogen sulfide',
             'helium', 'argon']

        for ii in range(21):
            nist_gas_mixture[a[ii]] = random_b[ii]

        gerg_composition = convert_to_gerg2008_composition(nist_gas_mixture)

        # Create an instance of the GasMixtureGERG2008 class with the NIST gas mixture
        gas_mixture = GasMixtureGERG2008(500 * bar, 400, gerg_composition, use_numba=False)

        # Expected value calculated from the function call
        expected_pseudocriticalpointgerg = gas_mixture.PseudoCriticalPointGERG()

        # Call the ReducingParametersGERG function
        actual_pseudocriticalpointgerg = PseudoCriticalPointGERG_numba(random_b)
        assert_allclose(actual_pseudocriticalpointgerg, expected_pseudocriticalpointgerg)


def test_alphar_gerg_100iter():
    """
            Test the numba version of the AlpharGERG() function of GasMixtureGERG2008 class.
    """
    for iter in range(100):
        # Generate random composition with sum equal to 1
        random_b = np.random.dirichlet(np.ones(21), size=1)[0]
        #print(random_b, sum(random_b))

        # Create the NIST gas mixture dictionary
        nist_gas_mixture = {}
        a = ['methane', 'nitrogen', 'carbon dioxide', 'ethane', 'propane', 'isobutane',
             'butane', 'isopentane', 'pentane', 'hexane', 'heptane', 'octane', 'nonane',
             'decane', 'hydrogen', 'oxygen', 'carbon monoxide', 'water', 'hydrogen sulfide',
             'helium', 'argon']
        b = np.array([0.77824, 0.02, 0.06, 0.08, 0.03, 0.0015, 0.003, 0.0005, 0.00165, 0.00215, 0.00088, 0.00024, 0.00015, 0.00009,
             0.004, 0.005, 0.002, 0.0001, 0.0025, 0.007, 0.001])
        for ii in range(21):
            nist_gas_mixture[a[ii]] = random_b[ii]

        gerg_composition = convert_to_gerg2008_composition(nist_gas_mixture)

        # Create an instance of the GasMixtureGERG2008 class with the NIST gas mixture
        gas_mixture = GasMixtureGERG2008(500 * bar, 400, gerg_composition, use_numba=False)

        # Expected value calculated from the function call
        #                         ar(0,0) - Residual Helmholtz energy (dimensionless, =a/RT)
        #                         ar(0,1) -     delta*partial  (ar)/partial(delta)
        #                         ar(0,2) -   delta^2*partial^2(ar)/partial(delta)^2
        #                         ar(0,3) -   delta^3*partial^3(ar)/partial(delta)^3
        #                         ar(1,0) -       tau*partial  (ar)/partial(tau)
        #                         ar(1,1) - tau*delta*partial^2(ar)/partial(tau)/partial(delta)
        #                         ar(2,0) -     tau^2*partial^2(ar)/partial(tau)^2

        #D = 15.03402741629294
        _, _, D = DensityGERG_numba(P=gas_mixture.P, T=gas_mixture.T, x=random_b, iFlag=0)

        expected_alphargerg = gas_mixture.AlpharGERG(1, 0, D)

        Temp = gas_mixture.T

        # Call the ReducingParametersGERG function
        actual_alphargerg = AlpharGERG_numba(Temp, random_b, 1, 0, D)

        assert_almost_equal(actual_alphargerg, expected_alphargerg)


def test_co2_emission():
    """
    Test the numba version of the CalculateHeatingValue function of GasMixtureGERG2008 class.
    """
    # Generate random composition with sum equal to 1
    random_b = np.random.dirichlet(np.ones(21), size=1)[0]

    # Create the NIST gas mixture dictionary
    nist_gas_mixture = {}
    a = ['methane', 'nitrogen', 'carbon dioxide', 'ethane', 'propane', 'isobutane',
         'butane', 'isopentane', 'pentane', 'hexane', 'heptane', 'octane', 'nonane',
         'decane', 'hydrogen', 'oxygen', 'carbon monoxide', 'water', 'hydrogen sulfide',
         'helium', 'argon']

    for _i in range(21):
        nist_gas_mixture[a[_i]] = random_b[_i]

    gerg_composition = convert_to_gerg2008_composition(nist_gas_mixture)

    # Create an instance of the GasMixtureGERG2008 class with the NIST gas mixture
    gas_mixture = GasMixtureGERG2008(500 * bar, 400, gerg_composition, use_numba=False)

    molarmass = gas_mixture.MolarMass

    co2_emission_factor = CalculateCO2Emission_numba(MolarMass=molarmass, x=random_b)
