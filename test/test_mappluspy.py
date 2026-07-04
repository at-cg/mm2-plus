import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mappluspy as mp

REF = str(ROOT / "test" / "MT-human.fa")
QRY = str(ROOT / "test" / "MT-orang.fa")


class TestMappluspy(unittest.TestCase):
    def test_version(self):
        self.assertIsInstance(mp.__version__, str)
        self.assertTrue(mp.__version__)

    def test_fastx_read(self):
        records = list(mp.fastx_read(QRY))
        self.assertGreater(len(records), 0)
        name, seq, qual = records[0]
        self.assertIsInstance(name, str)
        self.assertGreater(len(seq), 0)

    def test_aligner_from_file(self):
        aligner = mp.Aligner(REF, preset="map-ont")
        self.assertTrue(aligner)
        self.assertGreater(len(aligner.seq_names), 0)

    def test_map_produces_hits(self):
        aligner = mp.Aligner(REF, preset="map-ont", max_chain_skip=1000000)
        self.assertTrue(aligner)
        total_hits = 0
        for name, seq, qual in mp.fastx_read(QRY):
            for hit in aligner.map(seq):
                total_hits += 1
                self.assertLessEqual(hit.r_st, hit.r_en)
                self.assertLessEqual(hit.q_st, hit.q_en)
                self.assertIn(hit.strand, (-1, 1))
        self.assertGreater(total_hits, 0)

    def test_map_with_tags(self):
        aligner = mp.Aligner(REF, preset="map-ont")
        self.assertTrue(aligner)
        for name, seq, qual in mp.fastx_read(QRY):
            for hit in aligner.map(seq, cs=True, MD=True):
                self.assertIsNotNone(hit.cigar_str)
                self.assertIsNotNone(hit.cs)
                break
            break

    def test_in_memory_index(self):
        aligner = mp.Aligner(seq="ACGTACGTACGTACGTACGT", k=7, w=1)
        self.assertTrue(aligner)
        self.assertEqual(len(aligner.seq_names), 1)


if __name__ == "__main__":
    unittest.main()
