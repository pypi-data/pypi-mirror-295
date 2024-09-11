import os
import sys
import platform
import json
import types

__version__ = "1.0.1"
sys.path.insert(0, os.path.dirname(__file__))

if platform.system() == "Windows":
    mypath = os.path.dirname(os.path.realpath(__file__))
    if mypath not in sys.path:
        sys.path.insert(0, mypath)
    os.add_dll_directory(mypath)

from .cpppart import cpppart as base
if base.use_pyxyz:
    from .pyxyz import Confpool, MolProxy
# from .pyutils import pyutils
import networkx as nx
import pyutils

DEG2RAD = 0.0174532925199432957692
RAD2DEG = 1 / DEG2RAD
H2KC = 627.509474063
KC2H = 1 / H2KC


# Factory of Molecule objects
def Molecule(sdf=None,
             graph_data=None,
             request_free=None,
             require_best_sequence=False,
             clear_feed=True):
    assert (sdf is not None) or (
        graph_data is not None
    ), "Either 'sdf' or 'graph_data' must be passed as keyword-args"
    assert (sdf is None) or (
        graph_data is None
    ), "'sdf' or 'graph_data' should not be specified simultaneously"

    # Clear feed for new molecule
    if clear_feed:
        base.clear_status_feed()

    m = base.Molecule()

    if request_free is not None:
        request_free = [(i - 1, j - 1) for i, j in request_free]
        m.set_requested_dofs(request_free)

    if require_best_sequence:
        m.require_best_sequence()

    if sdf is not None:
        assert isinstance(sdf,
                          str), "sdf must be an str object (name of your SDF)"
        m.sdf_constructor(sdf, nx, pyutils)
    else:  # elif graph_data is not None
        assert isinstance(
            graph_data,
            dict), "graph_data must be a dict (see README for details)"
        assert set(graph_data.keys()) == {
            'graph', 'fixed_dihedrals'
        }, "graph_data keys must be precisely 'graph' and 'fixed_dihedrals'"
        m.graph_constructor(graph_data, nx, pyutils)
    return m


def get_one_seed():
    return int.from_bytes(os.urandom(3), byteorder="big")


def create_seed_list(size):
    unique_set = set()
    result = []
    while len(result) < size:
        list_element = get_one_seed()
        if list_element not in unique_set:
            unique_set.add(list_element)
            result.append(list_element)
    return result


MCR_FLAGS_DESCRIPTIONS = {
    'total': {
        'ntries': "Number of sampling attempts in total"
    },
    'good': {
        'nsucc':
        "Successfull iterations of MCR with postoptimization (if it's enabled)",
    },
    'bad': {
        'nfail':
        "Cases of TLC unable to provide correct solutions (only incorrect ones)",
        'nzero': "Cases of zero IK solutions",
        'ngeom': "MCR sampling attempts didn't pass geometry validation",
        'nolap': "MCR sampling attempts didn't pass overlap checks",
        'npostopt_fail':
        "Crashed postoptimizations (BFGS unable to make a step, etc.)",
        'npostopt_more_steps':
        "Postoptimization unable to pass the overlap and validity requirements",
        'ndihedral_filtering':
        "Discarded due to violated configuration rules for dihedrals",
        'nrmsd_duplicate': "Discarded by RMSD filter",
    }
}


def mcr_result_to_list(result_data: dict) -> dict:
    result_descriptions = {}
    for section_name, section_cases in MCR_FLAGS_DESCRIPTIONS.items():
        result_descriptions[section_name] = {}
        for key, description in section_cases.items():
            if key in result_data:
                result_descriptions[section_name][description] = result_data[
                    key]
    return result_descriptions


def run_confsearch(
    mol,
    pool=None,
    rmsd_settings=None,
    postopt_settings=[],
    geometry_validation={},
    nthreads=1,
    max_conformers=None,
    max_tries=None,
    timelimit=None,
    filter=None,
    clear_feed=True,
):
    max_conformers = max_conformers if max_conformers is not None else -1
    max_tries = max_tries if max_tries is not None else -1
    timelimit = timelimit if timelimit is not None else -1

    # Check if all requrements are supported by the used library
    # Concerning 'nthreads'
    assert isinstance(nthreads, int), "'nthreads' must be interger"
    if nthreads == 1:
        assert base.use_mcr_singlethreaded, "The default single-threaded Monte-Carlo is not supported by the current build of Ringo"
    elif nthreads > 1:
        assert base.use_mcr_parallel, "Parallel Monte-Carlo is not supported by the current build of Ringo"
    else:
        raise RuntimeError("'nthreads' must be >= 1")
    if not base.use_postoptimization:
        assert (len(postopt_settings) == 0) or \
            (postopt_settings == [{'enabled': False}, {'enabled': False}]), \
            "Postoptimization is not supported by this build"
    # Concerning pool object and RMSD filtering settings
    if (pool is not None) or (rmsd_settings
                              is not None) or (filter
                                               is not None) or base.use_pyxyz:
        assert base.use_pyxyz, "Either 'pool', 'rmsd_settings' or 'filter' were specified but Pyxyz is not included in the current build"
        assert pool is not None, "'pool' for conformer storage must be provided"
        # Set default rmsd_settings
        if rmsd_settings is None or rmsd_settings == 'default':
            # Using default settings for RMSD filtering
            rmsd_settings = {
                'isomorphisms': {
                    'ignore_elements': ['HCarbon'],
                },
                'rmsd': {
                    'threshold': 0.2,
                    'mirror_match': True,
                }
            }
        assert isinstance(
            pool, base.Confpool), "Pool must be an instance of pyxyz.Confpool"
        assert isinstance(rmsd_settings,
                          dict), "'rmsd_settings' must be a dict"
        assert filter is None or isinstance(
            filter, types.FunctionType) or isinstance(
                filter, dict), "'filter' must be a function or dict"
    # Other execution options
    assert isinstance(max_conformers, int) and (
        max_conformers >= 1
        or max_conformers == -1), "Incorrect value of 'max_conformers' keyword"
    assert isinstance(
        max_tries, int) and (max_tries >= 1 or max_tries
                             == -1), "Incorrect value of 'max_tries' keyword"
    assert isinstance(
        timelimit, int) and (timelimit >= 1 or timelimit
                             == -1), "Incorrect value of 'timelimit' keyword"
    if max_conformers == -1 and max_tries == -1 and timelimit == -1:
        raise RuntimeError(
            "At least one keyword 'max_conformers', 'max_tries' or 'timelimit' must be provided. "
            "Otherwise, Monte-Carlo run has no condition for termination.")
    # Clear feed for confsearch run
    if clear_feed:
        base.clear_status_feed()

    # Assemble argument list for Monte-Carlo call
    arg_list = [mol]
    if base.use_pyxyz:
        # Options for conformer storage and filtering
        arg_list += [pool, filter, rmsd_settings]
    if base.use_postoptimization:
        arg_list.append(postopt_settings)
    if base.use_geometry_validation:
        arg_list.append(geometry_validation)
    if nthreads == 1:
        # Option for single-threaded runs
        arg_list.append(get_one_seed())
    else:
        # Options for parallel runs
        arg_list += [nthreads, create_seed_list(nthreads)]
    # Options for termination criteria
    arg_list += [max_conformers, max_tries, timelimit]
    # Non-C++ modules
    # if nthreads > 1:
    arg_list += [nx, pyutils]

    # Execute Monte-Carlo
    if nthreads == 1:
        res = base.mcr_confsearch(*arg_list)
    else:
        res = base.mcr_confsearch_parallel(*arg_list)

    return res


def cleanup():
    seqcache_path = os.path.join(os.getcwd(), pyutils.CACHE_FILE)
    if os.path.isfile(seqcache_path):
        os.remove(seqcache_path)
        # print(f"Removing cache file {seqcache_path}")


# Work with vdw radii controls
build_flags = base.build_flags
if base.use_overlap_detection:
    get_vdw_radii = base.get_vdw_radii
    set_vdw_radii = base.set_vdw_radii
    set_radius_multiplier = base.set_radius_multiplier

# Work with Ringo status feed
WARNING_CODES = base.warning_codes
for warning_code, warning_line in base.warning_codes.items():
    globals(
    )[warning_code] = warning_line  # Declares str variables IK_NOT_APPLIED, SUBOPTIMAL_SOLN_SEQ, UNMET_DOF_REQUEST, etc.
add_message_to_feed = base.add_message_to_feed
clear_status_feed = base.clear_status_feed


def get_status_feed(important_only=True):
    json_data = base.get_status_feed()
    parsed_data = [json.loads(item) for item in json_data]
    for item in parsed_data:
        item['important'] = '[important]' in item['subject']
        item['subject'] = item['subject'].replace('[important]', '')
        if len(item['atoms']) > 0:
            item['atoms'] = sorted([idx + 1 for idx in item['atoms']])
        else:
            del item['atoms']

    if important_only:
        return [item for item in parsed_data if item['important']]
    else:
        return parsed_data


# Summarising statistics for the molecule
def get_molecule_statistics(m):
    graph = m.molgraph_access()
    symbols = m.get_symbols()

    composition = set(symbols[atom] for atom in graph.nodes)
    composition = {element: 0 for element in composition}
    for atom in graph.nodes:
        composition[symbols[atom]] += 1

    temp_graph = nx.Graph()
    temp_graph.add_edges_from(graph.edges)
    molgraph_bridges = list(nx.bridges(temp_graph))
    temp_graph.remove_edges_from(molgraph_bridges)
    lone_nodes = []
    for node in temp_graph.nodes:
        if len(list(temp_graph.neighbors(node))) == 0:
            lone_nodes.append(node)
    temp_graph.remove_nodes_from(lone_nodes)
    num_cyclic_parts = len([x for x in nx.connected_components(temp_graph)])
    all_ring_atoms = list(temp_graph.nodes)

    mcb = [set(c) for c in nx.minimum_cycle_basis(graph)]
    num_cyclic_rotatable_bonds = 0
    num_rotatable_bonds = 0
    for vxA, vxB in graph.edges:
        if len(list(graph.neighbors(vxA))) > 1 and len(
                list(graph.neighbors(vxB))) > 1:
            num_rotatable_bonds += 1
            for ring_atoms in mcb:
                if vxA in ring_atoms and vxB in ring_atoms:
                    num_cyclic_rotatable_bonds += 1
                    break

    num_cyclic_dofs = 0
    dof_list, _ = m.get_ps()
    for sideA, atA, atB, sideB in dof_list:
        if atA in all_ring_atoms and atB in all_ring_atoms and \
                (atA, atB) not in molgraph_bridges and (atB, atA) not in molgraph_bridges:
            num_cyclic_dofs += 1

    result = {
        'composition':
        composition,
        'num_atoms':
        graph.number_of_nodes(),
        'num_heavy_atoms':
        len([atom for atom in graph.nodes if symbols[atom] != 'H']),
        'num_bonds':
        graph.number_of_edges(),
        'num_rotatable_bonds':
        num_rotatable_bonds,
        'num_cyclic_rotatable_bonds':
        num_cyclic_rotatable_bonds,
        'largest_macrocycle_size':
        max([len(item) for item in mcb]) if len(mcb) > 0 else 0,
        'n_flexible_rings':
        m.get_num_flexible_rings(),
        'n_rigid_rings':
        m.get_num_rigid_rings(),
        'num_dofs':
        len(dof_list),
        'num_cyclic_dofs':
        num_cyclic_dofs,
        'cyclomatic_number':
        graph.number_of_edges() - graph.number_of_nodes() + 1,
        'num_cyclic_parts':
        num_cyclic_parts,
    }
    return result
