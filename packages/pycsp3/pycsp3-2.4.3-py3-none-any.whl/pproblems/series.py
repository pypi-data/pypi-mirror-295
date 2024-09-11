import os
import subprocess
import sys

from pycsp3.compiler import Compilation
from pycsp3.dashboard import options
from pycsp3.tools.utilities import BLUE, WHITE

path_home = os.sep + "home" + os.sep + "lecoutre" + os.sep
path_prefix = path_home + "workspacePy" + os.sep + "pycsp3" + os.sep + "problems" + os.sep
path_prefix_parsers = path_prefix + "data" + os.sep + "parsers" + os.sep
path_prefix_instances = path_home + "instances" + os.sep

path_csp_acad = path_prefix + "csp" + os.sep + "academic" + os.sep
path_csp_real = path_prefix + "csp" + os.sep + "complex" + os.sep
path_cop_acad = path_prefix + "cop" + os.sep + "academic" + os.sep
path_cop_real = path_prefix + "cop" + os.sep + "complex" + os.sep

path_mzn = path_home + "workspacePy" + os.sep + "ppycsp3" + os.sep + "pproblems" + os.sep + "mzn"
mzn08, mzn09 = [path_mzn + "0" + str(year) + os.sep for year in (8, 9)]
mzn10, mzn11, mzn12, mzn13, mzn14, mzn15, mzn16, mzn17, mzn18, mzn19, mzn20, mzn21, mzn22 = [path_mzn + str(year) + os.sep for year in range(10, 23)]
path_pbs = path_home + "instances" + os.sep + "minizinc-compets" + os.sep + "pbs"
pbs08, pbs09 = [path_pbs + "0" + str(year) + os.sep for year in (8, 9)]
pbs10, pbs11, pbs12, pbs13, pbs14, pbs15, pbs16, pbs17, pbs18, pbs19, pbs20, pbs21, pbs22 = [path_pbs + str(year) + os.sep for year in range(10, 23)]

cwd = os.getcwd()
seriesName = sys.argv[1].lower()


def list_files(d, *, filter=None):
    return [os.path.join(d, f) for f in os.listdir(d) if filter is None or filter(f)]


def series(name):
    os.chdir(cwd)
    if seriesName == name.lower():
        if not os.path.isdir(name):
            os.mkdir(name)
        os.chdir(name)
        return True
    return False


def execute(model, *, variants=None, data=None, dzn_dir=None, json_dir=None, dataformat=None, dataparser=None, series=None, other_args=None):
    if dzn_dir is not None:
        assert isinstance(dzn_dir, str) and data is None and json_dir is None
        for file in list_files(dzn_dir, filter=lambda s: s.endswith(".dzn")):
            execute(model, variants=variants, data=file, dataformat=dataformat, dataparser=dataparser, series=series, other_args=other_args)
        return
    if json_dir is not None:
        assert isinstance(json_dir, str) and data is None and dzn_dir is None
        for file in list_files(json_dir, filter=lambda s: s.endswith(".json")):
            execute(model, variants=variants, data=file, dataformat=dataformat, dataparser=dataparser, series=series, other_args=other_args)
        return
    if series:
        curr_wd = os.getcwd()
        if not os.path.isdir(series):
            os.mkdir(series)
        os.chdir(series)

    data = None if data is None else "[" + ",".join(str(v) for v in data) + "]" if isinstance(data, (tuple, list)) else str(data)
    variants = variants if isinstance(variants, (tuple, list)) else [variants]
    for variant in variants:
        command = "python3 " + model + (" -variant=" + variant if variant else "") + (" -data=" + data if data else "")
        command += (" -dataformat=" + dataformat if dataformat else "") + (" -dataparser=" + dataparser if dataparser else "")
        command += (" -suffix=" + options.suffix if options.suffix else "") + (" " + str(other_args) if other_args else "")
        # command += " -lzma"
        print(BLUE + "Command:" + WHITE, command)
        subprocess.call(command.split())
    if series:
        os.chdir(curr_wd)


def executemzn(dir1, dir2, model=None, *, variants=None, data=None, dzn_dir=None, json_dir=None, dataformat=None, dataparser=None, series=None,
               other_args=None):
    path = path_home + "workspacePy" + os.sep + "pycsp3-models" + os.sep + dir1 + os.sep + dir2 + os.sep
    model = dir2 + ".py" if model is None else dir2 + model + ".py" if not model.endswith(".py") else model
    if dzn_dir is not None:
        assert dataparser is None
        dataparser = path + "data" + os.sep + dir2 + "_ParserZ.py"
    execute(path + model, variants=variants, data=data, dzn_dir=dzn_dir, json_dir=json_dir, dataformat=dataformat, dataparser=dataparser, series=series,
            other_args=other_args)


new = True


def m08():  # 5s
    options.suffix = "_m08"

    if new:
        executemzn("realistic", "Radiation", "_z", dzn_dir=pbs08 + "radiation")
        executemzn("realistic", "RCPSP", "_z", dzn_dir=pbs08 + "rcpsp")
        executemzn("crafted", "ShortestPath", dzn_dir=pbs08 + "shortest-path")
        executemzn("crafted", "Trucking", dzn_dir=pbs08 + "trucking")
    else:
        execute(mzn12 + "Radiation.py", dzn_dir=pbs08 + "radiation", dataparser=mzn12 + "Radiation_ParserZ.py")
        execute(mzn13 + "RCPSP.py", dzn_dir=pbs08 + "rcpsp", dataparser=mzn13 + "RCPSP_ParserZ.py")
        execute(mzn08 + "ShortestPath.py", dzn_dir=pbs08 + "shortest-path", dataparser=mzn08 + "ShortestPath_ParserZ.py")
        execute(mzn08 + "Trucking.py", dzn_dir=pbs08 + "trucking", dataparser=mzn08 + "Trucking_ParserZ.py")


def m09():  # 45s
    options.suffix = "_m09"

    if new:
        executemzn("realistic", "OpenStacks", "_z", dzn_dir=pbs09 + "open-stacks")
        for v in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
            executemzn("academic", "Perfect1Factorization", variants=[None, "dec"], data=v, dataformat="{:02d}")
        executemzn("realistic", "Roster", dzn_dir=pbs09 + "roster")
        for v in [5, 6, 7, 8, 9]:
            executemzn("academic", "StillLife", "_z", data=v, dataformat="{:02d}")
        executemzn("realistic", "VRP", dzn_dir=pbs09 + "vrp")
    else:
        execute(mzn15 + "OpenStacks.py", dzn_dir=pbs09 + "open-stacks", dataparser=mzn15 + "OpenStacks_ParserZ.py")
        for v in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
            execute(mzn15 + "Perfect1Factorization.py", variants=[None, "dec"], data=v, dataformat="{:02d}")
        execute(mzn15 + "Roster.py", dzn_dir=pbs09 + "roster", dataparser=mzn15 + "Roster_ParserZ.py")
        for v in [5, 6, 7, 8, 9]:
            execute(mzn09 + "StillLife.py", data=v, dataformat="{:02d}")
        execute(mzn12 + "VRP.py", dzn_dir=pbs09 + "vrp", dataparser=mzn12 + "VRP_ParserZ.py")


def m10():  # 2' (rcpsp_max/psp-ubo500-33.dzn is long; GridColoring not introduced because same instances as in 2011)
    options.suffix = "_m10"

    if new:
        executemzn("realistic", "BACP", "_z", dzn_dir=pbs10 + "bacp")
        executemzn("realistic", "DepotPlacement", dzn_dir=pbs10 + "depot-placement")
        executemzn("realistic", "Filters", dzn_dir=pbs10 + "filters")
        for t in [(3, 10, 20), (3, 7, 20), (3, 8, 20), (3, 9, 16), (4, 10, 16), (4, 7, 16), (4, 8, 16), (4, 9, 10), (4, 9, 14), (4, 9, 18)]:
            executemzn("academic", "Ghoulomb", data=t, dataformat="{:01d}-{:02d}-{:02d}")
        executemzn("realistic", "RCPSP_MAX", dzn_dir=pbs10 + "rcpsp_max")
        executemzn("crafted", "Sugiyama", dzn_dir=pbs10 + "sugiyama")
    else:
        execute(mzn11 + "BACP.py", dzn_dir=pbs10 + "bacp", dataparser=mzn11 + "BACP_ParserZ.py")
        execute(mzn16 + "DepotPlacement.py", dzn_dir=pbs10 + "depot-placement", dataparser=mzn16 + "DepotPlacement_ParserZ.py")
        execute(mzn13 + "Filters.py", dzn_dir=pbs10 + "filters", dataparser=mzn13 + "Filters_ParserZ.py")
        for t in [(3, 10, 20), (3, 7, 20), (3, 8, 20), (3, 9, 16), (4, 10, 16), (4, 7, 16), (4, 8, 16), (4, 9, 10), (4, 9, 14), (4, 9, 18)]:
            execute(mzn13 + "Ghoulomb.py", data=t, dataformat="{:01d}-{:02d}-{:02d}")
        execute(mzn10 + "RCPSP_MAX.py", dzn_dir=pbs10 + "rcpsp_max", dataparser=mzn10 + "RCPSP_MAX_ParserZ.py")
        execute(mzn10 + "Sugiyama.py", dzn_dir=pbs10 + "sugiyama", dataparser=mzn10 + "Sugiyama_ParserZ.py")


def m11():  # 1'30s
    options.suffix = "_m11"

    if new:
        executemzn("realistic", "BACP", "_z", dzn_dir=pbs11 + "bacp")
        executemzn("realistic", "CarpetCutting", dzn_dir=pbs11 + "carpet-cutting")
        executemzn("realistic", "CyclicRCPSP", dzn_dir=pbs11 + "cyclic-rcpsp")
        executemzn("realistic", "DepotPlacement", dzn_dir=pbs11 + "depot-placement")
        executemzn("realistic", "Fastfood", "_z", dzn_dir=pbs11 + "fast-food")
        for t in [(5, 6), (7, 8), (10, 10), (12, 13), (15, 16)]:
            executemzn("academic", "GridColoring", data=t, dataformat="{:02d}-{:02d}")
        executemzn("realistic", "OpenStacks", "_z", dzn_dir=pbs11 + "open-stacks")
        executemzn("realistic", "ItemsetMining", dzn_dir=pbs11 + "pattern-set-mining" + os.sep + "k1", variants=[None, "table"], other_args="-dontuseauxcache")
        executemzn("realistic", "ItemsetMining", dzn_dir=pbs11 + "pattern-set-mining" + os.sep + "k2", other_args="-dontuseauxcache")
        executemzn("realistic", "PrizeCollecting", "_z", dzn_dir=pbs11 + "prize-collecting")
        executemzn("realistic", "Roster", dzn_dir=pbs11 + "roster")
        executemzn("realistic", "ShipScheduling", dzn_dir=pbs11 + "ship-schedule")
        executemzn("realistic", "TableLayout", dzn_dir=pbs11 + "table-layout")
        executemzn("realistic", "VRP", dzn_dir=pbs11 + "vrp")
    else:
        execute(mzn11 + "BACP.py", dzn_dir=pbs11 + "bacp", dataparser=mzn11 + "BACP_ParserZ.py")
        execute(mzn16 + "CarpetCutting.py", dzn_dir=pbs11 + "carpet-cutting", dataparser=mzn16 + "CarpetCutting_ParserZ.py")
        execute(mzn14 + "CyclicRCPSP.py", dzn_dir=pbs11 + "cyclic-rcpsp", dataparser=mzn14 + "CyclicRCPSP_ParserZ.py")
        execute(mzn16 + "DepotPlacement.py", dzn_dir=pbs11 + "depot-placement", dataparser=mzn16 + "DepotPlacement_ParserZ.py")
        execute(mzn11 + "Fastfood.py", dzn_dir=pbs11 + "fast-food", dataparser=mzn11 + "Fastfood_ParserZ.py")
        for t in [(5, 6), (7, 8), (10, 10), (12, 13), (15, 16)]:
            execute(mzn15 + "GridColoring.py", data=t, dataformat="{:02d}-{:02d}")
        execute(mzn15 + "OpenStacks.py", dzn_dir=pbs11 + "open-stacks", dataparser=mzn15 + "OpenStacks_ParserZ.py")
        execute(mzn13 + "ItemsetMining.py", dzn_dir=pbs11 + "pattern-set-mining" + os.sep + "k1", variants=[None, "table"],
                dataparser=mzn13 + "ItemsetMining_ParserZ.py", other_args="-dontuseauxcache")
        execute(mzn13 + "ItemsetMining.py", dzn_dir=pbs11 + "pattern-set-mining" + os.sep + "k2", dataparser=mzn13 + "ItemsetMining_ParserZ.py",
                other_args="-dontuseauxcache")
        execute(mzn11 + "PrizeCollecting.py", dzn_dir=pbs11 + "prize-collecting", dataparser=mzn11 + "PrizeCollecting_ParserZ.py")
        execute(mzn15 + "Roster.py", dzn_dir=pbs11 + "roster", dataparser=mzn15 + "Roster_ParserZ.py")
        execute(mzn12 + "ShipScheduling.py", dzn_dir=pbs11 + "ship-schedule", dataparser=mzn12 + "ShipScheduling_ParserZ.py")
        execute(mzn11 + "TableLayout.py", dzn_dir=pbs11 + "table-layout", dataparser=mzn11 + "TableLayout_ParserZ.py")
        execute(mzn12 + "VRP.py", dzn_dir=pbs11 + "vrp", dataparser=mzn12 + "VRP_ParserZ.py")


def m12():  # 40s (but the table variant of ItemsetMining is discarded for the moment, because very long)
    options.suffix = "_m12"

    if new:
        executemzn("recreational", "Amaze", "_z1", dzn_dir=pbs12 + "amaze")
        executemzn("realistic", "CarpetCutting", dzn_dir=pbs12 + "carpet-cutting")
        executemzn("realistic", "Fastfood", "_z", dzn_dir=pbs12 + "fast-food")
        executemzn("realistic", "Filters", dzn_dir=pbs12 + "filters")
        executemzn("recreational", "League", "_z", dzn_dir=pbs12 + "league")
        executemzn("realistic", "MSPSP", dzn_dir=pbs12 + "mspsp")
        executemzn("realistic", "ParityLearning", dzn_dir=pbs12 + "parity-learning")
        executemzn("realistic", "ItemsetMining", dzn_dir=pbs12 + "pattern-set-mining" + os.sep + "k1", other_args="-dontuseauxcache")
        executemzn("realistic", "ItemsetMining", dzn_dir=pbs12 + "pattern-set-mining" + os.sep + "k2", other_args="-dontuseauxcache")
        executemzn("realistic", "Radiation", "_z", dzn_dir=pbs12 + "radiation")
        executemzn("realistic", "ShipScheduling", dzn_dir=pbs12 + "ship-schedule")
        for v in [9, 10, 11, 12, 13]:
            executemzn("academic", "StillLifeWastage", data=v, dataformat="{:02d}")
        executemzn("realistic", "TPP", dzn_dir=pbs12 + "tpp")
        executemzn("realistic", "Train", dzn_dir=pbs12 + "train")
        executemzn("realistic", "VRP", dzn_dir=pbs12 + "vrp")
    else:
        execute(mzn12 + "Amaze1.py", dzn_dir=pbs12 + "amaze", dataparser=mzn12 + "Amaze_ParserZ.py")
        execute(mzn16 + "CarpetCutting.py", dzn_dir=pbs12 + "carpet-cutting", dataparser=mzn16 + "CarpetCutting_ParserZ.py")
        execute(mzn11 + "Fastfood.py", dzn_dir=pbs12 + "fast-food", dataparser=mzn11 + "Fastfood_ParserZ.py")
        execute(mzn13 + "Filters.py", dzn_dir=pbs12 + "filters", dataparser=mzn13 + "Filters_ParserZ.py")
        execute(mzn12 + "League.py", dzn_dir=pbs12 + "league", dataparser=mzn12 + "League_ParserZ.py")
        execute(mzn12 + "MSPSP.py", dzn_dir=pbs12 + "mspsp", dataparser=mzn12 + "MSPSP_ParserZ.py")
        execute(mzn12 + "ParityLearning.py", dzn_dir=pbs12 + "parity-learning", dataparser=mzn12 + "ParityLearning_ParserZ.py")
        execute(mzn13 + "ItemsetMining.py", dzn_dir=pbs12 + "pattern-set-mining" + os.sep + "k1",  # variants=[None, "table"],
                dataparser=mzn13 + "ItemsetMining_ParserZ.py", other_args="-dontuseauxcache")
        execute(mzn13 + "ItemsetMining.py", dzn_dir=pbs12 + "pattern-set-mining" + os.sep + "k2", dataparser=mzn13 + "ItemsetMining_ParserZ.py",
                other_args="-dontuseauxcache")
        execute(mzn12 + "Radiation.py", dzn_dir=pbs12 + "radiation", dataparser=mzn12 + "Radiation_ParserZ.py")
        execute(mzn12 + "ShipScheduling.py", dzn_dir=pbs12 + "ship-schedule", dataparser=mzn12 + "ShipScheduling_ParserZ.py")
        for v in [9, 10, 11, 12, 13]:
            execute(mzn12 + "StillLifeWastage.py", data=v, dataformat="{:02d}")
        execute(mzn12 + "TPP.py", dzn_dir=pbs12 + "tpp", dataparser=mzn12 + "TPP_ParserZ.py")
        execute(mzn18 + "Train.py", dzn_dir=pbs12 + "train", dataparser=mzn18 + "Train_ParserZ.py")
        execute(mzn12 + "VRP.py", dzn_dir=pbs12 + "vrp", dataparser=mzn12 + "VRP_ParserZ.py")


def m13():  # 50s (one big proteinDesign instance rather long; the table variant of ItemsetMining discarded)
    options.suffix = "_m13"

    if new:
        executemzn("realistic", "Cargo", dzn_dir=pbs13 + "cargo")
        executemzn("realistic", "CELAR", dzn_dir=pbs13 + "celar")
        executemzn("realistic", "Filters", dzn_dir=pbs13 + "filters")
        executemzn("realistic", "FlexibleJobshop", dzn_dir=pbs13 + "fjsp")
        for t in [(3, 9, 16), (3, 11, 29), (4, 9, 10), (4, 9, 20), (5, 7, 22)]:
            executemzn("academic", "Ghoulomb", data=t, dataformat="{:01d}-{:02d}-{:02d}")
        executemzn("realistic", "JavaRouting", dzn_dir=pbs13 + "javarouting")
        executemzn("realistic", "LinearToProgram", dzn_dir=pbs13 + "l2p")
        executemzn("realistic", "League", "13", dzn_dir=pbs13 + "league")
        executemzn("recreational", "Mario", "_z", dzn_dir=pbs13 + "mario")
        executemzn("realistic", "OncallRostering", dzn_dir=pbs13 + "on-call-rostering")
        executemzn("realistic", "ItemsetMining", dzn_dir=pbs13 + "pattern-set-mining" + os.sep + "k1", other_args="-dontuseauxcache")
        executemzn("realistic", "ItemsetMining", dzn_dir=pbs13 + "pattern-set-mining" + os.sep + "k2", other_args="-dontuseauxcache")
        executemzn("realistic", "ProteinDesign", dzn_dir=pbs13 + "proteindesign12")
        executemzn("realistic", "Radiation", "_z", dzn_dir=pbs13 + "radiation")
        executemzn("realistic", "RCPSP", "_z", dzn_dir=pbs13 + "rcpsp")
        executemzn("realistic", "VRP", dzn_dir=pbs13 + "vrp")
    else:
        execute(mzn18 + "Cargo.py", dzn_dir=pbs13 + "cargo", dataparser=mzn18 + "Cargo_ParserZ.py")
        execute(mzn13 + "Celar.py", dzn_dir=pbs13 + "celar", dataparser=mzn13 + "Celar_ParserZ.py")
        execute(mzn13 + "Filters.py", dzn_dir=pbs13 + "filters", dataparser=mzn13 + "Filters_ParserZ.py")
        execute(mzn13 + "FlexibleJobshop.py", dzn_dir=pbs13 + "fjsp", dataparser=mzn13 + "FlexibleJobshop_ParserZ.py")
        for t in [(3, 9, 16), (3, 11, 29), (4, 9, 10), (4, 9, 20), (5, 7, 22)]:
            execute(mzn13 + "Ghoulomb.py", data=t, dataformat="{:01d}-{:02d}-{:02d}")
        execute(mzn13 + "JavaRouting.py", dzn_dir=pbs13 + "javarouting", dataparser=mzn13 + "JavaRouting_ParserZ.py")
        execute(mzn13 + "LinearToProgram.py", dzn_dir=pbs13 + "l2p", dataparser=mzn13 + "LinearToProgram_ParserZ.py")
        execute(mzn13 + "League13.py", dzn_dir=pbs13 + "league", dataparser=mzn12 + "League_ParserZ.py")
        execute(mzn13 + "Mario.py", dzn_dir=pbs13 + "mario", dataparser=mzn13 + "Mario_ParserZ.py")
        execute(mzn13 + "OncallRostering.py", dzn_dir=pbs13 + "on-call-rostering", dataparser=mzn13 + "OncallRostering_ParserZ.py")
        execute(mzn13 + "ItemsetMining.py", dzn_dir=pbs13 + "pattern-set-mining" + os.sep + "k1",  # variants=[None, "table"],
                dataparser=mzn13 + "ItemsetMining_ParserZ.py", other_args="-dontuseauxcache")
        execute(mzn13 + "ItemsetMining.py", dzn_dir=pbs13 + "pattern-set-mining" + os.sep + "k2", dataparser=mzn13 + "ItemsetMining_ParserZ.py",
                other_args="-dontuseauxcache")
        execute(mzn18 + "ProteinDesign.py", dzn_dir=pbs13 + "proteindesign12", dataparser=mzn18 + "ProteinDesign_ParserZ.py")
        execute(mzn12 + "Radiation.py", dzn_dir=pbs13 + "radiation", dataparser=mzn12 + "Radiation_ParserZ.py")
        execute(mzn13 + "RCPSP.py", dzn_dir=pbs13 + "rcpsp", dataparser=mzn13 + "RCPSP_ParserZ.py")
        execute(mzn12 + "VRP.py", dzn_dir=pbs13 + "vrp", dataparser=mzn12 + "VRP_ParserZ.py")


def m14():  # 1'05s (unfinished groups for OpenShop)
    options.suffix = "_m14"

    if new:
        executemzn("realistic", "CyclicRCPSP", dzn_dir=pbs14 + "cyclic-rcpsp")
        executemzn("realistic", "Elitserien", dzn_dir=pbs14 + "elitserien")
        executemzn("realistic", "JapanEncoding", dzn_dir=pbs14 + "jp-encoding")
        executemzn("recreational", "Mario", "_z", dzn_dir=pbs14 + "mario")
        for v in [11, 12, 13, 20, 31]:
            executemzn("academic", "MQueens", data=v)
        executemzn("realistic", "OpenShop", dzn_dir=pbs14 + "openshop")
        executemzn("realistic", "RoadConstruction", dzn_dir=pbs14 + "road-cons")
        executemzn("realistic", "ShipScheduling", dzn_dir=pbs14 + "ship-schedule")
        executemzn("realistic", "Smelt", dzn_dir=pbs14 + "smelt")
        executemzn("realistic", "Spot5", variants=[None, "mini"], dzn_dir=pbs14 + "spot5")
        executemzn("realistic", "StochasticFJSP", json_dir=pbs14 + "stochastic-fjsp")
        executemzn("realistic", "StochasticVRP", json_dir=pbs14 + "stochastic-vrp")
        executemzn("realistic", "Train", dzn_dir=pbs14 + "train")
        executemzn("realistic", "TTP_PV", dzn_dir=pbs14 + "traveling-tppv")
    else:
        execute(mzn14 + "CyclicRCPSP.py", dzn_dir=pbs14 + "cyclic-rcpsp", dataparser=mzn14 + "CyclicRCPSP_ParserZ.py")
        execute(mzn18 + "Elitserien.py", dzn_dir=pbs14 + "elitserien", dataparser=mzn18 + "Elitserien_ParserZ.py")
        execute(mzn17 + "JapanEncoding.py", dzn_dir=pbs14 + "jp-encoding", dataparser=mzn17 + "JapanEncoding_ParserZ.py")
        execute(mzn13 + "Mario.py", dzn_dir=pbs14 + "mario", dataparser=mzn13 + "Mario_ParserZ.py")
        for v in [11, 12, 13, 20, 31]:
            execute(mzn14 + "MQueens.py", data=v)
        execute(mzn14 + "OpenShop.py", dzn_dir=pbs14 + "openshop", dataparser=mzn14 + "OpenShop_ParserZ.py")
        execute(mzn14 + "RoadConstruction.py", dzn_dir=pbs14 + "road-cons", dataparser=mzn14 + "RoadConstruction_ParserZ.py")
        execute(mzn12 + "ShipScheduling.py", dzn_dir=pbs14 + "ship-schedule", dataparser=mzn12 + "ShipScheduling_ParserZ.py")
        execute(mzn14 + "Smelt.py", dzn_dir=pbs14 + "smelt", dataparser=mzn14 + "Smelt_ParserZ.py")
        execute(mzn14 + "Spot5.py", variants=[None, "mini"], dzn_dir=pbs14 + "spot5", dataparser=mzn14 + "Spot5_ParserZ.py")  # long to generate
        execute(mzn14 + "StochasticFJSP.py", json_dir=pbs14 + "stochastic-fjsp")
        execute(mzn14 + "StochasticVRP.py", json_dir=pbs14 + "stochastic-vrp")
        execute(mzn18 + "Train.py", dzn_dir=pbs14 + "train", dataparser=mzn18 + "Train_ParserZ.py")
        execute(mzn14 + "TTPPV.py", dzn_dir=pbs14 + "traveling-tppv", dataparser=mzn14 + "TTPPV_ParserZ.py")


def m15():  # 1'30s
    options.suffix = "_m15"

    if new:
        executemzn("realistic", "CVRP", "_z", dzn_dir=pbs15 + "cvrp")
        executemzn("realistic", "FreePizza", "_z", dzn_dir=pbs15 + "freepizza")
        for t in [(4, 8), (4, 11), (10, 5), (13, 11), (19, 17)]:
            executemzn("academic", "GridColoring", data=t, dataformat="{:02d}-{:02d}")
        executemzn("realistic", "InstructionSelection", dzn_dir=pbs15 + "is")
        executemzn("crafted", "LargeScaleScheduling", "_z", dzn_dir=pbs15 + "largescheduling")
        executemzn("realistic", "Mapping", dzn_dir=pbs15 + "mapping")
        executemzn("crafted", "MultiKnapsack", "_z2", dzn_dir=pbs15 + "multi-knapsack")
        for v in [(10, 350, 100), (10, 100, 30), (10, 30, 9), (11, 22, 10), (13, 26, 6)]:
            executemzn("academic", "OPD", "_z", data=v, dataformat="{:02d}-{:03d}-{:03d}")
        executemzn("realistic", "OpenStacks", "_z", dzn_dir=pbs15 + "open_stacks")
        for v in [12, 13, 14, 15, 17]:
            executemzn("academic", "Perfect1Factorization", variants=[None, "dec"], data=v)
        executemzn("realistic", "Radiation", "_z", dzn_dir=pbs15 + "radiation")
        executemzn("realistic", "Roster", dzn_dir=pbs15 + "roster")
        executemzn("realistic", "Spot5", variants=[None, "mini"], dzn_dir=pbs15 + "spot5")
        executemzn("realistic", "TD_TSP", variants=[None, "plus"], dzn_dir=pbs15 + "tdtsp")
        for v in [10, 16, 22, 28, 37]:
            executemzn("academic", "Triangular", data=v)
    else:
        execute(mzn15 + "CVRP.py", dzn_dir=pbs15 + "cvrp", dataparser=mzn15 + "CVRP_ParserZ.py")
        execute(mzn15 + "FreePizza.py", dzn_dir=pbs15 + "freepizza", dataparser=mzn15 + "FreePizza_ParserZ.py")
        for t in [(4, 8), (4, 11), (10, 5), (13, 11), (19, 17)]:
            execute(mzn15 + "GridColoring.py", data=t, dataformat="{:02d}-{:02d}")
        execute(mzn15 + "Is.py", dzn_dir=pbs15 + "is", dataparser=mzn15 + "Is_ParserZ.py")  # rather long to generate
        execute(mzn18 + "LargeCumulative.py", dzn_dir=pbs15 + "largescheduling", dataparser=mzn18 + "LargeCumulative_ParserZ.py")
        execute(mzn18 + "Mapping.py", dzn_dir=pbs15 + "mapping", dataparser=mzn18 + "Mapping_ParserZ.py")
        execute(mzn15 + "MultiKnapsackG.py", dzn_dir=pbs15 + "multi-knapsack", dataparser=mzn15 + "MultiKnapsack_ParserZ.py")
        for v in [(10, 350, 100), (10, 100, 30), (10, 30, 9), (11, 22, 10), (13, 26, 6)]:
            execute(mzn15 + "OPD.py", data=v, dataformat="{:02d}-{:03d}-{:03d}")
        execute(mzn15 + "OpenStacks.py", dzn_dir=pbs15 + "open_stacks", dataparser=mzn15 + "OpenStacks_ParserZ.py")
        for v in [12, 13, 14, 15, 17]:
            execute(mzn15 + "Perfect1Factorization.py", variants=[None, "dec"], data=v)
        execute(mzn12 + "Radiation.py", dzn_dir=pbs15 + "radiation", dataparser=mzn12 + "Radiation_ParserZ.py")
        execute(mzn15 + "Roster.py", dzn_dir=pbs15 + "roster", dataparser=mzn15 + "Roster_ParserZ.py")
        execute(mzn14 + "Spot5.py", variants=[None, "mini"], dzn_dir=pbs15 + "spot5", dataparser=mzn14 + "Spot5_ParserZ.py")  # very long to generate
        execute(mzn15 + "TDTSP.py", variants=[None, "plus"], dzn_dir=pbs15 + "tdtsp", dataparser=mzn15 + "TDTSP_ParserZ.py")
        for v in [10, 16, 22, 28, 37]:
            execute(mzn15 + "Triangular.py", data=v)


def m16():  # 15s
    options.suffix = "_m16"

    if new:
        executemzn("realistic", "CarpetCutting", dzn_dir=pbs16 + "carpet-cutting")
        executemzn("realistic", "CELAR", dzn_dir=pbs16 + "celar")
        executemzn("realistic", "DepotPlacement", dzn_dir=pbs16 + "depot-placement")
        executemzn("realistic", "DC_MST", dzn_dir=pbs16 + "diameterc-mst")
        executemzn("realistic", "Elitserien", dzn_dir=pbs16 + "elitserien")
        executemzn("realistic", "Filters", dzn_dir=pbs16 + "filters")
        executemzn("realistic", "GBACP", "_z", dzn_dir=pbs16 + "gbac")
        executemzn("realistic", "GfdSchedule", "2", dzn_dir=pbs16 + "gfd-schedule")
        executemzn("realistic", "Mapping", dzn_dir=pbs16 + "mapping")
        executemzn("realistic", "MaximumDAG", dzn_dir=pbs16 + "maximum-dag")
        executemzn("realistic", "MRCPSP", dzn_dir=pbs16 + "mrcpsp")
        executemzn("crafted", "NFC", dzn_dir=pbs16 + "nfc")
        executemzn("realistic", "PrizeCollecting", "_z", dzn_dir=pbs16 + "prize-collecting")
        executemzn("realistic", "RCPSP_WET", dzn_dir=pbs16 + "rcpsp-wet")
        executemzn("realistic", "TPP", dzn_dir=pbs16 + "tpp")
        executemzn("realistic", "Zephyrus", dzn_dir=pbs16 + "zephyrus")
    else:
        execute(mzn16 + "CarpetCutting.py", dzn_dir=pbs16 + "carpet-cutting", dataparser=mzn16 + "CarpetCutting_ParserZ.py")
        execute(mzn13 + "Celar.py", dzn_dir=pbs16 + "celar", dataparser=mzn13 + "Celar_ParserZ.py")
        execute(mzn16 + "DepotPlacement.py", dzn_dir=pbs16 + "depot-placement", dataparser=mzn16 + "DepotPlacement_ParserZ.py")
        execute(mzn16 + "DiameterCMST.py", dzn_dir=pbs16 + "diameterc-mst", dataparser=mzn16 + "DiameterCMST_ParserZ.py")
        execute(mzn18 + "Elitserien.py", dzn_dir=pbs16 + "elitserien", dataparser=mzn18 + "Elitserien_ParserZ.py")
        execute(mzn13 + "Filters.py", dzn_dir=pbs16 + "filters", dataparser=mzn13 + "Filters_ParserZ.py")
        execute(mzn16 + "GeneralizedBACP.py", dzn_dir=pbs16 + "gbac", dataparser=mzn16 + "GeneralizedBACP_ParserZ.py")
        execute(mzn18 + "GfdSchedule2.py", dzn_dir=pbs16 + "gfd-schedule", dataparser=mzn18 + "GfdSchedule_ParserZ.py")  # one instance long to generate
        execute(mzn18 + "Mapping.py", dzn_dir=pbs16 + "mapping", dataparser=mzn18 + "Mapping_ParserZ.py")
        execute(mzn16 + "MaximumDag.py", dzn_dir=pbs16 + "maximum-dag", dataparser=mzn16 + "MaximumDag_ParserZ.py")
        execute(mzn16 + "MRCPSP.py", dzn_dir=pbs16 + "mrcpsp", dataparser=mzn16 + "MRCPSP_ParserZ.py")
        execute(mzn16 + "NFC.py", dzn_dir=pbs16 + "nfc", dataparser=mzn16 + "NFC_ParserZ.py")
        execute(mzn11 + "PrizeCollecting.py", dzn_dir=pbs16 + "prize-collecting", dataparser=mzn11 + "PrizeCollecting_ParserZ.py")
        execute(mzn16 + "RCPSPWet.py", dzn_dir=pbs16 + "rcpsp-wet", dataparser=mzn16 + "RCPSPWet_ParserZ.py")
        execute(mzn12 + "TPP.py", dzn_dir=pbs16 + "tpp", dataparser=mzn12 + "TPP_ParserZ.py")
        execute(mzn16 + "Zephyrus.py", dzn_dir=pbs16 + "zephyrus", dataparser=mzn16 + "Zephyrus_ParserZ.py")


def m17():  # 7'20s (two long CrosswordsOpt; many multiAgentPathFinding very long)
    options.suffix = "_m17"

    if new:
        executemzn("realistic", "Cargo", dzn_dir=pbs17 + "cargo")
        executemzn("realistic", "CityPosition", dzn_dir=pbs17 + "city-position")
        executemzn("realistic", "CommunityDetection", "_z1", dzn_dir=pbs17 + "community-detection")
        executemzn("recreational", "CrosswordsOpt", dzn_dir=pbs17 + "crosswords")
        executemzn("realistic", "GBACP", "_z", dzn_dir=pbs17 + "gbac")
        executemzn("realistic", "GroupSplitter", dzn_dir=pbs17 + "groupsplitter")
        executemzn("realistic", "HRC", dzn_dir=pbs17 + "hrc")
        executemzn("realistic", "JapanEncoding", dzn_dir=pbs17 + "jp-encoding")
        executemzn("realistic", "MultiAgentPathFinding", variants=[None, "table"], dzn_dir=pbs17 + "ma-path-finding")
        executemzn("recreational", "Mario", "_z", dzn_dir=pbs17 + "mario")
        for v in [(15, 350, 100), (13, 250, 80), (6, 50, 25), (6, 60, 30), (8, 28, 14)]:
            executemzn("academic", "OPD", data=v, dataformat="{:02d}-{:03d}-{:03d}")
        for v in [5, 7, 9, 11, 15]:
            executemzn("realistic", "OptCrypto", data=v, dataformat="{:02d}")
        executemzn("realistic", "RCPSP_WET", dzn_dir=pbs17 + "rcpsp-wet")
        executemzn("realistic", "RelToOntology", dzn_dir=pbs17 + "rel2onto")
        executemzn("realistic", "RoadConstruction", dzn_dir=pbs17 + "road-cons")
        executemzn("realistic", "SteelMillSlab", "_z", dzn_dir=pbs17 + "steelmillslab")
        executemzn("realistic", "TimeChangingGraphColoring", dzn_dir=pbs17 + "tc-graph-color")
        executemzn("realistic", "TD_TSP", variants=[None, "plus"], dzn_dir=pbs17 + "tdtsp")
        executemzn("realistic", "TTP_PV", dzn_dir=pbs17 + "traveling-tppv")
    else:
        execute(mzn18 + "Cargo.py", dzn_dir=pbs17 + "cargo", dataparser=mzn18 + "Cargo_ParserZ.py")
        execute(mzn17 + "CityPosition.py", dzn_dir=pbs17 + "city-position", dataparser=mzn17 + "CityPosition_ParserZ.py")
        execute(mzn17 + "CommunityDetection17.py", dzn_dir=pbs17 + "community-detection", dataparser=mzn17 + "CommunityDetection17_ParserZ.py")
        execute(mzn17 + "CrosswordsOpt.py", dzn_dir=pbs17 + "crosswords", dataparser=mzn17 + "CrosswordsOpt_ParserZ.py")
        execute(mzn16 + "GeneralizedBACP.py", dzn_dir=pbs17 + "gbac", dataparser=mzn16 + "GeneralizedBACP_ParserZ.py")
        execute(mzn19 + "GroupSplitter.py", dzn_dir=pbs17 + "groupsplitter", dataparser=mzn19 + "GroupSplitter_ParserZ.py")
        execute(mzn17 + "HRC.py", dzn_dir=pbs17 + "hrc", dataparser=mzn17 + "HRC_ParserZ.py")
        execute(mzn17 + "JapanEncoding.py", dzn_dir=pbs17 + "jp-encoding", dataparser=mzn17 + "JapanEncoding_ParserZ.py")
        execute(mzn17 + "MultiAgentPathFinding.py", variants=[None, "table"], dzn_dir=pbs17 + "ma-path-finding",
                dataparser=mzn17 + "MultiAgentPathFinding_ParserZ.py")
        execute(mzn13 + "Mario.py", dzn_dir=pbs17 + "mario", dataparser=mzn13 + "Mario_ParserZ.py")
        for v in [(15, 350, 100), (13, 250, 80), (6, 50, 25), (6, 60, 30), (8, 28, 14)]:
            execute(mzn15 + "OPD.py", data=v, dataformat="{:02d}-{:03d}-{:03d}")
        for v in [5, 7, 9, 11, 15]:
            execute(mzn21 + "OptCrypto.py", data=v, dataformat="{:02d}")
        execute(mzn16 + "RCPSPWet.py", dzn_dir=pbs17 + "rcpsp-wet", dataparser=mzn16 + "RCPSPWet_ParserZ.py")
        execute(mzn17 + "RelToOntology.py", dzn_dir=pbs17 + "rel2onto", dataparser=mzn17 + "RelToOntology_ParserZ.py")
        execute(mzn14 + "RoadConstruction.py", dzn_dir=pbs17 + "road-cons", dataparser=mzn14 + "RoadConstruction_ParserZ.py")
        execute(mzn17 + "SteelMillSlab.py", dzn_dir=pbs17 + "steelmillslab", dataparser=mzn17 + "SteelMillSlab_ParserZ.py")
        execute(mzn17 + "TimeChangingGraphColoring.py", dzn_dir=pbs17 + "tc-graph-color", dataparser=mzn17 + "TimeChangingGraphColoring_ParserZ.py")
        execute(mzn15 + "TDTSP.py", variants=[None, "plus"], dzn_dir=pbs17 + "tdtsp", dataparser=mzn15 + "TDTSP_ParserZ.py")
        execute(mzn14 + "TTPPV.py", dzn_dir=pbs17 + "traveling-tppv", dataparser=mzn14 + "TTPPV_ParserZ.py")


def m18():  # 8' (two big ProteinDesign rather long)
    options.suffix = "_m18"

    if new:
        executemzn("realistic", "Cargo", dzn_dir=pbs18 + "cargo")
        executemzn("realistic", "ConcertHall", dzn_dir=pbs18 + "concert-hall-cap")
        executemzn("realistic", "Elitserien", dzn_dir=pbs18 + "elitserien")
        executemzn("realistic", "GfdSchedule", "2", dzn_dir=pbs18 + "gfd-schedule")
        executemzn("crafted", "LargeScaleScheduling", "_z", dzn_dir=pbs18 + "largescheduling")
        executemzn("realistic", "Mapping", dzn_dir=pbs18 + "mapping")
        for v in [(5, 5), (4, 7), (7, 8), (6, 6), (9, 4)]:
            executemzn("academic", "Neighbours", data=v, variants=[None, "table"])
        executemzn("realistic", "OncallRostering", dzn_dir=pbs18 + "on-call-rostering")
        for v in [6, 8, 10, 12, 14]:
            executemzn("realistic", "OptCrypto", data=v, dataformat="{:02d}")
        executemzn("realistic", "ProteinDesign", dzn_dir=pbs18 + "proteindesign12")
        executemzn("realistic", "RACP", dzn_dir=pbs18 + "racp")
        executemzn("realistic", "SeatMoving", dzn_dir=pbs18 + "seat-moving")
        executemzn("realistic", "SteinerTree", dzn_dir=pbs18 + "steiner-tree")
        executemzn("realistic", "TeamAssignment", dzn_dir=pbs18 + "team-assignment")
        executemzn("realistic", "TestScheduling", dzn_dir=pbs18 + "test-scheduling")
        executemzn("realistic", "Train", dzn_dir=pbs18 + "train")
        executemzn("realistic", "VRP_LC", dzn_dir=pbs18 + "vrplc")
    else:
        execute(mzn18 + "Cargo.py", dzn_dir=pbs18 + "cargo", dataparser=mzn18 + "Cargo_ParserZ.py")
        execute(mzn18 + "ConcertHall.py", dzn_dir=pbs18 + "concert-hall-cap", dataparser=mzn18 + "ConcertHall_ParserZ.py")
        execute(mzn18 + "Elitserien.py", dzn_dir=pbs18 + "elitserien", dataparser=mzn18 + "Elitserien_ParserZ.py")
        execute(mzn18 + "GfdSchedule2.py", dzn_dir=pbs18 + "gfd-schedule", dataparser=mzn18 + "GfdSchedule_ParserZ.py")
        execute(mzn18 + "LargeCumulative.py", dzn_dir=pbs18 + "largescheduling", dataparser=mzn18 + "LargeCumulative_ParserZ.py")
        execute(mzn18 + "Mapping.py", dzn_dir=pbs18 + "mapping", dataparser=mzn18 + "Mapping_ParserZ.py")
        for v in [(5, 5), (4, 7), (7, 8), (6, 6), (9, 4)]:
            execute(mzn21 + "Neighbours.py", data=v, variants=[None, "table"])
        execute(mzn13 + "OncallRostering.py", dzn_dir=pbs18 + "on-call-rostering", dataparser=mzn13 + "OncallRostering_ParserZ.py")
        for v in [6, 8, 10, 12, 14]:
            execute(mzn21 + "OptCrypto.py", data=v, dataformat="{:02d}")
        execute(mzn18 + "ProteinDesign.py", dzn_dir=pbs18 + "proteindesign12", dataparser=mzn18 + "ProteinDesign_ParserZ.py")
        execute(mzn18 + "RACP.py", dzn_dir=pbs18 + "racp", dataparser=mzn18 + "RACP_ParserZ.py")
        execute(mzn21 + "SeatMoving.py", dzn_dir=pbs18 + "seat-moving", dataparser=mzn21 + "SeatMoving_ParserZ.py")
        execute(mzn18 + "SteinerTree.py", dzn_dir=pbs18 + "steiner-tree", dataparser=mzn18 + "SteinerTree_ParserZ.py")
        execute(mzn18 + "TeamAssignment.py", dzn_dir=pbs18 + "team-assignment", dataparser=mzn18 + "TeamAssignment_ParserZ.py")
        execute(mzn18 + "TestSchedulingM18.py", dzn_dir=pbs18 + "test-scheduling", dataparser=mzn18 + "TestSchedulingM18_ParserZ.py")
        execute(mzn18 + "Train.py", dzn_dir=pbs18 + "train", dataparser=mzn18 + "Train_ParserZ.py")
        execute(mzn18 + "VRPLC.py", dzn_dir=pbs18 + "vrplc", dataparser=mzn18 + "VRPLC_ParserZ.py")


def m19():  # 11' (RCPSPWetDiverse : very long (362s for j90) ; Nside rather long, especially, the instance hard-2000)
    options.suffix = "_m19"

    if new:
        executemzn("realistic", "ACCAP", dzn_dir=pbs19 + "accap")
        for t in [(6, 7, 8, 4, 15, 8, 12, 9), (50, 50, 50, 7, 35, 9, 10, 8), (6, 7, 8, 1, 31, 0, 6, 3), (118, 213, 124, 178, 3, 7, 5, 3),
                  (10, 10, 12, 5, 19, 1, 1, 1)]:
            executemzn("academic", "FoxGeeseCorn", data=t)
        executemzn("realistic", "GroupSplitter", dzn_dir=pbs19 + "groupsplitter")
        executemzn("realistic", "HRC", dzn_dir=pbs19 + "hrc")
        executemzn("realistic", "KidneyExchange", dzn_dir=pbs19 + "kidney-exchange")
        executemzn("realistic", "LotSizing", dzn_dir=pbs19 + "lot-sizing")
        executemzn("realistic", "MedianString", dzn_dir=pbs19 + "median-string")
        executemzn("crafted", "MultiKnapsack", "_z2", dzn_dir=pbs19 + "multi-knapsack")
        executemzn("realistic", "Nside", dzn_dir=pbs19 + "nside")
        executemzn("realistic", "PAX", dzn_dir=pbs19 + "ptv")
        executemzn("realistic", "RCPSP_WET_Diverse", dzn_dir=pbs19 + "rcpsp-wet-diverse", other_args="-dontuseauxcache")
        executemzn("realistic", "StackCutstock", dzn_dir=pbs19 + "stack-cuttingstock")
        executemzn("realistic", "SteelMillSlab", "_z", dzn_dir=pbs19 + "steelmillslab")
        executemzn("realistic", "StochasticVRP", json_dir=pbs19 + "stochastic-vrp")
        for v in [10, 17, 23, 29, 37]:
            executemzn("academic", "Triangular", data=v)
        executemzn("realistic", "Zephyrus", dzn_dir=pbs19 + "zephyrus")
    else:
        execute(mzn19 + "Accap.py", dzn_dir=pbs19 + "accap", dataparser=mzn19 + "Accap_ParserZ.py")
        for t in [(6, 7, 8, 4, 15, 8, 12, 9), (50, 50, 50, 7, 35, 9, 10, 8), (6, 7, 8, 1, 31, 0, 6, 3), (118, 213, 124, 178, 3, 7, 5, 3),
                  (10, 10, 12, 5, 19, 1, 1, 1)]:
            execute(mzn19 + "FoxGeeseCorn.py", data=t)
        execute(mzn19 + "GroupSplitter.py", dzn_dir=pbs19 + "groupsplitter", dataparser=mzn19 + "GroupSplitter_ParserZ.py")
        execute(mzn17 + "HRC.py", dzn_dir=pbs19 + "hrc", dataparser=mzn17 + "HRC_ParserZ.py")
        execute(mzn19 + "KidneyExchange.py", dzn_dir=pbs19 + "kidney-exchange", dataparser=mzn19 + "KidneyExchange_ParserZ.py")
        execute(mzn19 + "LotSizing.py", dzn_dir=pbs19 + "lot-sizing", dataparser=mzn19 + "LotSizing_ParserZ.py")
        execute(mzn19 + "MedianString.py", dzn_dir=pbs19 + "median-string", dataparser=mzn19 + "MedianString_ParserZ.py")
        execute(mzn15 + "MultiKnapsackG.py", dzn_dir=pbs19 + "multi-knapsack", dataparser=mzn15 + "MultiKnapsack_ParserZ.py")
        execute(mzn19 + "Nside.py", dzn_dir=pbs19 + "nside", dataparser=mzn19 + "Nside_ParserZ.py")
        execute(mzn19 + "PAX.py", dzn_dir=pbs19 + "ptv", dataparser=mzn19 + "PAX_ParserZ.py")
        execute(mzn19 + "RCPSPWetDiverse.py", dzn_dir=pbs19 + "rcpsp-wet-diverse", dataparser=mzn19 + "RCPSPWetDiverse_ParserZ.py",
                other_args="-dontuseauxcache")
        execute(mzn19 + "StackCutstock.py", dzn_dir=pbs19 + "stack-cuttingstock", dataparser=mzn19 + "StackCutstock_ParserZ.py")
        execute(mzn17 + "SteelMillSlab.py", dzn_dir=pbs19 + "steelmillslab", dataparser=mzn17 + "SteelMillSlab_ParserZ.py")
        execute(mzn14 + "StochasticVRP.py", json_dir=pbs19 + "stochastic-vrp")
        for v in [10, 17, 23, 29, 37]:
            execute(mzn15 + "Triangular.py", data=v)
        execute(mzn16 + "Zephyrus.py", dzn_dir=pbs19 + "zephyrus", dataparser=mzn16 + "Zephyrus_ParserZ.py")


def m20():  # 12' (StableGoods : very long)
    options.suffix = "_m20"

    if new:
        executemzn("realistic", "BnnPlanner", dzn_dir=pbs20 + "bnn-planner", other_args="-dontuseauxcache")
        executemzn("realistic", "CableTreeWiring", dzn_dir=pbs20 + "cable_tree_wiring")
        executemzn("realistic", "CollectiveConstruction", dzn_dir=pbs20 + "collaborative-construction", other_args="-dontuseauxcache")
        executemzn("realistic", "GBACP", "_z", dzn_dir=pbs20 + "gbac")
        executemzn("realistic", "Hoist", dzn_dir=pbs20 + "hoist")
        executemzn("realistic", "InstructionSelection", dzn_dir=pbs20 + "is")
        executemzn("realistic", "LotSizing", dzn_dir=pbs20 + "lot-sizing")
        executemzn("realistic", "MinimalDecisionSets", dzn_dir=pbs20 + "minimal-decision-sets")
        for v in [10, 16, 17, 20, 21]:
            executemzn("academic", "Perfect1Factorization", variants=[None, "dec"], data=v)
        executemzn("realistic", "PillarsPlanks", dzn_dir=pbs20 + "pillars-and-planks")
        executemzn("realistic", "RACP", dzn_dir=pbs20 + "racp")
        executemzn("realistic", "Radiation", "_z", dzn_dir=pbs20 + "radiation")
        executemzn("realistic", "SdnChain", dzn_dir=pbs20 + "sdn-chain")
        executemzn("realistic", "SkillAllocation", dzn_dir=pbs20 + "skill-allocation")
        executemzn("realistic", "StableGoods", variants=[None, "table"], dzn_dir=pbs20 + "stable-goods", other_args="-dontuseauxcache")
        executemzn("realistic", "Tower", variants=[None, "any"], dzn_dir=pbs20 + "tower_challenge")
    else:
        execute(mzn20 + "BnnPlanner.py", dzn_dir=pbs20 + "bnn-planner", dataparser=mzn20 + "BnnPlanner_ParserZ.py", other_args="-dontuseauxcache")
        execute(mzn20 + "CableTreeWiring.py", dzn_dir=pbs20 + "cable_tree_wiring", dataparser=mzn20 + "CableTreeWiring_ParserZ.py")
        execute(mzn20 + "CollectiveConstruction.py", dzn_dir=pbs20 + "collaborative-construction", dataparser=mzn20 + "CollectiveConstruction_ParserZ.py",
                other_args="-dontuseauxcache")
        execute(mzn16 + "GeneralizedBACP.py", dzn_dir=pbs20 + "gbac", dataparser=mzn16 + "GeneralizedBACP_ParserZ.py")
        execute(mzn20 + "Hoist.py", dzn_dir=pbs20 + "hoist", dataparser=mzn20 + "Hoist_ParserZ.py")
        execute(mzn15 + "Is.py", dzn_dir=pbs20 + "is", dataparser=mzn15 + "Is_ParserZ.py")
        execute(mzn19 + "LotSizing.py", dzn_dir=pbs20 + "lot-sizing", dataparser=mzn19 + "LotSizing_ParserZ.py")
        execute(mzn20 + "MinimalDecisionSets.py", dzn_dir=pbs20 + "minimal-decision-sets", dataparser=mzn20 + "MinimalDecisionSets_ParserZ.py")
        for v in [10, 16, 17, 20, 21]:
            execute(mzn15 + "Perfect1Factorization.py", variants=[None, "dec"], data=v)
        execute(mzn20 + "PillarsPlanks.py", dzn_dir=pbs20 + "pillars-and-planks", dataparser=mzn20 + "PillarsPlanks_ParserZ.py")
        execute(mzn18 + "RACP.py", dzn_dir=pbs20 + "racp", dataparser=mzn18 + "RACP_ParserZ.py")
        execute(mzn12 + "Radiation.py", dzn_dir=pbs20 + "radiation", dataparser=mzn12 + "Radiation_ParserZ.py")
        execute(mzn20 + "SdnChain.py", dzn_dir=pbs20 + "sdn-chain", dataparser=mzn20 + "SdnChain_ParserZ.py", other_args="-dontuseauxcache")
        execute(mzn20 + "SkillAllocation.py", dzn_dir=pbs20 + "skill-allocation", dataparser=mzn20 + "SkillAllocation_ParserZ.py")
        execute(mzn20 + "StableGoods.py", variants=[None, "table"], dzn_dir=pbs20 + "stable-goods", dataparser=mzn20 + "StableGoods_ParserZ.py",
                other_args="-dontuseauxcache")
        execute(mzn20 + "Tower.py", variants=[None, "any"], dzn_dir=pbs20 + "tower_challenge", dataparser=mzn20 + "Tower_ParserZ.py")


def m21():  # 5'30  (1 Neighbours instance very long)
    options.suffix = "_m21"

    if new:
        executemzn("realistic", "ATSP", dzn_dir=pbs21 + "ATSP")
        executemzn("realistic", "CarpetCutting", dzn_dir=pbs21 + "carpet-cutting")
        executemzn("realistic", "CommunityDetection", json_dir=pbs21 + "community-detection-rnd")
        executemzn("realistic", "JavaRouting", dzn_dir=pbs21 + "java-routing")
        executemzn("realistic", "Mapping", dzn_dir=pbs21 + "mapping")
        for v in [(9, 14), (40, 50), (20, 19), (4, 4), (4, 9)]:
            executemzn("academic", "Neighbours", data=v, variants=[None, "table"], dataformat="{:02d}-{:02d}")
        for v in [1, 2, 3, 4, 13]:
            executemzn("realistic", "OptCrypto", data=v, dataformat="{:02d}")
        for v in [12, 14, 17, 18, 22]:
            executemzn("academic", "Perfect1Factorization", variants=[None, "dec"], data=v)
        for v in [8, 11, 25, 40, 50]:
            executemzn("academic", "PeacableQueens", data=v, dataformat="{:02d}")
        executemzn("realistic", "PhysicianSchedule", dzn_dir=pbs21 + "physician-scheduling")
        executemzn("realistic", "SeatMoving", dzn_dir=pbs21 + "seat-moving")
        executemzn("realistic", "CVRP_TW", json_dir=pbs21 + "vrp-submission")
        executemzn("realistic", "WMSC", dzn_dir=pbs21 + "wmsmc-int")
    else:
        execute(mzn21 + "ATSP.py", dzn_dir=pbs21 + "ATSP", dataparser=mzn21 + "ATSP_ParserZ.py")
        execute(mzn16 + "CarpetCutting.py", dzn_dir=pbs21 + "carpet-cutting", dataparser=mzn16 + "CarpetCutting_ParserZ.py")
        execute(mzn21 + "CommunityDetection.py", json_dir=pbs21 + "community-detection-rnd")
        execute(mzn13 + "JavaRouting.py", dzn_dir=pbs21 + "java-routing", dataparser=mzn13 + "JavaRouting_ParserZ.py")
        execute(mzn18 + "Mapping.py", dzn_dir=pbs21 + "mapping", dataparser=mzn18 + "Mapping_ParserZ.py")
        for v in [(9, 14), (40, 50), (20, 19), (4, 4), (4, 9)]:
            execute(mzn21 + "Neighbours.py", data=v, variants=[None, "table"], dataformat="{:02d}-{:02d}")
        for v in [1, 2, 3, 4, 13]:
            execute(mzn21 + "OptCrypto.py", data=v, dataformat="{:02d}")
        for v in [12, 14, 17, 18, 22]:
            execute(mzn15 + "Perfect1Factorization.py", variants=[None, "dec"], data=v)
        for v in [8, 11, 25, 40, 50]:
            execute(mzn21 + "PeacableQueens.py", data=v, dataformat="{:02d}")
        execute(mzn21 + "PhysicianSchedule.py", dzn_dir=pbs21 + "physician-scheduling", dataparser=mzn21 + "PhysicianSchedule_ParserZ.py")
        execute(mzn21 + "SeatMoving.py", dzn_dir=pbs21 + "seat-moving", dataparser=mzn21 + "SeatMoving_ParserZ.py")
        execute(mzn21 + "VrpSubmission.py", json_dir=pbs21 + "vrp-submission")
        execute(mzn21 + "WMSC.py", dzn_dir=pbs21 + "wmsmc-int", dataparser=mzn21 + "WMSC_ParserZ.py")


def m22():  # 11' (MultiAgentPathFinding: long and 1 instance discarded, as pb with an assert:
    # g16_p10_a30.dzn with broken assert all(agent[0] != agent[1] for agent in agents) ; RosterSickness: long)
    options.suffix = "_m22"

    if new:
        executemzn("realistic", "ACCAP", dzn_dir=pbs22 + "accap")
        executemzn("realistic", "ArithmeticTarget", json_dir=pbs22 + "arithmetic-target")
        executemzn("recreational", "Blocks", dzn_dir=pbs22 + "blocks-world")
        executemzn("realistic", "DC_MST", dzn_dir=pbs22 + "diameterc-mst")
        for t in [(8, 3), (9, 5), (11, 5), (13, 5), (25, 4)]:
            executemzn("academic", "GeneralizedPeacableQueens", data=t, dataformat="{:02d}-{:01d}")
        executemzn("realistic", "GfdSchedule", "2", dzn_dir=pbs22 + "gfd-schedule")
        executemzn("realistic", "MultiAgentPathFinding", variants=[None, "table"], dzn_dir=pbs22 + "ma-path-finding")
        executemzn("crafted", "NFC", dzn_dir=pbs22 + "nfc")
        executemzn("realistic", "RosterSickness", dzn_dir=pbs22 + "roster-sickness")
        executemzn("realistic", "Spot5", variants=[None, "mini"], dzn_dir=pbs22 + "spot5")
        executemzn("recreational", "SudokuOpt", dzn_dir=pbs22 + "sudoku_opt")
        executemzn("realistic", "TeamAssignment", dzn_dir=pbs22 + "team-assignment")
        executemzn("realistic", "Tower", variants=[None, "any"], dzn_dir=pbs22 + "tower")
        executemzn("realistic", "TTP_PV", dzn_dir=pbs22 + "traveling-tppv")
        for v in [10, 18, 24, 30, 39]:
            executemzn("academic", "Triangular", data=v)
        executemzn("realistic", "Vaccine", dzn_dir=pbs22 + "vaccine")
        executemzn("realistic", "Wordpress", dzn_dir=pbs22 + "wordpress")
    else:
        execute(mzn19 + "Accap.py", dzn_dir=pbs22 + "accap", dataparser=mzn19 + "Accap_ParserZ.py")
        execute(mzn22 + "ArithmeticTarget.py", json_dir=pbs22 + "arithmetic-target")
        execute(mzn22 + "Blocks.py", dzn_dir=pbs22 + "blocks-world", dataparser=mzn22 + "Blocks_ParserZ.py")
        execute(mzn16 + "DiameterCMST.py", dzn_dir=pbs22 + "diameterc-mst", dataparser=mzn16 + "DiameterCMST_ParserZ.py")
        for t in [(8, 3), (9, 5), (11, 5), (13, 5), (25, 4)]:
            execute(mzn22 + "GeneralizedPeacableQueens.py", data=t, dataformat="{:02d}-{:01d}")
        execute(mzn18 + "GfdSchedule2.py", dzn_dir=pbs22 + "gfd-schedule", dataparser=mzn18 + "GfdSchedule_ParserZ.py")
        execute(mzn17 + "MultiAgentPathFinding.py", variants=[None, "table"], dzn_dir=pbs22 + "ma-path-finding",
                dataparser=mzn17 + "MultiAgentPathFinding_ParserZ.py")
        execute(mzn16 + "NFC.py", dzn_dir=pbs22 + "nfc", dataparser=mzn16 + "NFC_ParserZ.py")
        execute(mzn22 + "RosterSickness.py", dzn_dir=pbs22 + "roster-sickness", dataparser=mzn22 + "RosterSickness_ParserZ.py")
        execute(mzn14 + "Spot5.py", variants=[None, "mini"], dzn_dir=pbs22 + "spot5", dataparser=mzn14 + "Spot5_ParserZ.py")
        execute(mzn22 + "SudokuOpt.py", dzn_dir=pbs22 + "sudoku_opt", dataparser=mzn22 + "SudokuOpt_ParserZ.py")
        execute(mzn18 + "TeamAssignment.py", dzn_dir=pbs22 + "team-assignment", dataparser=mzn18 + "TeamAssignment_ParserZ.py")
        execute(mzn20 + "Tower.py", variants=[None, "any"], dzn_dir=pbs22 + "tower", dataparser=mzn20 + "Tower_ParserZ.py")
        execute(mzn14 + "TTPPV.py", dzn_dir=pbs22 + "traveling-tppv", dataparser=mzn14 + "TTPPV_ParserZ.py")
        for v in [10, 18, 24, 30, 39]:
            execute(mzn15 + "Triangular.py", data=v)
        execute(mzn22 + "Vaccine.py", dzn_dir=pbs22 + "vaccine", dataparser=mzn22 + "Vaccine_ParserZ.py")
        execute(mzn22 + "Wordpress.py", dzn_dir=pbs22 + "wordpress", dataparser=mzn22 + "Wordpress_ParserZ.py")


def mcsp():  # 8'30 (but pb with the variant 'det' of PentominoesSazenz: to be fixed)
    if new:
        options.suffix = "_m08"
        for t in [(2, 3), (2, 7), (2, 8), (2, 9), (2, 10), (3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8)]:
            executemzn("academic", "DeBruijn", data=t, dataformat="{:01d}-{:02d}")
        for v in [20, 40, 60, 80, 100, 150, 200, 300, 400, 500]:
            executemzn("academic", "NaiveMagicSequence", data=v, dataformat="{:03d}")
        executemzn("recreational", "Pentominoes", "1", dzn_dir=pbs08 + "pentominoes-int")
        for v in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
            executemzn("academic", "QuasiGroup", "_z", data=v, dataformat="{:02d}")
        for t in [(4, 4), (8, 4), (8, 8)]:
            executemzn("academic", "SearchStress", data=t)
        for v in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            executemzn("academic", "SlowConvergence", data=v, dataformat="{:04d}")

        options.suffix = "_m09"
        executemzn("recreational", "Blackhole", "_z", dzn_dir=pbs09 + "blackhole")
        executemzn("recreational", "Fillomino", "_z", dzn_dir=pbs09 + "fillomino")
        executemzn("recreational", "Nonogram", "_z", dzn_dir=pbs09 + "nonogram")
        for v in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            executemzn("academic", "PropStress", data=v, dataformat="{:04d}")
        for t in [(5, 1), (9, 0), (12, 1), (14, 0), (15, 1), (19, 0), (22, 1), (24, 0)]:
            executemzn("realistic", "RectPacking", "_z", data=t, dataformat="{:02d}-{:01d}")

        options.suffix = "_m10"
        # NB: CostasArray not introduced because largely the same instances as in 2011
        executemzn("recreational", "SolitaireBattleship", "_z", dzn_dir=pbs10 + "solbat")
        executemzn("realistic", "WWTPP", "_z", dzn_dir=pbs10 + "wwtpp-real")

        options.suffix = "_m11"
        executemzn("recreational", "Blackhole", "_z", dzn_dir=pbs11 + "black-hole")
        for v in [14, 15, 16, 17, 18]:
            executemzn("academic", "CostasArray", "_z", data=v)
        executemzn("recreational", "Fillomino", "_z", dzn_dir=pbs11 + "fillomino")
        executemzn("recreational", "Nonogram", "_z", dzn_dir=pbs11 + "nonogram")
        # NB: Pentominoes not introduced because same instances as in 2013
        executemzn("recreational", "SolitaireBattleship", "_z", dzn_dir=pbs11 + "solbat")
        executemzn("realistic", "WWTPP", "_z", dzn_dir=pbs11 + "wwtpp-real")

        options.suffix = "_m12"
        executemzn("recreational", "Amaze", "_z2", dzn_dir=pbs12 + "amaze2")
        executemzn("recreational", "Nonogram", "_z", dzn_dir=pbs12 + "nonogram")
        executemzn("recreational", "SolitaireBattleship", "_z", dzn_dir=pbs12 + "solbat")

        options.suffix = "_m13"
        executemzn("recreational", "Blackhole", "_z", dzn_dir=pbs13 + "black-hole")
        for v in [99, 143, 202, 395, 478]:
            executemzn("academic", "NaiveMagicSequence", data=v, dataformat="{:03d}")
        executemzn("recreational", "Nonogram", "_z", dzn_dir=pbs13 + "nonogram")
        executemzn("recreational", "Pentominoes", "1", dzn_dir=pbs13 + "pentominoes-int")
        executemzn("crafted", "Rubik", dzn_dir=pbs13 + "rubik")

        options.suffix = "_m14"
        executemzn("recreational", "Amaze", "_z3", dzn_dir=pbs14 + "amaze")
        executemzn("recreational", "Fillomino", "_z", dzn_dir=pbs14 + "fillomino")
        executemzn("crafted", "MultiKnapsack", "_z1", dzn_dir=pbs14 + "multi-knapsack")
        for t in [(18, 1), (21, 0), (22, 0), (23, 0), (26, 0)]:
            executemzn("realistic", "RectPacking", "_z", data=t, dataformat="{:02d}-{:01d}")
        executemzn("recreational", "SolitaireBattleship", "_z", dzn_dir=pbs14 + "solbat")

        options.suffix = "_m15"
        for v in [16, 17, 18, 19, 20]:
            executemzn("academic", "CostasArray", "_z", data=v)
        for v in [83, 176, 207, 269, 396]:
            executemzn("academic", "NaiveMagicSequence", data=v, dataformat="{:03d}")

        options.suffix = "_m16"
        for t in [(5, 11, 128), (5, 14, 128), (5, 16, 128), (5, 17, 128), (7, 10, 192)]:
            executemzn("realistic", "Cryptanalysis", data=t)
        executemzn("recreational", "SolitaireBattleship", "_z", dzn_dir=pbs16 + "solbat")

        options.suffix = "_m18"
        executemzn("realistic", "RotatingWorkforce1", dzn_dir=pbs18 + "rotating-workforce")
        executemzn("realistic", "Soccer", dzn_dir=pbs18 + "soccer-computational")

        options.suffix = "_m19"
        executemzn("recreational", "Amaze", "_z3", dzn_dir=pbs19 + "amaze")
        executemzn("realistic", "RotatingWorkforce1", dzn_dir=pbs19 + "rotating-workforce")

        options.suffix = "_m20"
        executemzn("recreational", "Pentominoes", "2", dzn_dir=pbs20 + "pentominoes")
        executemzn("realistic", "Soccer", dzn_dir=pbs20 + "soccer-computational")
        for v in [(8, 8), (12, 12), (21, 21), (29, 29), (30, 30)]:
            executemzn("academic", "Whirlpool", data=v, dataformat="{:02d}")

        options.suffix = "_m21"
        for t in [(3, 97), (4, 75), (4, 97), (5, 50), (6, 50)]:
            executemzn("academic", "Monomatch", data=t)
        executemzn("recreational", "PentominoesZayenz", variants=[None],
                   # variants=[None, "det"],  # TODO: pb to be fixed with the function that makes a deterministic copy
                   dzn_dir=pbs21 + "pentominoes-zayenz")
        executemzn("recreational", "PerfectSquare", json_dir=pbs21 + "perfect_square")
        for t in [(2, 7, 21), (3, 3, 11), (3, 4, 8), (4, 4, 10), (6, 6, 7)]:
            executemzn("academic", "SteinerSystems", data=t, dataformat="{:01d}-{:01d}-{:02d}")

        options.suffix = "_m22"
        executemzn("realistic", "RotatingWorkforce2", dzn_dir=pbs22 + "rotating-workforce-scheduling")

    else:
        options.suffix = "_m08"
        for t in [(2, 3), (2, 7), (2, 8), (2, 9), (2, 10), (3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8)]:
            execute(mzn08 + "DeBruijn.py", data=t, dataformat="{:01d}-{:02d}")
        for v in [20, 40, 60, 80, 100, 150, 200, 300, 400, 500]:
            execute(mzn13 + "NaiveMagicSequence.py", data=v, dataformat="{:03d}")
        execute(mzn11 + "Pentominoes.py", dzn_dir=pbs08 + "pentominoes-int", dataparser=mzn11 + "Pentominoes_ParserZ.py")
        for v in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
            execute(mzn08 + "QuasiGroup7.py", data=v, dataformat="{:02d}")
        for t in [(4, 4), (8, 4), (8, 8)]:
            execute(mzn08 + "SearchStress.py", data=t)
        for v in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            execute(mzn08 + "SlowConvergence.py", data=v, dataformat="{:04d}")

        options.suffix = "_m09"
        execute(mzn11 + "Blackhole.py", dzn_dir=pbs09 + "blackhole", dataparser=mzn11 + "Blackhole_ParserZ.py")
        execute(mzn14 + "Fillomino.py", dzn_dir=pbs09 + "fillomino", dataparser=mzn14 + "Fillomino_ParserZ.py")
        execute(mzn11 + "Nonogram.py", dzn_dir=pbs09 + "nonogram", dataparser=mzn11 + "Nonogram_ParserZ.py")
        for v in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            execute(mzn09 + "PropStress.py", data=v, dataformat="{:04d}")
        for t in [(5, 1), (9, 0), (12, 1), (14, 0), (15, 1), (19, 0), (22, 1), (24, 0)]:
            execute(mzn14 + "RectPacking.py", data=t, dataformat="{:02d}-{:01d}")

        options.suffix = "_m10"
        # NB: CostasArray not introduced because largely the same instances as in 2011
        execute(mzn12 + "Solbat.py", dzn_dir=pbs10 + "solbat", dataparser=mzn12 + "Solbat_ParserZ.py")
        execute(mzn11 + "WwtppReal.py", dzn_dir=pbs10 + "wwtpp-real", dataparser=mzn11 + "WwtppReal_ParserZ.py")

        options.suffix = "_m11"
        execute(mzn11 + "Blackhole.py", dzn_dir=pbs11 + "black-hole", dataparser=mzn11 + "Blackhole_ParserZ.py")
        for v in [14, 15, 16, 17, 18]:
            execute(mzn15 + "CostasArray.py", data=v)
        execute(mzn14 + "Fillomino.py", dzn_dir=pbs11 + "fillomino", dataparser=mzn14 + "Fillomino_ParserZ.py")
        execute(mzn11 + "Nonogram.py", dzn_dir=pbs11 + "nonogram", dataparser=mzn11 + "Nonogram_ParserZ.py")
        # NB: Pentominoes not introduced because same instances as in 2013
        execute(mzn12 + "Solbat.py", dzn_dir=pbs11 + "solbat", dataparser=mzn12 + "Solbat_ParserZ.py")
        execute(mzn11 + "WwtppReal.py", dzn_dir=pbs11 + "wwtpp-real", dataparser=mzn11 + "WwtppReal_ParserZ.py")

        options.suffix = "_m12"
        execute(mzn12 + "Amaze2.py", dzn_dir=pbs12 + "amaze2", dataparser=mzn12 + "Amaze_ParserZ.py")
        execute(mzn11 + "Nonogram.py", dzn_dir=pbs12 + "nonogram", dataparser=mzn11 + "Nonogram_ParserZ.py")
        execute(mzn12 + "Solbat.py", dzn_dir=pbs12 + "solbat", dataparser=mzn12 + "Solbat_ParserZ.py")

        options.suffix = "_m13"
        execute(mzn11 + "Blackhole.py", dzn_dir=pbs13 + "black-hole", dataparser=mzn11 + "Blackhole_ParserZ.py")
        for v in [99, 143, 202, 395, 478]:
            execute(mzn13 + "NaiveMagicSequence.py", data=v, dataformat="{:03d}")
        execute(mzn11 + "Nonogram.py", dzn_dir=pbs13 + "nonogram", dataparser=mzn11 + "Nonogram_ParserZ.py")
        execute(mzn11 + "Pentominoes.py", dzn_dir=pbs13 + "pentominoes-int", dataparser=mzn11 + "Pentominoes_ParserZ.py")
        execute(mzn13 + "Rubik.py", dzn_dir=pbs13 + "rubik", dataparser=mzn13 + "Rubik_ParserZ.py")

        options.suffix = "_m14"
        execute(mzn14 + "Amaze3.py", dzn_dir=pbs14 + "amaze", dataparser=mzn12 + "Amaze_ParserZ.py")
        execute(mzn14 + "Fillomino.py", dzn_dir=pbs14 + "fillomino", dataparser=mzn14 + "Fillomino_ParserZ.py")
        execute(mzn14 + "MultiKnapsackP.py", dzn_dir=pbs14 + "multi-knapsack", dataparser=mzn15 + "MultiKnapsack_ParserZ.py")
        for t in [(18, 1), (21, 0), (22, 0), (23, 0), (26, 0)]:
            execute(mzn14 + "RectPacking.py", data=t)
        execute(mzn12 + "Solbat.py", dzn_dir=pbs14 + "solbat", dataparser=mzn12 + "Solbat_ParserZ.py")

        options.suffix = "_m15"
        for v in [16, 17, 18, 19, 20]:
            execute(mzn15 + "CostasArray.py", data=v)
        for v in [83, 176, 207, 269, 396]:
            execute(mzn13 + "NaiveMagicSequence.py", data=v, dataformat="{:03d}")

        options.suffix = "_m16"
        for t in [(5, 11, 128), (5, 14, 128), (5, 16, 128), (5, 17, 128), (7, 10, 192)]:
            execute(mzn16 + "Cryptanalysis.py", data=t)
        execute(mzn12 + "Solbat.py", dzn_dir=pbs16 + "solbat", dataparser=mzn12 + "Solbat_ParserZ.py")

        options.suffix = "_m18"
        execute(mzn18 + "RotatingWorkforce.py", dzn_dir=pbs18 + "rotating-workforce", dataparser=mzn18 + "RotatingWorkforce_ParserZ.py")
        execute(mzn20 + "Soccer.py", dzn_dir=pbs18 + "soccer-computational", dataparser=mzn20 + "Soccer_ParserZ.py")

        options.suffix = "_m19"
        execute(mzn14 + "Amaze3.py", dzn_dir=pbs19 + "amaze", dataparser=mzn12 + "Amaze_ParserZ.py")
        execute(mzn18 + "RotatingWorkforce.py", dzn_dir=pbs19 + "rotating-workforce", dataparser=mzn18 + "RotatingWorkforce_ParserZ.py")

        options.suffix = "_m20"
        execute(mzn20 + "PentominoesInt.py", dzn_dir=pbs20 + "pentominoes", dataparser=mzn20 + "PentominoesInt_ParserZ.py")
        execute(mzn20 + "Soccer.py", dzn_dir=pbs20 + "soccer-computational", dataparser=mzn20 + "Soccer_ParserZ.py")
        for v in [(8, 8), (12, 12), (21, 21), (29, 29), (30, 30)]:
            execute(mzn20 + "Whirlpool.py", data=v, dataformat="{:02d}")

        options.suffix = "_m21"
        for t in [(3, 97), (4, 75), (4, 97), (5, 50), (6, 50)]:
            execute(mzn21 + "Monomatch.py", data=t)
        execute(mzn21 + "PentominoesZayenz.py", variants=[None],
                # variants=[None, "det"],   # TODO: pb to be fixed with the function that makes a deterministic copy
                dzn_dir=pbs21 + "pentominoes-zayenz", dataparser=mzn21 + "PentominoesZayenz_ParserZ.py")
        execute(mzn21 + "PerfectSquare.py", json_dir=pbs21 + "perfect_square")
        for t in [(2, 7, 21), (3, 3, 11), (3, 4, 8), (4, 4, 10), (6, 6, 7)]:
            execute(mzn21 + "SteinerSystems.py", data=t, dataformat="{:01d}-{:01d}-{:02d}")

        options.suffix = "_m22"
        execute(mzn22 + "RotatingWorkforce.py", dzn_dir=pbs22 + "rotating-workforce-scheduling", dataparser=mzn22 + "RotatingWorkforce_ParserZ.py")


t = [m08, m09, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22]

if seriesName.startswith("mzn") and seriesName[3:].isdigit():
    v = int(seriesName[3:])
    if v in range(8, 30):
        series(seriesName)
        t[v - 8]()

if series("mzncsp"):
    mcsp()

if seriesName == "allmzn":  # 64'
    for v in range(8, 23):  # for the moment, 23 not included
        seriesName = "mzn" + ("0" if v < 10 else "") + str(v)
        series(seriesName)
        t[v - 8]()
    seriesName = "mzncsp"
    series(seriesName)
    mcsp()

Compilation.done = True
