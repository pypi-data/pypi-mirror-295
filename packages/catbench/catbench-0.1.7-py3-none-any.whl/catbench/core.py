from ase.optimize import LBFGS
import os
import pickle
import json
import time
from copy import deepcopy
from ase.constraints import FixAtoms
import numpy as np
from ase.io import read, write
import requests
import json
import io
import copy
import os
from ase.io import read
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
import traceback

GRAPHQL = "http://api.catalysis-hub.org/graphql"


def convert_trajectory(filename):
    images = read(filename, index=":")
    os.remove(filename)
    write(filename, images, format="extxyz")


def energy_cal_gas(calculator, atoms_origin, F_CRIT_RELAX):
    atoms = deepcopy(atoms_origin)
    atoms.calc = calculator
    cell_size = [10, 10, 10]
    atoms.set_cell(cell_size)
    atoms.center()
    atomic_numbers = atoms.get_atomic_numbers()
    max_atomic_number = np.max(atomic_numbers)
    max_atomic_number_indices = [
        i for i, num in enumerate(atomic_numbers) if num == max_atomic_number
    ]
    fixed_atom_index = np.random.choice(max_atomic_number_indices)
    c = FixAtoms(indices=[fixed_atom_index])
    atoms.set_constraint(c)
    tags = np.ones(len(atoms))
    atoms.set_tags(tags)
    opt = LBFGS(atoms)
    opt.run(fmax=F_CRIT_RELAX, steps=2000)

    return atoms, atoms.get_potential_energy()


def energy_cal(
    calculator,
    atoms_origin,
    F_CRIT_RELAX,
    N_CRIT_RELAX,
    damping,
    z_target,
    logfile="",
    filename="",
):
    atoms = deepcopy(atoms_origin)
    atoms.calc = calculator
    tags = np.ones(len(atoms))
    atoms.set_tags(tags)
    if z_target != 0:
        atoms.set_constraint(fixatom(atoms, z_target))

    if logfile == "no":
        opt = LBFGS(atoms, logfile=None, damping=damping)
        opt.run(fmax=F_CRIT_RELAX, steps=N_CRIT_RELAX)
        elapsed_time = 0
    else:
        time_init = time.time()
        logfile = open(logfile, "w", buffering=1)
        logfile.write("######################\n")
        logfile.write("##  NNP relax starts  ##\n")
        logfile.write("######################\n")
        logfile.write("\nStep 1. Relaxing\n")
        opt = LBFGS(atoms, logfile=logfile, trajectory=filename, damping=damping)
        opt.run(fmax=F_CRIT_RELAX, steps=N_CRIT_RELAX)
        convert_trajectory(filename)
        logfile.write("Done!\n")
        elapsed_time = time.time() - time_init
        logfile.write(f"\nElapsed time: {elapsed_time} s\n\n")
        logfile.write("###############################\n")
        logfile.write("##  Relax terminated normally  ##\n")
        logfile.write("###############################\n")
        logfile.close()

    return atoms.get_potential_energy(), opt.nsteps, atoms, elapsed_time


def fixatom(atoms, z_target):
    indices_to_fix = [atom.index for atom in atoms if atom.position[2] < z_target]
    const = FixAtoms(indices=indices_to_fix)
    return const


def calc_displacement(atoms1, atoms2):
    positions1 = atoms1.get_positions()
    positions2 = atoms2.get_positions()
    displacements = positions2 - positions1
    displacement_magnitudes = np.linalg.norm(displacements, axis=1)
    max_displacement = np.max(displacement_magnitudes)
    return max_displacement


def find_median_index(arr):
    orig_arr = deepcopy(arr)
    sorted_arr = sorted(arr)
    length = len(sorted_arr)
    median_index = (length - 1) // 2
    median_value = sorted_arr[median_index]
    for i, num in enumerate(orig_arr):
        if num == median_value:
            return i, median_value


def fix_z(atoms, rate_fix):
    if rate_fix:
        z_max = max(atoms.positions[:, 2])
        z_min = min(atoms.positions[:, 2])
        z_target = z_min + rate_fix * (z_max - z_min)

        return z_target

    else:
        return 0


def process_output(dataset_name, coeff_setting):
    for dirpath, dirnames, filenames in os.walk(dataset_name):
        # OSZICAR와 CONTCAR 파일이 모두 있는지 확인합니다.
        if "OSZICAR" in filenames and "CONTCAR" in filenames:
            # 해당 폴더 내의 모든 파일을 순회합니다.
            for file in filenames:
                # 파일 이름이 OSZICAR 또는 CONTCAR가 아니라면 삭제합니다.
                if file not in ["OSZICAR", "CONTCAR"]:  # , "coeff.json"]:
                    file_path = os.path.join(dirpath, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

            rxn_name = dirpath.split("/")[2]

            not_calc_dirs = [
                name
                for name in os.listdir(f"{dataset_name}/gas")
                if os.path.isdir(os.path.join(f"{dataset_name}/gas", name))
            ] + ["slab"]

            if rxn_name not in not_calc_dirs:
                coeff = coeff_setting[rxn_name]
            else:
                coeff = {}

            coeff_path = os.path.join(dirpath, "coeff.json")
            if not os.path.exists(coeff_path) and coeff != {}:
                with open(coeff_path, "w") as json_file:
                    json.dump(coeff, json_file, indent=4)

    for dir_name in os.listdir(dataset_name):
        dir_path = os.path.join(dataset_name, dir_name)
        if os.path.isdir(dir_path) and dir_name != "gas":
            slab_folder_path = os.path.join(dir_path, "slab")
            os.makedirs(slab_folder_path, exist_ok=True)


def vasp2pkl(dataset_name):
    save_directory = os.path.join(os.getcwd(), "raw_data")
    os.makedirs(save_directory, exist_ok=True)
    path_output = os.path.join(os.getcwd(), f"raw_data/{dataset_name}.pkl")
    data_total = {}
    tags = []
    not_calc_dirs = [
        name
        for name in os.listdir(f"{dataset_name}/gas")
        if os.path.isdir(os.path.join(f"{dataset_name}/gas", name))
    ] + ["slab"]

    for dirpath, dirnames, filenames in os.walk(dataset_name):
        if "OSZICAR" in filenames and "CONTCAR" in filenames:
            rxn_name = dirpath.split("/")[2]
            if rxn_name not in not_calc_dirs:
                input = {}
                slab_name = dirpath.split("/")[1]
                slab_path = dirpath[: dirpath.find("/", dirpath.find("/") + 1)]

                coeff_path = os.path.join(dirpath, "coeff.json")
                with open(coeff_path, "r") as file:
                    coeff = json.load(file)

                tag = slab_name + "_" + rxn_name

                if tag in tags:
                    count = tags.count(tag)
                    tags.append(tag)
                    tag = f"{tag}_{count}"
                else:
                    tags.append(tag)

                input["star"] = {
                    "stoi": coeff["slab"],
                    "atoms": read(f"{slab_path}/slab/CONTCAR"),
                    "energy_cathub": read_E0_from_OSZICAR(f"{slab_path}/slab/OSZICAR"),
                }

                input[f"{rxn_name}star"] = {
                    "stoi": coeff["adslab"],
                    "atoms": read(f"{dirpath}/CONTCAR"),
                    "energy_cathub": read_E0_from_OSZICAR(f"{dirpath}/OSZICAR"),
                }

                for key in coeff:
                    if key not in ["slab", "adslab"]:
                        input[key] = {
                            "stoi": coeff[key],
                            "atoms": read(f"{dataset_name}/gas/{key}/CONTCAR"),
                            "energy_cathub": read_E0_from_OSZICAR(
                                f"{dataset_name}/gas/{key}/OSZICAR"
                            ),
                        }

                energy_check = 0
                for structure in input:
                    energy_check += (
                        input[structure]["energy_cathub"] * input[structure]["stoi"]
                    )

                data_total[tag] = {}

                data_total[tag]["raw"] = input
                data_total[tag]["cathub_energy"] = energy_check

    print(f"# of reactions : {len(data_total)}")

    with open(path_output, "wb") as file:
        pickle.dump(data_total, file)


def read_E0_from_OSZICAR(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            last_line = lines[-1]

        # 'E0=' 다음의 값을 추출
        energy = None
        for word in last_line.split():
            if word == "E0=":
                energy_index = last_line.split().index(word) + 1
                energy = last_line.split()[energy_index]
                energy = float(energy)
                break

        if energy is None:
            raise ValueError(f"Energy value not found in file: {file_path}")

        return energy

    except Exception as e:
        raise RuntimeError(
            f"An error occurred while reading the file '{file_path}': {str(e)}"
        )


def execute_benchmark(calculators, **kwargs):
    required_keys = ["NNP_name", "benchmark"]

    if not isinstance(calculators, list) or len(calculators) == 0:
        raise ValueError("Calculators must be a non-empty list.")

    for key in required_keys:
        if key not in kwargs:
            raise ValueError(f"Missing required keyword argument: {key}")

    NNP_name = kwargs["NNP_name"]
    benchmark = kwargs["benchmark"]
    F_CRIT_RELAX = kwargs.get("F_CRIT_RELAX", 0.05)
    N_CRIT_RELAX = kwargs.get("N_CRIT_RELAX", 999)
    rate = kwargs.get("rate", 0.5)
    disp_thrs_slab = kwargs.get("disp_thrs_slab", 1.0)
    disp_thrs_ads = kwargs.get("disp_thrs_ads", 1.5)
    again_seed = kwargs.get("again_seed", 0.2)
    damping = kwargs.get("damping", 1.0)

    path_pkl = os.path.join(os.getcwd(), f"raw_data/{benchmark}.pkl")

    with open(path_pkl, "rb") as file:
        cathub_data = pickle.load(file)

    save_directory = os.path.join(os.getcwd(), "result", NNP_name)
    print(f"Starting {NNP_name} Benchmarking")
    # Basic Settings==============================================================================
    os.makedirs(f"{save_directory}/traj", exist_ok=True)
    os.makedirs(f"{save_directory}/log", exist_ok=True)
    os.makedirs(f"{save_directory}/gases", exist_ok=True)

    final_result = {}

    final_outlier = {}
    final_outlier["Time"] = []
    final_outlier["normal"] = []
    final_outlier["outlier"] = []

    # Calculation Part==============================================================================

    accum_time = 0
    gas_energies = {}

    print("Starting calculations...")
    for index, key in enumerate(cathub_data):
        print(f"[{index+1}/{len(cathub_data)}] {key}")
        final_result[key] = {}
        final_result[key]["cathub"] = {}
        final_result[key]["cathub"]["ads_eng"] = cathub_data[key]["cathub_energy"]
        for structure in cathub_data[key]["raw"]:
            if "gas" not in str(structure):
                final_result[key]["cathub"][f"{structure}_abs"] = cathub_data[key][
                    "raw"
                ][structure]["energy_cathub"]
        final_result[key]["outliers"] = {
            "slab_conv": 0,
            "ads_conv": 0,
            "slab_move": 0,
            "ads_move": 0,
            "slab_seed": 0,
            "ads_seed": 0,
            "ads_eng_seed": 0,
        }

        trag_path = f"{save_directory}/traj/{key}"
        log_path = f"{save_directory}/log/{key}"

        os.makedirs(trag_path, exist_ok=True)
        os.makedirs(log_path, exist_ok=True)

        POSCAR_star = cathub_data[key]["raw"]["star"]["atoms"]
        z_target = fix_z(POSCAR_star, rate)

        informs = {}
        informs["ads_eng"] = []
        informs["slab_disp"] = []
        informs["ads_disp"] = []
        informs["slab_seed"] = []
        informs["ads_seed"] = []

        time_total_slab = 0
        time_total_ads = 0

        for i in range(len(calculators)):
            ads_energy_calc = 0
            for structure in cathub_data[key]["raw"]:
                if "gas" not in str(structure):
                    POSCAR_str = cathub_data[key]["raw"][structure]["atoms"]
                    (
                        energy_calculated,
                        steps_calculated,
                        CONTCAR_calculated,
                        time_calculated,
                    ) = energy_cal(
                        calculators[i],
                        POSCAR_str,
                        F_CRIT_RELAX,
                        N_CRIT_RELAX,
                        damping,
                        z_target,
                        f"{log_path}/{structure}_{i}.txt",
                        f"{trag_path}/{structure}_{i}",
                    )
                    ads_energy_calc += (
                        energy_calculated * cathub_data[key]["raw"][structure]["stoi"]
                    )
                    accum_time += time_calculated
                    if structure == "star":
                        slab_steps = steps_calculated
                        slab_displacement = calc_displacement(
                            POSCAR_str, CONTCAR_calculated
                        )
                        slab_energy = energy_calculated
                        slab_time = time_calculated
                        time_total_slab += time_calculated
                    else:
                        ads_step = steps_calculated
                        ads_displacement = calc_displacement(
                            POSCAR_str, CONTCAR_calculated
                        )
                        ads_energy = energy_calculated
                        ads_time = time_calculated
                        time_total_ads += time_calculated
                else:
                    gas_tag = f"{structure}_{i}th"
                    if gas_tag in gas_energies:
                        ads_energy_calc += (
                            gas_energies[gas_tag]
                            * cathub_data[key]["raw"][structure]["stoi"]
                        )
                    else:
                        print(f"{gas_tag} calculating")
                        gas_POSCAR, gas_energy = energy_cal_gas(
                            calculators[i],
                            cathub_data[key]["raw"][structure]["atoms"],
                            F_CRIT_RELAX,
                        )
                        gas_energies[gas_tag] = gas_energy
                        ads_energy_calc += (
                            gas_energy * cathub_data[key]["raw"][structure]["stoi"]
                        )
                        write(f"{save_directory}/gases/POSCAR_{gas_tag}", gas_POSCAR)

            if slab_steps == N_CRIT_RELAX:
                final_result[key]["outliers"]["slab_conv"] += 1

            if ads_step == N_CRIT_RELAX:
                final_result[key]["outliers"]["ads_conv"] += 1

            if slab_displacement > disp_thrs_slab:
                final_result[key]["outliers"]["slab_move"] += 1

            if ads_displacement > disp_thrs_ads:
                final_result[key]["outliers"]["ads_move"] += 1

            final_result[key][f"{i}"] = {
                "ads_eng": ads_energy_calc,
                "slab_abs": slab_energy,
                "ads_abs": ads_energy,
                "slab_disp": slab_displacement,
                "ads_disp": ads_displacement,
                "time_slab": slab_time,
                "time_ads": ads_time,
            }

            informs["ads_eng"].append(ads_energy_calc)
            informs["slab_disp"].append(slab_displacement)
            informs["ads_disp"].append(ads_displacement)
            informs["slab_seed"].append(slab_energy)
            informs["ads_seed"].append(ads_energy)

        ads_med_index, ads_med_eng = find_median_index(informs["ads_eng"])
        slab_seed_range = np.max(np.array(informs["slab_seed"])) - np.min(
            np.array(informs["slab_seed"])
        )
        ads_seed_range = np.max(np.array(informs["ads_seed"])) - np.min(
            np.array(informs["ads_seed"])
        )
        ads_eng_seed_range = np.max(np.array(informs["ads_eng"])) - np.min(
            np.array(informs["ads_eng"])
        )
        if slab_seed_range > again_seed:
            final_result[key]["outliers"]["slab_seed"] = 1
        if ads_seed_range > again_seed:
            final_result[key]["outliers"]["ads_seed"] = 1
        if ads_eng_seed_range > again_seed:
            final_result[key]["outliers"]["ads_eng_seed"] = 1

        final_result[key]["final"] = {
            "ads_eng_median": ads_med_eng,
            "median_num": ads_med_index,
            "slab_max_disp": np.max(np.array(informs["slab_disp"])),
            "ads_max_disp": np.max(np.array(informs["ads_disp"])),
            "slab_seed_range": slab_seed_range,
            "ads_seed_range": ads_seed_range,
            "ads_eng_seed_range": ads_eng_seed_range,
            "time_total_slab": time_total_slab,
            "time_total_ads": time_total_ads,
        }

        outlier_sum = sum(final_result[key]["outliers"].values())
        final_outlier["Time"] = accum_time

        if outlier_sum == 0:
            final_outlier["normal"].append(key)
        else:
            final_outlier["outlier"].append(key)

        with open(f"{save_directory}/{NNP_name}_result.json", "w") as file:
            json.dump(final_result, file, indent=4)

        with open(f"{save_directory}/{NNP_name}_outlier.json", "w") as file:
            json.dump(final_outlier, file, indent=4)

        with open(f"{save_directory}/{NNP_name}_gases.json", "w") as file:
            json.dump(gas_energies, file, indent=4)

    print(f"{NNP_name} Benchmarking Finish")


def fetch(query):
    return requests.get(GRAPHQL, {"query": query}).json()["data"]


def reactions_from_dataset(pub_id, page_size=40):
    reactions = []
    has_next_page = True
    start_cursor = ""
    page = 0
    while has_next_page:
        data = fetch(
            """{{
      reactions(pubId: "{pub_id}", first: {page_size}, after: "{start_cursor}") {{
        totalCount
        pageInfo {{
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }}
        edges {{
          node {{
            Equation
            reactants
            products
            reactionEnergy
            reactionSystems {{
              name
              systems {{
                energy
                InputFile(format: "json")
              }}
            }}
          }}
        }}
      }}
    }}""".format(
                start_cursor=start_cursor,
                page_size=page_size,
                pub_id=pub_id,
            )
        )
        has_next_page = data["reactions"]["pageInfo"]["hasNextPage"]
        start_cursor = data["reactions"]["pageInfo"]["endCursor"]
        page += 1
        print(
            has_next_page,
            start_cursor,
            page_size * page,
            data["reactions"]["totalCount"],
        )
        reactions.extend(map(lambda x: x["node"], data["reactions"]["edges"]))

    return reactions


def aseify_reactions(reactions):
    for i, reaction in enumerate(reactions):
        for j, _ in enumerate(reactions[i]["reactionSystems"]):
            system_info = reactions[i]["reactionSystems"][j].pop("systems")

            with io.StringIO() as tmp_file:
                tmp_file.write(system_info.pop("InputFile"))
                tmp_file.seek(0)
                atoms = read(tmp_file, format="json")
                atoms.pbc = True
                reactions[i]["reactionSystems"][j]["atoms"] = atoms

            reactions[i]["reactionSystems"][j]["energy"] = system_info["energy"]

        reactions[i]["reactionSystems"] = {
            x["name"]: {"atoms": x["atoms"], "energy": x["energy"]}
            for x in reactions[i]["reactionSystems"]
        }


def json2pkl(benchmark):
    save_directory = os.path.join(os.getcwd(), "raw_data")
    os.makedirs(save_directory, exist_ok=True)
    path_json = os.path.join(save_directory, f"{benchmark}.json")
    path_output = os.path.join(os.getcwd(), f"raw_data/{benchmark}.pkl")
    if not os.path.exists(path_output):
        if not os.path.exists(path_json):
            raw_reactions = reactions_from_dataset(benchmark)
            raw_reactions_json = {"raw_reactions": raw_reactions}
            with open(path_json, "w") as file:
                json.dump(raw_reactions_json, file, indent=4)

        with open(path_json, "r") as f:
            data = json.load(f)
        loaded_data = data["raw_reactions"]
        dat = copy.deepcopy(loaded_data)
        aseify_reactions(dat)

        data_total = {}
        tags = []

        for i, _ in enumerate(dat):
            try:
                input = {}
                input_slab_1_check = {}
                reactants_json = dat[i]["reactants"]
                reactants_dict = json.loads(reactants_json)

                products_json = dat[i]["products"]
                products_dict = json.loads(products_json)

                if "star" not in dat[i]["reactionSystems"]:
                    print(f"Error at {dat[i]}: star not exist in reaction")
                    continue

                sym = dat[i]["reactionSystems"]["star"]["atoms"].get_chemical_formula()
                reaction_name = dat[i]["Equation"]

                tag = sym + "_" + reaction_name
                if tag in tags:
                    count = tags.count(tag)
                    tags.append(tag)
                    tag = f"{tag}_{count}"
                else:
                    tags.append(tag)

                if "star" not in reactants_dict:
                    print(f"Error at {tag}: star not exist in reactants")
                    if tag in data_total:
                        del data_total[tag]
                    if tag in tags:
                        tags.remove(tag)
                    continue

                for key in dat[i]["reactionSystems"]:
                    if key in reactants_dict:
                        input[key] = {
                            "stoi": -reactants_dict[key],
                            "atoms": dat[i]["reactionSystems"][key]["atoms"],
                            "energy_cathub": dat[i]["reactionSystems"][key]["energy"],
                        }
                        input_slab_1_check[key] = {
                            "stoi": -reactants_dict[key],
                            "atoms": dat[i]["reactionSystems"][key]["atoms"],
                            "energy_cathub": dat[i]["reactionSystems"][key]["energy"],
                        }
                    elif key in products_dict:
                        input[key] = {
                            "stoi": products_dict[key],
                            "atoms": dat[i]["reactionSystems"][key]["atoms"],
                            "energy_cathub": dat[i]["reactionSystems"][key]["energy"],
                        }
                        input_slab_1_check[key] = {
                            "stoi": 1,
                            "atoms": dat[i]["reactionSystems"][key]["atoms"],
                            "energy_cathub": dat[i]["reactionSystems"][key]["energy"],
                        }

                data_total[tag] = {}
                data_total[tag]["raw"] = input
                data_total[tag]["cathub_energy"] = dat[i]["reactionEnergy"]
                energy_check = 0
                energy_check_slab_1 = 0
                star_num = 0
                for structure in input:
                    if "star" in str(structure):
                        star_num += 1
                    energy_check += (
                        input[structure]["energy_cathub"] * input[structure]["stoi"]
                    )
                    energy_check_slab_1 += (
                        input_slab_1_check[structure]["energy_cathub"]
                        * input_slab_1_check[structure]["stoi"]
                    )

                if star_num != 2:
                    print(f"Error at {tag}: Stars are not 2")
                    if tag in data_total:
                        del data_total[tag]
                    if tag in tags:
                        tags.remove(tag)
                    continue

                if dat[i]["reactionEnergy"] - energy_check > 0.001:
                    if dat[i]["reactionEnergy"] - energy_check_slab_1 < 0.001:
                        data_total[tag]["raw"] = input_slab_1_check
                        data_total[tag]["cathub_energy"] = dat[i]["reactionEnergy"]
                    else:
                        print(f"Error at {tag}: Reaction energy check failed")
                        if tag in data_total:
                            del data_total[tag]
                        if tag in tags:
                            tags.remove(tag)
                        continue

            except Exception as e:
                traceback.print_exc()
                print(f"Unexpected error {tag}: {e}")

        print(f"{len(data_total)}/{len(dat)} data construction complete!")
        with open(path_output, "wb") as file:
            pickle.dump(data_total, file)


def find_adsorbate(data):
    for key in data:
        if key.endswith("star_abs") and key != "star_abs":
            return key[: -len("star_abs")]


def min_max(DFT_values):
    min_value = float(np.min(DFT_values))
    max_value = float(np.max(DFT_values))

    range_value = max_value - min_value

    min = min_value - 0.1 * range_value
    max = max_value + 0.1 * range_value

    return min, max


def plotter_mono(DFT_values, NNP_values, NNP_name, tag, min_value, max_value, **kwargs):
    plot_save_path = os.path.join(os.getcwd(), "plot", NNP_name)
    os.makedirs(plot_save_path, exist_ok=True)
    figsize = kwargs.get("figsize", (9, 8))
    mark_size = kwargs.get("mark_size", 100)
    linewidths = kwargs.get("linewidths", 1.5)
    specific_color = kwargs.get("specific_color", "black")
    dpi = kwargs.get("dpi", 300)

    plt.figure(figsize=figsize)
    plt.scatter(
        DFT_values,
        NNP_values,
        color=specific_color,
        marker="^",
        s=mark_size,
        edgecolors="black",
        linewidths=linewidths,
    )

    plt.xlim(min_value, max_value)
    plt.ylim(min_value, max_value)
    plt.plot([min_value, max_value], [min_value, max_value], "r-")

    MAE = (
        np.sum(np.abs(DFT_values - NNP_values)) / len(DFT_values)
        if len(DFT_values) != 0
        else 0
    )

    plt.text(
        x=0.05,
        y=0.95,
        s=f"MAE-{NNP_name}: {MAE:.2f}",
        transform=plt.gca().transAxes,
        fontsize=30,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round", alpha=0.5, facecolor="white", edgecolor="black", pad=0.5
        ),
    )

    plt.xlabel("DFT (eV)", fontsize=40)
    plt.ylabel(f"{NNP_name} (eV)", fontsize=40)
    plt.tick_params(axis="both", which="major", labelsize=20)
    plt.grid(True)

    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(3)

    plt.tight_layout()
    plt.savefig(f"{plot_save_path}/{tag}_mono.png", dpi=dpi)
    plt.close()

    return MAE


def plotter_multi(ads_data, NNP_name, types, tag, min_value, max_value, **kwargs):
    colors = [
        "blue",
        "red",
        "green",
        "purple",
        "orange",
        "brown",
        "pink",
        "gray",
        "olive",
        "cyan",
        "magenta",
        "lime",
        "indigo",
        "gold",
        "darkred",
    ]
    markers = [
        "o",
        "^",
        "s",
        "p",
        "*",
        "h",
        "H",
        "D",
        "d",
        "<",
        ">",
        "v",
        "8",
        "P",
        "X",
    ]
    plot_save_path = os.path.join(os.getcwd(), "plot", NNP_name)
    os.makedirs(plot_save_path, exist_ok=True)
    figsize = kwargs.get("figsize", (9, 8))
    mark_size = kwargs.get("mark_size", 100)
    linewidths = kwargs.get("linewidths", 1.5)
    dpi = kwargs.get("dpi", 300)
    analysis_adsorbates = [
        adsorbate for adsorbate in ads_data.keys() if adsorbate != "all"
    ]

    plt.figure(figsize=figsize)
    error_sum = 0
    len_total = 0
    MAEs = {}

    for i, adsorbate in enumerate(analysis_adsorbates):
        DFT_values = []
        NNP_values = []
        for type in types:
            DFT_values.append(ads_data[adsorbate][type]["DFT"])
            NNP_values.append(ads_data[adsorbate][type]["NNP"])
        DFT_values = np.concatenate(DFT_values)
        NNP_values = np.concatenate(NNP_values)

        plt.scatter(
            DFT_values,
            NNP_values,
            color=colors[i],
            label=f"* {adsorbate}",
            marker=markers[i],
            s=mark_size,
            edgecolors="black",
            linewidths=linewidths,
        )
        MAEs[adsorbate] = (
            np.sum(np.abs(DFT_values - NNP_values)) / len(DFT_values)
            if len(DFT_values) != 0
            else 0
        )
        error_sum += np.sum(np.abs(DFT_values - NNP_values))
        len_total += len(DFT_values)

        MAEs[f"len_{adsorbate}"] = len(DFT_values)

    plt.xlim(min_value, max_value)
    plt.ylim(min_value, max_value)
    plt.plot([min_value, max_value], [min_value, max_value], "r-")

    MAE_total = error_sum / len_total if len_total != 0 else 0
    MAEs["total"] = MAE_total

    plt.text(
        x=0.05,
        y=0.95,
        s=f"MAE-{NNP_name}: {MAE_total:.2f}",
        transform=plt.gca().transAxes,
        fontsize=30,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round", alpha=0.5, facecolor="white", edgecolor="black", pad=0.5
        ),
    )

    plt.xlabel("DFT (eV)", fontsize=40)
    plt.ylabel(f"{NNP_name} (eV)", fontsize=40)
    plt.tick_params(axis="both", which="major", labelsize=20)
    plt.legend(loc="lower right", fontsize=20)
    plt.grid(True)

    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(3)

    plt.tight_layout()
    plt.savefig(f"{plot_save_path}/{tag}_multi.png", dpi=dpi)
    plt.close()

    return MAEs


def data_to_excel(main_data, outlier_data, NNPs_data, analysis_adsorbates, **kwargs):
    benchmarking_name = kwargs.get("Benchmarking_name", os.path.basename(os.getcwd()))

    df_main = pd.DataFrame(main_data)

    output_file = f"{benchmarking_name}_Benchmarking_Analysis.xlsx"

    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        df_main.to_excel(writer, sheet_name="MLP_Data", index=False)

        df_outlier = pd.DataFrame(outlier_data)
        df_outlier.to_excel(writer, sheet_name="outlier", index=False)

        for NNP_name, data_dict in NNPs_data.items():
            data_tmp = []
            for adsorbate in analysis_adsorbates:
                if f"len_{adsorbate}" in data_dict["normal"]:
                    normal_rate = (
                        data_dict["normal"][f"len_{adsorbate}"]
                        / data_dict["all"][f"len_{adsorbate}"]
                        * 100
                    )
                    data_tmp.append(
                        {
                            "Adsorbate_name": adsorbate,
                            "Normal rate (%)": normal_rate,
                            "MAE_total (eV)": data_dict["all"][adsorbate],
                            "MAE_normal (eV)": data_dict["normal"][adsorbate],
                            "MAE_outlier (eV)": data_dict["outlier"][adsorbate],
                            "Num_total": data_dict["all"][f"len_{adsorbate}"],
                            "Num_normal": data_dict["normal"][f"len_{adsorbate}"],
                            "Num_outlier": data_dict["outlier"][f"len_{adsorbate}"],
                        }
                    )

            data_df = pd.DataFrame(data_tmp)
            data_df.to_excel(writer, sheet_name=NNP_name, index=False)

        # 워크북 및 포맷 정의
        workbook = writer.book
        center_align = workbook.add_format({"align": "center"})
        number_format_0f = workbook.add_format(
            {"num_format": "#,##0", "align": "center"}
        )
        number_format_1f = workbook.add_format({"num_format": "0.0", "align": "center"})
        number_format_2f = workbook.add_format(
            {"num_format": "0.00", "align": "center"}
        )
        number_format_3f = workbook.add_format(
            {"num_format": "0.000", "align": "center"}
        )

        # 열 별 형식 및 너비 지정
        column_formats = {
            "Normal rate (%)": (
                15,
                workbook.add_format(
                    {"num_format": "0.00", "align": "center", "bold": True}
                ),
            ),
            "MAE_total (eV)": (15, number_format_3f),
            "MAE_normal (eV)": (
                15,
                workbook.add_format(
                    {"num_format": "0.000", "align": "center", "bold": True}
                ),
            ),
            "MAE_outlier (eV)": (15, number_format_3f),
            "Num_total": (12, number_format_0f),
            "Num_normal": (12, number_format_0f),
            "Num_outlier": (12, number_format_0f),
            "slab_conv": (12, number_format_0f),
            "ads_conv": (12, number_format_0f),
            "slab_move": (12, number_format_0f),
            "ads_move": (12, number_format_0f),
            "slab_seed": (12, number_format_0f),
            "ads_seed": (12, number_format_0f),
            "ads_eng_seed": (12, number_format_0f),
            "Time_total (s)": (15, number_format_0f),
            "Time_per_step (s)": (17, number_format_3f),
        }

        # 모든 시트에 대해 포맷 적용
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            df = (
                df_main
                if sheet_name == "MLP_Data"
                else (
                    df_outlier
                    if sheet_name == "outlier"
                    else pd.DataFrame(
                        [dict(zip(data_tmp[0].keys(), range(len(data_tmp[0]))))]
                    )
                )
            )

            for col_num, col_name in enumerate(df.columns):
                if col_name in column_formats:
                    width, fmt = column_formats[col_name]
                else:
                    width = (
                        max(df[col_name].astype(str).map(len).max(), len(col_name)) + 10
                    )
                    fmt = center_align

                worksheet.set_column(col_num, col_num, width, fmt)

                # 문자열 열인 경우
                if df[col_name].dtype == "object":
                    worksheet.set_column(col_num, col_num, width, center_align)
                else:
                    worksheet.set_column(col_num, col_num, width, fmt)

    print(f"Excel file '{output_file}' created successfully.")


def count_lbfgs_steps(log_path):
    with open(log_path, "r") as file:
        lines = file.readlines()

    # Iterate through the lines in reverse to find the last "Done!" instance
    for i, line in enumerate(reversed(lines)):
        if "Done!" in line:
            # Get the line right above "Done!"
            previous_line = lines[
                -(i + 2)
            ]  # i+2 because i starts at 0 and we're looking for the line above
            if previous_line.startswith("LBFGS:"):
                # Extract the step number from the LBFGS line and add 1
                step_number = int(previous_line.split()[1])
                return step_number + 1

    # Return 0 if "Done!" or "LBFGS:" is not found
    print("notfound")
    return 0


def get_txt_files_in_directory(directory_path):
    txt_files = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".txt"):
                # Get full path of the txt file
                full_path = os.path.join(root, file)
                txt_files.append(full_path)

    return txt_files


def analysis_MLPs(**kwargs):
    main_data = []
    outlier_data = []
    NNP_datas = {}
    adsorbates = set()
    calculating_path = kwargs.get(
        "calculating_path", os.path.join(os.getcwd(), "result")
    )
    NNP_list = kwargs.get(
        "NNP_list",
        sorted(
            [
                name
                for name in os.listdir(calculating_path)
                if os.path.isdir(os.path.join(calculating_path, name))
            ],
            key=str.lower,
        ),
    )
    for NNP_name in NNP_list:
        print(NNP_name)
        with open(f"{calculating_path}/{NNP_name}/{NNP_name}_result.json", "r") as f:
            NNP_result = json.load(f)

        with open(f"{calculating_path}/{NNP_name}/{NNP_name}_outlier.json", "r") as f:
            NNP_outlier = json.load(f)

        ads_data = {
            "all": {
                "normal": {"DFT": np.array([]), "NNP": np.array([])},
                "outlier": {"DFT": np.array([]), "NNP": np.array([])},
            }
        }

        for reaction in NNP_result:
            adsorbate = find_adsorbate(NNP_result[reaction]["cathub"])
            adsorbates.add(adsorbate)

        time_accum = 0
        step_accum = 0

        slab_conv = 0
        ads_conv = 0
        slab_move = 0
        ads_move = 0
        slab_seed = 0
        ads_seed = 0
        ads_eng_seed = 0

        analysis_adsorbates = kwargs.get("target_adsorbates", adsorbates)

        for reaction in NNP_result:
            adsorbate = find_adsorbate(NNP_result[reaction]["cathub"])
            if adsorbate in analysis_adsorbates:
                if adsorbate not in ads_data:
                    ads_data[adsorbate] = {
                        "normal": {"DFT": np.array([]), "NNP": np.array([])},
                        "outlier": {"DFT": np.array([]), "NNP": np.array([])},
                    }

                num_outliers = sum(NNP_result[reaction]["outliers"].values())

                if num_outliers == 0:
                    ads_data[adsorbate]["normal"]["DFT"] = np.append(
                        ads_data[adsorbate]["normal"]["DFT"],
                        NNP_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data[adsorbate]["normal"]["NNP"] = np.append(
                        ads_data[adsorbate]["normal"]["NNP"],
                        NNP_result[reaction]["final"]["ads_eng_median"],
                    )
                    ads_data["all"]["normal"]["DFT"] = np.append(
                        ads_data["all"]["normal"]["DFT"],
                        NNP_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data["all"]["normal"]["NNP"] = np.append(
                        ads_data["all"]["normal"]["NNP"],
                        NNP_result[reaction]["final"]["ads_eng_median"],
                    )
                else:
                    ads_data[adsorbate]["outlier"]["DFT"] = np.append(
                        ads_data[adsorbate]["outlier"]["DFT"],
                        NNP_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data[adsorbate]["outlier"]["NNP"] = np.append(
                        ads_data[adsorbate]["outlier"]["NNP"],
                        NNP_result[reaction]["final"]["ads_eng_median"],
                    )
                    ads_data["all"]["outlier"]["DFT"] = np.append(
                        ads_data["all"]["outlier"]["DFT"],
                        NNP_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data["all"]["outlier"]["NNP"] = np.append(
                        ads_data["all"]["outlier"]["NNP"],
                        NNP_result[reaction]["final"]["ads_eng_median"],
                    )

                time_accum += sum(
                    value
                    for key, value in NNP_result[reaction]["final"].items()
                    if "time_total" in key
                )

                log_dir_path = f"{calculating_path}/{NNP_name}/log/{reaction}"
                txt_files = get_txt_files_in_directory(log_dir_path)

                for txt_file in txt_files:
                    step_tmp = count_lbfgs_steps(txt_file)
                    step_accum += step_tmp

                if NNP_result[reaction]["outliers"]["slab_conv"]:
                    slab_conv += 1

                if NNP_result[reaction]["outliers"]["ads_conv"]:
                    ads_conv += 1

                if NNP_result[reaction]["outliers"]["slab_move"]:
                    slab_move += 1

                if NNP_result[reaction]["outliers"]["ads_move"]:
                    ads_move += 1

                if NNP_result[reaction]["outliers"]["slab_seed"]:
                    slab_seed += 1

                if NNP_result[reaction]["outliers"]["ads_seed"]:
                    ads_seed += 1

                if NNP_result[reaction]["outliers"]["ads_eng_seed"]:
                    ads_eng_seed += 1

        DFT_data = np.concatenate(
            (ads_data["all"]["normal"]["DFT"], ads_data["all"]["outlier"]["DFT"])
        )
        min_value_DFT, max_value_DFT = min_max(DFT_data)

        min_value = kwargs.get("min", min_value_DFT)
        max_value = kwargs.get("max", max_value_DFT)

        MAE_all = plotter_mono(
            np.concatenate(
                (ads_data["all"]["normal"]["DFT"], ads_data["all"]["outlier"]["DFT"])
            ),
            np.concatenate(
                (ads_data["all"]["normal"]["NNP"], ads_data["all"]["outlier"]["NNP"])
            ),
            NNP_name,
            "all",
            min_value,
            max_value,
            **kwargs,
        )
        MAE_normal = plotter_mono(
            ads_data["all"]["normal"]["DFT"],
            ads_data["all"]["normal"]["NNP"],
            NNP_name,
            "normal",
            min_value,
            max_value,
            **kwargs,
        )
        MAE_outlier = plotter_mono(
            ads_data["all"]["outlier"]["DFT"],
            ads_data["all"]["outlier"]["NNP"],
            NNP_name,
            "outlier",
            min_value,
            max_value,
            **kwargs,
        )

        MAEs_all_multi = plotter_multi(
            ads_data,
            NNP_name,
            ["normal", "outlier"],
            "all",
            min_value,
            max_value,
            **kwargs,
        )
        MAEs_normal_multi = plotter_multi(
            ads_data, NNP_name, ["normal"], "normal", min_value, max_value, **kwargs
        )
        MAEs_outlier_multi = plotter_multi(
            ads_data, NNP_name, ["outlier"], "outlier", min_value, max_value, **kwargs
        )

        NNP_datas[NNP_name] = {
            "all": MAEs_all_multi,
            "normal": MAEs_normal_multi,
            "outlier": MAEs_outlier_multi,
        }

        total_num = len(ads_data["all"]["normal"]["DFT"]) + len(
            ads_data["all"]["outlier"]["DFT"]
        )
        normal_rate = len(ads_data["all"]["normal"]["DFT"]) / total_num * 100

        main_data.append(
            {
                "NNP_name": NNP_name,
                "Normal rate (%)": normal_rate,
                "MAE_total (eV)": MAE_all,
                "MAE_normal (eV)": MAE_normal,
                "MAE_outlier (eV)": MAE_outlier,
                "Num_total": total_num,
                "Num_normal": len(ads_data["all"]["normal"]["DFT"]),
                "Num_outlier": len(ads_data["all"]["outlier"]["DFT"]),
                "Time_total (s)": NNP_outlier["Time"],
                "Time_per_step (s)": time_accum / step_accum,
            }
        )

        outlier_data.append(
            {
                "NNP_name": NNP_name,
                "Num_outlier": len(ads_data["all"]["outlier"]["DFT"]),
                "slab_conv": slab_conv,
                "ads_conv": ads_conv,
                "slab_move": slab_move,
                "ads_move": ads_move,
                "slab_seed": slab_seed,
                "ads_seed": ads_seed,
                "ads_eng_seed": ads_eng_seed,
            }
        )

    data_to_excel(
        main_data, outlier_data, NNP_datas, list(analysis_adsorbates), **kwargs
    )
