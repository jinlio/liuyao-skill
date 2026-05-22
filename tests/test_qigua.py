import importlib.util
import json
import random
import re
import unittest
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("qigua", ROOT / "scripts" / "qigua.py")
qigua = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qigua)


def result_for(inputs):
    return qigua.build_result(qigua.load_gua_data(), qigua.divine_manual(inputs))


class QiguaTests(unittest.TestCase):
    def test_lower_trigram_mapping_uses_bottom_to_top_lines(self):
        upper_qian = [1, 1, 1]
        cases = [
            ([1, 1, 1], "乾为天", "乾"),
            ([1, 1, 2], "天泽履", "兑"),
            ([1, 2, 1], "天火同人", "离"),
            ([1, 2, 2], "天雷无妄", "震"),
            ([2, 1, 1], "天风姤", "巽"),
            ([2, 1, 2], "天水讼", "坎"),
            ([2, 2, 1], "天山遁", "艮"),
            ([2, 2, 2], "天地否", "坤"),
        ]

        for lower, expected_name, expected_lower in cases:
            with self.subTest(lower=lower):
                result = result_for(lower + upper_qian)
                self.assertEqual(result["ben_gua"]["name"], expected_name)
                self.assertEqual(result["ben_gua"]["lower"], expected_lower)

    def test_upper_trigram_mapping_uses_bottom_to_top_lines(self):
        lower_qian = [1, 1, 1]
        cases = [
            ([1, 1, 1], "乾为天", "乾"),
            ([1, 1, 2], "泽天夬", "兑"),
            ([1, 2, 1], "火天大有", "离"),
            ([1, 2, 2], "雷天大壮", "震"),
            ([2, 1, 1], "风天小畜", "巽"),
            ([2, 1, 2], "水天需", "坎"),
            ([2, 2, 1], "山天大畜", "艮"),
            ([2, 2, 2], "地天泰", "坤"),
        ]

        for upper, expected_name, expected_upper in cases:
            with self.subTest(upper=upper):
                result = result_for(lower_qian + upper)
                self.assertEqual(result["ben_gua"]["name"], expected_name)
                self.assertEqual(result["ben_gua"]["upper"], expected_upper)

    def test_moving_yao_changes_to_bian_gua(self):
        result = result_for([3, 1, 1, 1, 1, 1])

        self.assertEqual(result["ben_gua"]["name"], "乾为天")
        self.assertEqual(result["bian_gua"]["name"], "天风姤")
        self.assertEqual(result["moving_yao"], ["初九"])

    def test_shicao_generates_six_valid_lines(self):
        random.seed(20260522)
        yaos = qigua.divine_shicao()

        self.assertEqual(len(yaos), 6)
        for yao in yaos:
            self.assertIn(yao["shicao_value"], {6, 7, 8, 9})
            self.assertIn(yao["type"], {"老阴", "少阳", "少阴", "老阳"})

    def test_shicao_line_value_uses_classic_change_odds(self):
        with patch.object(qigua.random, "random", side_effect=[0.1, 0.1, 0.1]):
            self.assertEqual(qigua.shicao_line_value(), 9)

        with patch.object(qigua.random, "random", side_effect=[0.9, 0.9, 0.9]):
            self.assertEqual(qigua.shicao_line_value(), 6)

    def test_manual_input_errors_are_catchable(self):
        with self.assertRaises(ValueError):
            qigua.divine_manual([1, 2, 3])

        with self.assertRaises(ValueError):
            qigua.divine_manual([1, 2, 3, 0, 1, 4])

    def test_lookup_table_is_derived_from_hexagram_records(self):
        data = qigua.load_gua_data()
        expected_lookup = {
            key: entry["name"]
            for key, entry in data["hexagrams"].items()
        }

        self.assertEqual(data["lookup"], expected_lookup)
        for key, entry in data["hexagrams"].items():
            self.assertEqual(data["lookup"][key], entry["name"])

    def test_reference_headings_cover_all_hexagrams(self):
        data = json.loads((ROOT / "assets" / "gua-data.json").read_text(encoding="utf-8"))
        expected_names = {entry["name"] for entry in data["hexagrams"].values()}

        for rel_path in ["references/guaci-full.md", "references/yaoci-full.md"]:
            text = (ROOT / rel_path).read_text(encoding="utf-8")
            headings = set(re.findall(r"^## (.+)$", text, flags=re.M))
            self.assertEqual(headings, expected_names)


if __name__ == "__main__":
    unittest.main()
