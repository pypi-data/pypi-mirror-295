#   #!/usr/bin/env python
#   -*- coding: utf-8 -*-
#   ******************************************************************************
#     Copyright (c) 2023.
#     Developed by Yifei Lu
#     Last change on 1/4/23, 4:13 PM
#     Last change by yifei
#    *****************************************************************************
import thermo
from scipy.constants import bar, atm

print(thermo.__version__)

thermo.GCEOSMIX

print(thermo.Mixture.eos)
thermo.Mixture.eos = thermo.PRMIX
thermo.Mixture.eos_in_a_box.append(thermo.Mixture.eos)
print(thermo.Mixture.eos)
print(thermo.Mixture.eos_in_a_box)

gas_mix = thermo.Mixture(T=300, P=50*bar, zs={"methane": 0.9, "hydrogen": 0.1})

# print(gas_mix.eos)

print(gas_mix.Z)

print(gas_mix.Vmg)

# print(gas_mix.VolumeGasMixture(T=gas_mix.T, P=gas_mix.P, zs=gas_mix.ys, ws=gas_mix.wsg))
