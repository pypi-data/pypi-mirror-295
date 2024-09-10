# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import os
import unittest
import tempfile
from shutil import rmtree, move
import numpy as np

import qtealeaves as qtl
from qtealeaves import modeling
from qtealeaves.models import get_quantum_ising_1d, get_bose_hubbard_1d
from qtealeaves.operators import TNOperators, TNCombinedOperators
from qtealeaves.tensors import set_block_size_qteatensors, TensorBackend
from qtealeaves.emulator import MPS, TTN


class TestsTNsimulation(unittest.TestCase):
    def setUp(self):
        """
        Provide some default settings.
        """
        np.random.seed([11, 13, 17, 19])

        self.conv = qtl.convergence_parameters.TNConvergenceParameters(
            max_bond_dimension=16, cut_ratio=1e-16, max_iter=10
        )
        self.ansatz = {5: "TTN", 6: "MPS"}
        self.ansatz_type = {5: TTN, 6: MPS}

        self.temp_dir = tempfile.TemporaryDirectory()
        self.in_folder = os.path.join(self.temp_dir.name, "INPUT")
        self.out_folder = os.path.join(self.temp_dir.name, "OUTPUT")

        self.qtea_timelimit_intrasweep_checkpoints = (
            qtl.simulation.tn_simulation.QTEA_TIMELIMIT_INTRASWEEP_CHECKPOINTS
        )

    def tearDown(self):
        """
        Remove input and output folders again
        """
        self.temp_dir.cleanup()

        qtl.simulation.tn_simulation.QTEA_TIMELIMIT_INTRASWEEP_CHECKPOINTS = (
            self.qtea_timelimit_intrasweep_checkpoints
        )

        return

    def run_model(self, model, my_ops, my_obs, params=None):
        """
        Run TTN simulation and test results for ising model or similar.
        """
        params = {} if params is None else params

        for tn_type in self.ansatz.keys():
            in_folder = self.in_folder + f"TN{tn_type}"
            out_folder = self.out_folder + f"TN{tn_type}"

            simulation = qtl.QuantumGreenTeaSimulation(
                model,
                my_ops,
                self.conv,
                my_obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            for elem in [
                {
                    "L": 8,
                    "J": 0.0,
                    "g": -1,
                }
            ]:
                elem.update(params)
                jj = elem["J"]
                simulation.run(elem)
                results = simulation.get_static_obs(elem)
                prefix = f"For ansatz {self.ansatz[tn_type]} "
                msg = prefix + f"Energy vs energy via system size for J={jj} is wrong."
                self.assertAlmostEqual(results["energy"], -elem["L"], msg=msg)
                for ii in range(elem["L"]):
                    self.assertAlmostEqual(
                        results["sz"][ii], -1, msg=prefix + f"Sz for J={jj} is wrong"
                    )

                energy_0 = np.linalg.eigh(model.build_ham(my_ops, elem))[0][0]

                msg = prefix + f"Energy vs energy via ED for J={jj} is wrong."
                self.assertAlmostEqual(results["energy"], energy_0, msg=msg)

    def test_ising(self):
        """
        Testing Ising with TTNs
        """
        model, my_ops = get_quantum_ising_1d()

        my_obs = qtl.observables.TNObservables(num_trajectories=3)
        my_obs += qtl.observables.TNObsLocal("sz", "sz")

        self.run_model(model, my_ops, my_obs)

    def test_almost_non_binary_tree_ising(self):
        """
        Testing Ising with non-binary TTNs, i.e. 7 sites instead of 8
        """
        model, my_ops = get_quantum_ising_1d()

        my_obs = qtl.observables.TNObservables(num_trajectories=3)
        my_obs += qtl.observables.TNObsLocal("sz", "sz")

        self.run_model(model, my_ops, my_obs, {"L": 7})

    def test_spinglass_1(self):
        """
        Testing spinglass with TTNs. In this first test, the random couplings
        are set to 1, in order to retrieve the same results of test_ising.
        """
        model_name = lambda params: "Spinglass_g%2.4f" % (params["g"])

        # test if we get the same results of ising by setting
        # the coupling to one
        get_zrand = lambda params: np.ones(params["L"])
        get_xrand = lambda params: np.ones((params["L"], params["L"]))

        model = modeling.QuantumModel(1, "L", name=model_name)
        model += modeling.RandomizedLocalTerm(
            "sz", get_zrand, strength="g", prefactor=-1
        )
        model += modeling.TwoBodyAllToAllTerm1D(
            ["sx", "sx"], get_xrand, strength="J", prefactor=-1
        )

        my_ops = qtl.operators.TNSpin12Operators()
        my_obs = qtl.observables.TNObservables()
        my_obs += qtl.observables.TNObsLocal("sz", "sz")

        self.run_model(model, my_ops, my_obs)

    def test_spinglass_2(self):
        """
        Testing spinglass with TTNs. In the second test, the energy with
        random couplings is compared with the result of exact diagonalization.
        """
        model_name = lambda params: "Spinglass"

        rvec = np.random.rand(8)
        rmat = np.random.rand(8, 8)

        def get_rvec(params, rvec=rvec):
            return rvec

        def get_rmat(params, rmat=rmat):
            return rmat

        get_zrand = get_rvec
        get_xrand = get_rmat

        model = modeling.QuantumModel(1, "L", name=model_name)
        model += modeling.RandomizedLocalTerm("sz", get_zrand, prefactor=-1)
        model += modeling.TwoBodyAllToAllTerm1D(["sx", "sx"], get_xrand, prefactor=-1)

        my_ops = qtl.operators.TNSpin12Operators()
        my_obs = qtl.observables.TNObservables()

        for tn_type in self.ansatz.keys():
            in_folder = self.in_folder + f"TN{tn_type}"
            out_folder = self.out_folder + f"TN{tn_type}"

            simulation = qtl.QuantumGreenTeaSimulation(
                model,
                my_ops,
                self.conv,
                my_obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            for elem in [
                {
                    "L": 8,
                }
            ]:
                energy_0 = np.linalg.eigh(model.build_ham(my_ops, elem))[0][0]
                simulation.run(elem)
                results = simulation.get_static_obs(elem)

                prefix = f"For ansatz {self.ansatz[tn_type]} "
                self.assertAlmostEqual(
                    results["energy"], energy_0, msg=prefix + f"Energy is wrong"
                )

    def test_operator_sets(self):
        """Test the operator set by combining Ising and Hubbard model."""

        # Reduce bond dimension and iterations for runtime
        self.conv.max_iter = 4
        self.conv.sim_params["max_bond_dimension"] = 8

        model_a, ops_a = get_quantum_ising_1d()
        obs_a = qtl.observables.TNObservables()

        model_b, ops_b = get_bose_hubbard_1d()
        obs_b = qtl.observables.TNObservables()

        def mask_a(params):
            mask_a = np.ones(16, dtype=bool)
            mask_a[8:] = False
            return mask_a

        def mask_b(params):
            mask_b = np.ones(16, dtype=bool)
            mask_b[:8] = False
            return mask_b

        def mask_c(params):
            mask_c = np.ones(16, dtype=bool)
            mask_c[7:] = False
            return mask_c

        def mapping_func(site_idx):
            if site_idx < 8:
                return "A"

            return "B"

        ops_c = TNOperators(set_names=["A", "B"], mapping_func=mapping_func)
        for key, value in ops_a.items():
            ops_c[("A", key[1])] = value
        for key, value in ops_b.items():
            ops_c[("B", key[1])] = value

        model_c = modeling.QuantumModel(1, 16)
        model_c += modeling.LocalTerm("sz", strength="g", prefactor=-1, mask=mask_a)
        model_c += modeling.TwoBodyTerm1D(
            ["sx", "sx"], 1, strength="J", prefactor=-1, mask=mask_c
        )
        model_c += modeling.LocalTerm("nint", strength="U", mask=mask_b)
        model_c += modeling.TwoBodyTerm1D(
            ["bdagger", "b"], 1, strength="Jb", prefactor=-1, mask=mask_b
        )
        model_c += modeling.TwoBodyTerm1D(
            ["b", "bdagger"], 1, strength="Jb", prefactor=-1, mask=mask_b
        )
        obs_c = qtl.observables.TNObservables()
        obs_c += qtl.observables.TNObsLocal("<1>", "id")
        obs_c += qtl.observables.TNObsCorr("<11>", ["id", "id"])

        for tn_type in self.ansatz.keys():
            in_folder = self.in_folder + f"TN{tn_type}_a"
            out_folder = self.out_folder + f"TN{tn_type}_a"

            simulation = qtl.QuantumGreenTeaSimulation(
                model_a,
                ops_a,
                self.conv,
                obs_a,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            elem = {"L": 8, "g": 0.5, "J": 1.0}
            simulation.run(elem)
            results_a = simulation.get_static_obs(elem)

            # --------------------------------------------------------

            in_folder = self.in_folder + f"TN{tn_type}_b"
            out_folder = self.out_folder + f"TN{tn_type}_b"

            simulation = qtl.QuantumGreenTeaSimulation(
                model_b,
                ops_b,
                self.conv,
                obs_b,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            elem = {"L": 8, "U": 0.5, "J": 1.0}
            simulation.run(elem)
            results_b = simulation.get_static_obs(elem)

            # --------------------------------------------------------

            in_folder = self.in_folder + f"TN{tn_type}_c"
            out_folder = self.out_folder + f"TN{tn_type}_c"

            simulation = qtl.QuantumGreenTeaSimulation(
                model_c,
                ops_c,
                self.conv,
                obs_c,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            elem = {"g": 0.5, "J": 1.0, "Jb": 1.0, "U": 0.5}
            simulation.run(elem)
            results_c = simulation.get_static_obs(elem)

            # --------------------------------------------------------

            en_a = results_a["energy"]
            en_b = results_b["energy"]
            en_c = results_c["energy"]

            # Digits can be improved with increasing bond dimension at
            # the cost of a longer runtime of the unittest
            digits = 1 if tn_type in [5] else 2
            self.assertAlmostEqual(
                en_a + en_b, en_c, digits, msg=f"Mismatch energy in ansatz {tn_type}."
            )

    def base_checkpoints_statics(self, intrasweep=False, mid_sweep=False, max_iter=3):
        """Base test for statics checkpoints."""
        model, my_ops = get_quantum_ising_1d()

        my_obs = qtl.observables.TNObservables()
        my_obs += qtl.observables.TNObsLocal("sz", "sz")

        if intrasweep:
            qtl.simulation.tn_simulation.QTEA_TIMELIMIT_INTRASWEEP_CHECKPOINTS = 0

        for tn_type in self.ansatz.keys():
            self.conv.max_iter = max_iter - 1

            in_folder = self.in_folder + f"TN{tn_type}"
            out_folder = self.out_folder + f"TN{tn_type}"

            if tn_type in [5]:
                sweep_order_short = [(1, 3), (1, 2), (1, 1), (1, 0), (0, 0)]
            elif tn_type in [6]:
                sweep_order_short = [0, 1, 2, 3]
            else:
                raise Exception("Define short sweep order for unit test.")

            simulation = qtl.QuantumGreenTeaSimulation(
                model,
                my_ops,
                self.conv,
                my_obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            params = [
                {
                    "L": 8,
                    "J": 0.0,
                    "g": -1,
                }
            ]

            if mid_sweep:
                params[0]["sweep_order"] = sweep_order_short
                params[0]["exclude_from_hash"] = ["sweep_order", "exclude_from_hash"]

            sim_status = simulation.status(params)
            self.assertEqual(
                sim_status, (1, 0, 0), msg=f"Failed for TN {tn_type} & not started."
            )

            for elem in params:
                simulation.run(elem)

            # Reset conv params iterations and remove file tracking finished
            # simulations
            self.conv.max_iter = max_iter
            finished_json = os.path.join(out_folder, "has_finished.json")
            os.remove(finished_json)
            if mid_sweep:
                del params[0]["sweep_order"]
                del params[0]["exclude_from_hash"]

            sim_status = simulation.status(params)
            self.assertEqual(
                sim_status, (0, 1, 0), msg=f"Failed for TN {tn_type} & interrupted."
            )

            for elem in params:
                simulation.run(elem)

            sim_status = simulation.status(params)
            self.assertEqual(
                sim_status, (0, 0, 1), msg=f"Failed for TN {tn_type} & finished."
            )

    def test_checkpoints_statics(self):
        """Test the checkpoints of statics at end of sweep."""
        self.base_checkpoints_statics()

    def test_checkpoints_statics_intrasweep(self):
        """Test the checkpoints of statics intrasweep."""
        self.base_checkpoints_statics(intrasweep=True)

    def test_checkpoints_statics_intrasweep_midsweep(self):
        """Test the checkpoints of statics intrasweep and midsweep."""
        self.base_checkpoints_statics(intrasweep=True, mid_sweep=True, max_iter=2)

    def base_checkpoints_statics_results_preserved(self):
        """Test that rerunning a finished simulation does not change the statics results."""
        model, my_ops = get_quantum_ising_1d()

        my_obs = qtl.observables.TNObservables()
        my_obs += qtl.observables.TNObsLocal("<z>", "sz")

        for tn_type in self.ansatz.keys():
            # We want to be sure the ground state converges before
            # reaching the maximum number of iterations.
            self.conv.max_iter = 200

            in_folder = self.in_folder + f"TN{tn_type}"
            out_folder = self.out_folder + f"TN{tn_type}"

            simulation = qtl.QuantumGreenTeaSimulation(
                model,
                my_ops,
                self.conv,
                my_obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            params = [
                {
                    "L": 8,
                    "J": 0.0,
                    "g": -1,
                }
            ]

            simulation.run(params)
            results = simulation.get_static_obs(params[0])
            energy_a = results["energy"]
            meas_sz_a = list(results["<z>"])

            # Check that output file is not re-generated
            # ..........................................

            out_file = os.path.join(out_folder, "static_obs.dat")
            tmp_file = os.path.join(out_folder, "static_obs2.dat")
            move(out_file, tmp_file)

            simulation.run(params)
            try:
                results = simulation.get_static_obs(params[0])
                raise Exception(
                    "Expecting to load checkpoint without re-running the measurement. "
                    "The measurement file was removed by hand, but could be read now. "
                    "Thus, error because file with static obs results rewritten after "
                    "converging."
                )
            except FileNotFoundError:
                pass

            move(tmp_file, out_file)

            # Check that output is still the same
            # ...................................

            simulation.run(params)
            results = simulation.get_static_obs(params[0])
            energy_b = results["energy"]
            meas_sz_b = list(results["<z>"])

            # They must actual be equal, not just to numerical precision
            self.assertEqual(energy_a, energy_b)
            self.assertEqual(meas_sz_a, meas_sz_b)

    def test_checkpoints_statics_results_preserved(self):
        """Test that rerunning a finished simulation does not change the statics results."""
        self.base_checkpoints_statics_results_preserved()

    def test_checkpoints_statics_intrasweep_results_preserved(self):
        """
        Test that rerunning a finished simulation does not change the
        statics results (intrasweep checkpoints present).
        """
        qtl.simulation.tn_simulation.QTEA_TIMELIMIT_INTRASWEEP_CHECKPOINTS = 0
        self.base_checkpoints_statics_results_preserved()

    def test_checkpoints_dynamics(self):
        """Test the checkpoints of a dynamics simulation."""
        model, my_ops = get_quantum_ising_1d()

        my_obs = qtl.observables.TNObservables()
        my_obs += qtl.observables.TNObsLocal("sz", "sz")

        # Dynamics
        quench = qtl.DynamicsQuench(
            "t_grid", measurement_period=2, time_evolution_mode=1
        )
        quench["g"] = lambda tt, params: 2.0 - 2.0 * (tt / 10.0)

        for tn_type in self.ansatz.keys():
            in_folder = self.in_folder + f"TN{tn_type}"
            out_folder = self.out_folder + f"TN{tn_type}"

            simulation = qtl.QuantumGreenTeaSimulation(
                model,
                my_ops,
                self.conv,
                my_obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            params = []
            params.append(
                {
                    "L": 8,
                    "J": 1.0,
                    "g": 2.0,
                    "t_grid": [0.05] * 4,
                    "Quenches": [quench],
                    "exclude_from_hash": ["Quenches", "t_grid"],
                }
            )

            sim_status = simulation.status(params)
            self.assertEqual(
                sim_status, (1, 0, 0), msg=f"Failed for TN {tn_type} & not started."
            )

            simulation.run(params)

            # Prepare restart
            params[0]["t_grid"] = [0.05] * 6
            finished_json = os.path.join(out_folder, "has_finished.json")
            os.remove(finished_json)

            sim_status = simulation.status(params)
            self.assertEqual(
                sim_status, (0, 1, 0), msg=f"Failed for TN {tn_type} & interrupted."
            )

            simulation.run(params)

            sim_status = simulation.status(params)
            self.assertEqual(
                sim_status, (0, 0, 1), msg=f"Failed for TN {tn_type} & finished."
            )

    def test_dynamics_measurement_period(self):
        """Test the measurement period of a dynamics simulation."""
        model, my_ops = get_quantum_ising_1d()

        my_obs = qtl.observables.TNObservables()
        my_obs += qtl.observables.TNObsLocal("sz", "sz")

        # Dynamics
        quench = qtl.DynamicsQuench(
            "t_grid", measurement_period=2, time_evolution_mode=1
        )
        quench["g"] = lambda tt, params: 2.0 - 2.0 * (tt / 10.0)

        for tn_type in self.ansatz.keys():
            in_folder = self.in_folder + f"TN{tn_type}"
            out_folder = self.out_folder + f"TN{tn_type}"

            simulation = qtl.QuantumGreenTeaSimulation(
                model,
                my_ops,
                self.conv,
                my_obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            params = []
            params.append(
                {
                    "L": 8,
                    "J": 1.0,
                    "g": 2.0,
                    "t_grid": [0.05] * 5,
                    "Quenches": [quench],
                    "exclude_from_hash": ["Quenches", "t_grid"],
                }
            )

            simulation.run(params)
            results = simulation.get_dynamic_obs(params[0])
            self.assertEqual(3, len(results[0]))
            for elem in results[0]:
                self.assertTrue(elem is not None)

            quench.measurement_period = 1
            results = simulation.get_dynamic_obs(params[0])
            for ii, elem in enumerate(results[0]):
                if ii in [0, 2]:
                    self.assertTrue(elem is None)
                else:
                    self.assertTrue(elem is not None)

            # Testing multiple ansaetze, have to reset
            quench.measurement_period = 2

    def base_qtea_block_size(
        self, chi_user, chi_block, chi_max, data_type, block_size, set_via_byte
    ):
        """Test if we can sucessfully set hardware specific value to be respected."""

        self.conv.max_iter = 1
        self.conv.sim_params["max_bond_dimension"] = chi_user
        self.conv.ini_bond_dimension = chi_user
        self.conv.sim_params["data_type"] = data_type

        if set_via_byte:
            set_block_size_qteatensors(block_size_byte=block_size)
        else:
            set_block_size_qteatensors(block_size_bond_dimension=block_size)

        model, ops = get_quantum_ising_1d()

        for tn_type in self.ansatz.keys():
            in_folder = self.in_folder + f"TN{tn_type}"
            out_folder = self.out_folder + f"TN{tn_type}"

            obs = qtl.observables.TNObservables()
            psi_file = os.path.join(in_folder, "psi")
            obs += qtl.observables.TNState2File(psi_file, "F")

            simulation = qtl.QuantumGreenTeaSimulation(
                model,
                ops,
                self.conv,
                obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
                store_checkpoints=False,
            )

            elem = {"L": 16, "g": 0.5, "J": 1.0}
            simulation.run(elem, delete_existing_folder=True)
            results = simulation.get_static_obs(elem)

            psi_file_path = results[psi_file]
            state = self.ansatz_type[tn_type].read(psi_file_path, TensorBackend())

            # Select on tensor which is good to test (ansatz specific)
            if tn_type in [5]:
                tensor = state[0][1]
                chis = list(tensor.shape)
            elif tn_type in [6]:
                tensor = state[3]
                chis = [tensor.shape[0], tensor.shape[2]]

            for chi_now in chis:
                msg = f"Chi={chi_now} is not a multiple of {chi_block} for ansatz {tn_type}."
                self.assertEqual(chi_now % chi_block, 0, msg=msg)

                msg = f"Detected chi={chi_now} for ansatz {tn_type}."
                self.assertFalse(chi_now > chi_max, msg=msg)

    def test_qtea_block_size_bond_dimension(self):
        """Test if we can sucessfully set hardware specific value to be respected via chi."""
        self.base_qtea_block_size(3, 4, 4, "S", 4, False)
        self.base_qtea_block_size(3, 4, 4, "D", 4, False)
        self.base_qtea_block_size(3, 4, 4, "Z", 4, False)

        self.base_qtea_block_size(5, 4, 8, "S", 4, False)
        self.base_qtea_block_size(5, 4, 8, "D", 4, False)
        self.base_qtea_block_size(5, 4, 8, "Z", 4, False)

        self.base_qtea_block_size(5, 8, 8, "S", 8, False)
        self.base_qtea_block_size(5, 8, 8, "D", 8, False)
        self.base_qtea_block_size(5, 8, 8, "Z", 8, False)

    def test_qtea_block_size_byte(self):
        """Test if we can sucessfully set hardware specific value to be respected via bytes."""
        self.base_qtea_block_size(3, 4, 4, "S", 16, True)
        self.base_qtea_block_size(3, 4, 4, "D", 32, True)
        self.base_qtea_block_size(3, 4, 4, "Z", 64, True)

        self.base_qtea_block_size(5, 4, 8, "S", 16, True)
        self.base_qtea_block_size(5, 4, 8, "D", 32, True)
        self.base_qtea_block_size(5, 4, 8, "Z", 64, True)

        self.base_qtea_block_size(5, 8, 8, "S", 32, True)
        self.base_qtea_block_size(5, 8, 8, "D", 64, True)
        self.base_qtea_block_size(5, 8, 8, "Z", 128, True)

    def test_combined_operators(self):
        """Test if the combined operator work in a simulation."""
        self.conv.max_iter = 5
        self.conv.sim_params["max_bond_dimension"] = 16

        model, my_ops = get_quantum_ising_1d()

        my_cops = TNCombinedOperators(my_ops, my_ops)

        cmodel = modeling.QuantumModel(1, "L")
        cmodel += modeling.LocalTerm("sz.id", strength="g", prefactor=-1)
        cmodel += modeling.LocalTerm("id.sz", strength="g", prefactor=-1)
        cmodel += modeling.LocalTerm("sx.sx", strength="J", prefactor=-1)
        cmodel += modeling.TwoBodyTerm1D(
            ["id.sx", "sx.id"], shift=1, strength="J", prefactor=-1
        )

        my_obs = qtl.observables.TNObservables()

        for tn_type in self.ansatz.keys():
            # ------------------------------------------------------------------
            # Simulation without combined operators

            in_folder = self.in_folder + f"TN{tn_type}"
            out_folder = self.out_folder + f"TN{tn_type}"

            simulation = qtl.QuantumGreenTeaSimulation(
                model,
                my_ops,
                self.conv,
                my_obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            params = {"L": 16, "g": 0.5, "J": 1.0}
            simulation.run(params)
            results = simulation.get_static_obs(params)
            energy = results["energy"]

            # ------------------------------------------------------------------
            # Simulation with combined operators

            in_folder = self.in_folder + f"TN{tn_type}_c"
            out_folder = self.out_folder + f"TN{tn_type}_c"

            simulation = qtl.QuantumGreenTeaSimulation(
                cmodel,
                my_cops,
                self.conv,
                my_obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
            )

            params = {"L": 8, "g": 0.5, "J": 1.0}
            simulation.run(params)
            results = simulation.get_static_obs(params)
            energy_c = results["energy"]

            # ------------------------------------------------------------------
            # Test we get the same energy

            self.assertAlmostEqual(energy, energy_c, 3)

    def base_skip_exact_rgtensors(self, tn_type, obs):
        """Base routine for skip exact RG tensors returning results and reference."""
        self.conv.sim_params["max_bond_dimension"] = 5
        self.conv.ini_bond_dimension = 5

        model, ops = get_quantum_ising_1d()

        results_list = []
        for skip_exact_rg in [False, True]:
            self.conv.sim_params["skip_exact_rg_tensors"] = skip_exact_rg

            in_folder = self.in_folder + f"TN{skip_exact_rg}"
            out_folder = self.out_folder + f"TN{skip_exact_rg}"

            simulation = qtl.QuantumGreenTeaSimulation(
                model,
                ops,
                self.conv,
                obs,
                tn_type=tn_type,
                tensor_backend=2,
                folder_name_input=in_folder,
                folder_name_output=out_folder,
                has_log_file=True,
                store_checkpoints=False,
            )

            elem = {"L": 8, "g": 0.5, "J": 1.0}
            simulation.run(elem, delete_existing_folder=True)
            results = simulation.get_static_obs(elem)
            results_list.append(results)

        return results_list[0], results_list[1]

    def test_skip_exact_rgtensors(self):
        """Test the skip exact rg tensor feature."""
        obs = qtl.observables.TNObservables()
        obs += qtl.observables.TNObsLocal("sz", "sz")

        for tn_type in self.ansatz.keys():
            ref, res = self.base_skip_exact_rgtensors(tn_type, obs)

            msg = "Energy with skip_exact_rgtensors failed."
            self.assertAlmostEqual(res["energy"], ref["energy"], 5, msg=msg)

            eps = np.max(np.abs(res["sz"] - ref["sz"]))
            msg = "Local measurement with skip_exact_rgtensors failed."
            self.assertAlmostEqual(eps, 0, 5, msg=msg)

    def test_skip_exact_rgtensors_correlation(self):
        """Test the skip exact rg tensor feature."""
        obs = qtl.observables.TNObservables()
        obs += qtl.observables.TNObsCorr("zz", ["sz", "sz"])

        for tn_type in self.ansatz.keys():
            ref, res = self.base_skip_exact_rgtensors(tn_type, obs)

            msg = "Energy with skip_exact_rgtensors failed."
            self.assertAlmostEqual(res["energy"], ref["energy"], 5, msg=msg)

            eps = np.max(np.abs(res["zz"] - ref["zz"]))
            msg = "Local measurement with skip_exact_rgtensors failed."
            self.assertAlmostEqual(eps, 0, 5, msg=msg)

    def test_skip_exact_rgtensors_bond_entropy(self):
        """Test the skip exact rg tensor feature."""
        obs_list = []

        obs = qtl.observables.TNObservables()
        obs += qtl.observables.TNObsBondEntropy()
        obs_list.append(obs)

        obs = qtl.observables.TNObservables()
        obs += qtl.observables.TNObsBondEntropy()
        obs += qtl.observables.TNObsCorr("zz", ["sz", "sz"])
        obs_list.append(obs)

        for obs in obs_list:
            for tn_type in self.ansatz.keys():
                ref, res = self.base_skip_exact_rgtensors(tn_type, obs)

                msg = "Energy with skip_exact_rgtensors failed."
                self.assertAlmostEqual(res["energy"], ref["energy"], 5, msg=msg)

                for key in ref["bond_entropy0"].keys():
                    eps = np.max(
                        np.abs(res["bond_entropy0"][key] - ref["bond_entropy0"][key])
                    )
                    msg = f"Bond entropy {key} with skip_exact_rgtensors failed."
                    self.assertAlmostEqual(eps, 0, 5, msg=msg)

    def test_parameterized_convergence_parameters(self):
        """Test if we can parameterize convergence parameters."""
        model, my_ops = get_quantum_ising_1d()

        my_obs = qtl.observables.TNObservables(num_trajectories=3)
        my_obs += qtl.observables.TNObsLocal("sz", "sz")

        self.conv = qtl.convergence_parameters.TNConvergenceParameters(
            max_bond_dimension="chi",
            cut_ratio="cut_ratio",
            max_iter="max_iter",
        )

        params = {"chi": 4, "cut_ratio": 0.1, "max_iter": 2}
        self.run_model(model, my_ops, my_obs, params=params)
