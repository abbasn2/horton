#!/usr/bin/env python
"""Provide info for regression tester after running compare.py.

It is assumed that you run the compare script as follows:

    ./data/examples/hf_compare/compare.py data/test/helium_hf_sto3g.fchk > compare.log

The the regression tester can be called with:

    horton-regression-test.py data/examples/hf_compare/compare_rt.py
"""

with open('compare.log') as f:
    lines = f.readlines()
horton_energy = float(lines[2].split()[2])


# CODE BELOW IS FOR horton-regression-test.py ONLY. IT IS NOT PART OF THE EXAMPLE.
rt_results = {'horton_energy': horton_energy}
# BEGIN AUTOGENERATED CODE. DO NOT CHANGE MANUALLY.
rt_previous = {
    'horton_energy': -2.8077839566,
}
