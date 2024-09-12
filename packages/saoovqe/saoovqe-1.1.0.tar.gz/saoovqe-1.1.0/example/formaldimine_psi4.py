#!/usr/bin/env python3
"""
Example script for utilization of SA-OO-VQE solver on the computation of
formaldimine (methylene imine) molecule
energies for the lowest 2 singlet states, gradients of the potential energy
surface and the corresponding non-adiabatic
couplings.
"""
import numpy as np
from qiskit_algorithms.optimizers import SciPyOptimizer
from qiskit.primitives import Estimator
import psi4

import saoovqe

R_BOHR_ANG = 0.5291772105638411


def gen_formaldimine_geom_psi4(alpha, phi):
    """
    Function to generate an .xyz file for formaldimine, aligns N-C bond with
    the z-axis.
    """
    variables = [1.498047, 1.066797, 0.987109, 118.359375] + [alpha, phi]
    string_geo_dum = """0 1
                    N
                    C 1 {0}
                    H 2 {1}  1 {3}
                    H 2 {1}  1 {3} 3 180
                    H 1 {2}  2 {4} 3 {5}
                    symmetry c1
                    """.format(*variables)

    psi4.core.set_output_file("output_Psi4.txt", False)
    molecule_dum = psi4.geometry(string_geo_dum)
    molecule_dum.translate(psi4.core.Vector3(-molecule_dum.x(0),
                                             -molecule_dum.y(0),
                                             -molecule_dum.z(0)))
    mol_geom_dum = np.copy(molecule_dum.geometry().np) * R_BOHR_ANG
    if not np.isclose(mol_geom_dum[1, 1], 0.):
        mol_geom_dum[:, [1, 2]] = mol_geom_dum[:, [2, 1]]
        mol_geom_dum[4, 0] = -mol_geom_dum[4, 0]
        print("switched axes, new geom:", mol_geom_dum)
    string_geo = ""
    for i in range(molecule_dum.natom()):
        string_geo += "  {:7s} {:12.9f} {:12.9f} {:12.9f}\n".format(
            molecule_dum.flabel(
                i), mol_geom_dum[i, 0], mol_geom_dum[i, 1], mol_geom_dum[i, 2])
    string_geo += "symmetry c1\n"
    string_geo += "nocom\n"
    string_geo += "noreorient\n"

    return string_geo


def gen_formaldimine_geom_sa_oo_vqe(alpha, phi):
    """
    Function to generate an .xyz file for formaldimine, aligns N-C bond with
    the z-axis.
    """
    variables = [1.498047, 1.066797, 0.987109, 118.359375] + [alpha, phi]
    string_geo_dum = """0 1
                    N
                    C 1 {0}
                    H 2 {1}  1 {3}
                    H 2 {1}  1 {3} 3 180
                    H 1 {2}  2 {4} 3 {5}
                    symmetry c1
                    """.format(*variables)

    psi4.core.set_output_file("output_Psi4.txt", False)
    molecule_dum = psi4.geometry(string_geo_dum)
    molecule_dum.translate(psi4.core.Vector3(-molecule_dum.x(0),
                                             -molecule_dum.y(0),
                                             -molecule_dum.z(0)))
    geometry_coordinate = np.copy(molecule_dum.geometry().np) * R_BOHR_ANG
    if not np.isclose(geometry_coordinate[1, 1], 0.):
        geometry_coordinate[:, [1, 2]] = geometry_coordinate[:, [2, 1]]
        geometry_coordinate[4, 0] = -geometry_coordinate[4, 0]
        print("switched axes, new geom:", geometry_coordinate)
    return [('N', geometry_coordinate[0]),
            ('C', geometry_coordinate[1]),
            ('H', geometry_coordinate[2]),
            ('H', geometry_coordinate[3]),
            ('H', geometry_coordinate[4])]


#######################
# Method specification
#######################
estimator = Estimator()

n_states = 2
repetitions = 1

#########################
# Molecule specification
#########################
alpha = 130
phi = 80
geometry = gen_formaldimine_geom_sa_oo_vqe(alpha, phi)
coords = [ list(geometry[e][1]) for e in range(5)]
sym = [ geometry[e][0] for e in range(5)]
n_orbs_active = 2
n_elec_active = 2
charge = 0
multiplicity = 1
basis = "sto-3g"

#########################################################

# Weights of the ensemble:
problem = saoovqe.ProblemSet(symbols=sym, coords=coords, charge=charge, multiplicity=multiplicity, n_electrons_active=n_elec_active,
                             n_orbitals_active=n_orbs_active, basis_name=basis)

# Step 1: Initialization - states |phiA>, |phiB>
initial_circuits = saoovqe.OrthogonalCircuitSet.from_problem_set(n_states,
                                                                 problem)

# Define the ansatz circuit:
#
# Operator Û(theta)
ansatz = saoovqe.Ansatz.from_problem_set(saoovqe.AnsatzType.GUCCSD,
                                         problem,
                                         repetitions,
                                         qubit_mapper=problem.fermionic_mapper)

# Perform SA-VQE procedure
saoovqe_solver = saoovqe.SAOOVQE(estimator,
                                 initial_circuits,
                                 ansatz,
                                 problem,
                                 orbital_optimization_settings={})

energies = saoovqe_solver.get_energy(
    SciPyOptimizer('SLSQP', options={'maxiter': 500, 'ftol': 1e-8}))

print('\n============== SA-OO-VQE Results ==============')
print(f'Optimized ansatz parameters: {saoovqe_solver.ansatz_param_values}')
print(f'Optimized (state-resolution) angle: {saoovqe_solver.resolution_angle}')
print(f'Energies: {energies}')


# print('\n============== Gradients ==============')
# for state_idx in range(2):
#     for atom_idx in range(len(geometry)):
#         print(state_idx, atom_idx, saoovqe_solver.eval_eng_gradient(
#         state_idx, atom_idx))
#
# print('\n============== Total non-adiabatic couplings ==============')
# for atom_idx in range(len(geometry)):
#     print(atom_idx, saoovqe_solver.eval_nac(atom_idx))
#
# print('\n============== CI non-adiabatic couplings ==============')
# for atom_idx in range(len(geometry)):
#     print(atom_idx, saoovqe_solver.ci_nacs[atom_idx])
#
# print('\n============== CSF non-adiabatic couplings ==============')
# for atom_idx in range(len(geometry)):
#     print(atom_idx, saoovqe_solver.csf_nacs[atom_idx])


# Compute using Psi4

def run_sacasscf_psi4(string_geo,
                      basisset,
                      n_mo_optimized,
                      active_indices,
                      frozen_indices,
                      virtual_indices,
                      num_roots=2,
                      d_conv=1e-6,
                      e_conv=1e-6):
    """
    Function to perform SA-CASSCF with psi4.
    """
    frozen_uocc = virtual_indices[-1] - n_mo_optimized + 1
    restricted_uocc = n_mo_optimized - \
                      (len(frozen_indices) + len(active_indices))

    options = {'basis': basisset,
               'DETCI_FREEZE_CORE': False,
               'reference': 'RHF',
               'scf_type': 'pk',
               # set e_convergence and d_convergence to 1e-8 instead of 1e-6
               'num_roots': num_roots,
               'frozen_docc': [0],
               'restricted_docc': [len(frozen_indices)],
               'active': [len(active_indices)],
               'restricted_uocc': [restricted_uocc],
               'frozen_uocc': [frozen_uocc],
               'MAXITER': 1000,
               'DIIS': False,
               'D_CONVERGENCE': d_conv,
               'E_CONVERGENCE': e_conv,
               'S': 0}

    if num_roots > 1:
        options['avg_states'] = [0, 1]
        options['avg_weights'] = [0.5, 0.5]

    psi4.geometry(string_geo)
    psi4.set_options(options)

    psi4.energy('scf', return_wfn=True)
    psi4.energy('casscf', return_wfn=True)

    if num_roots == 2:
        e0_sacasscf = psi4.variable('CI ROOT 0 TOTAL ENERGY')
        e1_sacasscf = psi4.variable('CI ROOT 1 TOTAL ENERGY')

        return e0_sacasscf, e1_sacasscf
    else:
        e_casscf = psi4.variable('CI TOTAL ENERGY')
        return e_casscf


E0_psi4, E1_psi4 = run_sacasscf_psi4(string_geo=problem.geometry_str,
                                     basisset=basis,
                                     n_mo_optimized=saoovqe_solver.n_mo_optim,
                                     active_indices=problem.active_orbitals,
                                     frozen_indices=problem.frozen_orbitals_indices,
                                     virtual_indices=problem.virtual_orbitals_indices)

# Gradients dE/dalpha
delta = 1e-5
geom_plus = gen_formaldimine_geom_psi4(alpha=alpha + (delta / 2), phi=phi)
geom_minus = gen_formaldimine_geom_psi4(alpha=alpha - (delta / 2), phi=phi)
E0_psi4_p, E1_psi4_p = run_sacasscf_psi4(string_geo=geom_plus, basisset=basis,
                                         n_mo_optimized=saoovqe_solver.n_mo_optim,
                                         active_indices=problem.active_orbitals,
                                         frozen_indices=problem.frozen_orbitals_indices,
                                         virtual_indices=problem.virtual_orbitals_indices)
E0_psi4_m, E1_psi4_m = run_sacasscf_psi4(string_geo=geom_minus, basisset=basis,
                                         n_mo_optimized=saoovqe_solver.n_mo_optim,
                                         active_indices=problem.active_orbitals,
                                         frozen_indices=problem.frozen_orbitals_indices,
                                         virtual_indices=problem.virtual_orbitals_indices)

grad_de_da_0 = (E0_psi4_p - E0_psi4_m) / delta
grad_de_da_1 = (E1_psi4_p - E1_psi4_m) / delta


# Transform sa-oo-vqe gradients to spherical coordinates
def grad_vec_to_spherical(vector, R, phi, alpha):
    phi_rad = np.deg2rad(phi)
    alpha_rad = np.deg2rad(alpha)
    v_R = -(vector[0] * np.sin(phi_rad) * np.sin(alpha_rad)) - (
            vector[1] * np.cos(phi_rad) * np.sin(alpha_rad)) + (
                  vector[2] * np.cos(alpha_rad))
    v_phi = -(vector[0] * R * np.cos(phi_rad) * np.sin(alpha_rad)) + (
            vector[1] * R * np.sin(phi_rad) * np.sin(alpha_rad))
    v_alpha = -(vector[0] * R * np.sin(phi_rad) * np.cos(alpha_rad)) - (
            vector[1] * R * np.cos(phi_rad) * np.cos(alpha_rad)) - (
                      vector[2] * R * np.sin(alpha_rad))
    v_R_deg = v_R / (180 / np.pi)
    v_phi_deg = v_phi / (180 / np.pi)
    v_alpha_deg = v_alpha / (180 / np.pi)

    return v_R_deg, v_phi_deg, v_alpha_deg


dE_0dx, dE_0dy, dE_0dz = saoovqe_solver.eval_eng_gradient(0, 4)
dE_1dx, dE_1dy, dE_1dz = saoovqe_solver.eval_eng_gradient(1, 4)
bond_length = np.sqrt(
    geometry[4][1][0] ** 2. + geometry[4][1][1] ** 2. + geometry[4][1][
        2] ** 2.)
print(f'bond length: {bond_length}')
dE_0dR, dE_0dphi, dE_0dalpha = grad_vec_to_spherical([dE_0dx, dE_0dy, dE_0dz],
                                                     bond_length, phi, alpha)
dE_1dR, dE_1dphi, dE_1dalpha = grad_vec_to_spherical([dE_1dx, dE_1dy, dE_1dz],
                                                     bond_length, phi, alpha)

# Compare the results
print('saoovqe engs')
print(energies)

print('psi4 energies')
print(E0_psi4)
print(E1_psi4)

print("dE_0/da")
print(f'Psi4: {grad_de_da_0}')
print(f'SA-OO-VQE: {dE_0dalpha}')
print("dE_1/da")
print(f'Psi4: {grad_de_da_1}')
print(f'SA-OO-VQE: {dE_1dalpha}')
