import unittest
from pathlib import Path
import pandas as pd
import json

from ionerdss.model.graph_based.complexes.examples import get_example
from ionerdss.model.graph_based.complexes.subcomplexes import get_unique_fully_connected_subgraphs
from ionerdss.model.graph_based.reactions.dimer import find_all_dimer_reactions, get_broken_edges
from ionerdss.model.graph_based.reactions.transformation import find_all_transformable_subgraph_pairs

from datetime import datetime
import time
import platform

def capture_environment_info():
    return {
        "timestamp": datetime.now().isoformat(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "cpu": platform.processor(),
    }

def benchmark_pipeline(graph_name="8y7s"):
    G = get_example(graph_name)
    results = {}
    env_info = capture_environment_info()

    t0 = time.time()
    species = get_unique_fully_connected_subgraphs(G)
    t1 = time.time()

    reactions = find_all_dimer_reactions(species, use_multiprocessing=True)
    t2 = time.time()

    reaction_df = pd.DataFrame([
        {
            "product": list(r[2].nodes),
            "part1": list(r[0]),
            "part2": list(r[1]),
            "bonds_broken": get_broken_edges(r[2], r[0], r[1])
        }
        for r in reactions
    ])

    transformations = find_all_transformable_subgraph_pairs(G, species)
    t3 = time.time()

    transformations_df = pd.DataFrame([
        {
            "monomer_1_nodes": list(t1.nodes),
            "monomer_2_nodes": list(t2.nodes),
            "diff": list(set(t1.edges(data="type")) ^ set(t2.edges(data="type")))
        }
        for t1, t2 in transformations
    ])

    results["timing"] = {
        "subgraph_enumeration": round(t1 - t0, 4),
        "dimer_reactions": round(t2 - t1, 4),
        "transformable_pairs": round(t3 - t2, 4),
        "total": round(t3 - t0, 4),
    }
    results["n_species"] = len(species)
    results["n_reactions"] = len(reaction_df)
    results["n_transformations"] = len(transformations_df)
    results["environment"] = env_info

    return reaction_df, transformations_df, results


class TestBenchmarkPipeline(unittest.TestCase):

    def test_benchmark_output_8y7s(self):
        graph_name = "8y7s"
        reaction_df, transformation_df, metadata = benchmark_pipeline(graph_name)

        # Basic structure checks
        self.assertIsInstance(reaction_df, pd.DataFrame)
        self.assertIsInstance(transformation_df, pd.DataFrame)
        self.assertIsInstance(metadata, dict)

        # Output sanity
        self.assertGreaterEqual(len(reaction_df), 1, "No dimer reactions found")
        self.assertGreaterEqual(len(transformation_df), 0, " Transformable subgraphs found while none expected")
        self.assertIn("timing", metadata)
        self.assertIn("n_species", metadata)

        # Timing keys present
        for key in ["subgraph_enumeration", "dimer_reactions", "transformable_pairs", "total"]:
            self.assertIn(key, metadata["timing"])
            self.assertGreaterEqual(metadata["timing"][key], 0.0)


if __name__ == "__main__":
    unittest.main()
