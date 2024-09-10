# -*- coding: utf-8 -*-
#
#
#     ॐ भूर्भुवः स्वः
#     तत्स॑वि॒तुर्वरे॑ण्यं॒
#    भर्गो॑ दे॒वस्य॑ धीमहि।
#   धियो॒ यो नः॑ प्रचो॒दया॑त्॥
#
#
# बोसजी के द्वारा रचित टिप्पी अधिलेखन प्रकृया।
# ================================
#
# एक सरल संचार सहायक और संलग्न तंत्र।
#
# ~~~~~~~~~~~~~~~~~~~~~~~
# एक रचनात्मक भारतीय उत्पाद।
# ~~~~~~~~~~~~~~~~~~~~~~~
#
# Sources
# --------
#
# https://github.com/boseji/pytppi
#
# License
# ----------
#
#   `tppi` stands for Tilde Pipe Plus Interface
#
#   Copyright (C) 2024 Abhijit Bose (aka. Boseji). All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   <http://www.apache.org/licenses/LICENSE-2.0>
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   SPDX short identifier: Apache-2.0
#

import unittest

# Fix Paths
import sys

sys.path.append("src")
sys.path.append("../src")

# Import the Target
from tppi import assemble_func, assemble_all, join_packets


class TestAssembleFunc(unittest.TestCase):
    """Test Collection for assemble decorator for TPPI"""

    def test_parts(self):
        """basic"""

        @assemble_func
        def parts():
            arr = []
            isNeeded = False
            fl = 2.43
            arr.append(f"Bool:{isNeeded}")
            arr.append(f"Float:{fl}")
            return arr

        self.assertEqual(parts(), "~|Bool:False|Float:2.43|~")

    def test_single(self):
        """Single Text"""

        @assemble_func
        def single():
            return "Hari Aum"

        self.assertEqual(single(), "~|Hari Aum|~")

    def test_mapper(self):
        """Map data type"""

        @assemble_func
        def mapper():
            return {"Provision": True, "Data": 13.5}

        self.assertEqual(mapper(), "~|True|13.5|~")

    def test_mixed_parts(self):
        """Mixed types in a list"""

        @assemble_func
        def mixed_parts():
            return ["Test", True, 17.34e-4]

        self.assertEqual(mixed_parts(), "~|Test|True|0.001734|~")

    def test_blank_data(self):
        """Blank data"""

        @assemble_func
        def blank():
            pass

        self.assertEqual(blank(), "~||~")

    def test_none_data(self):
        """None data"""

        @assemble_func
        def real_none():
            return None

        self.assertEqual(real_none(), "~||~")

    def test_special_chars(self):
        """with special characters"""

        @assemble_func
        def special_chars():
            return ["Table+3", "P1|P2"]

        self.assertEqual(special_chars(), "~|Table\\x2B3|P1\\x7CP2|~")

    def test_wrong(self):
        """wrong data"""

        @assemble_func
        def real_trouble():
            def tester():
                pass

            return tester

        with self.assertRaises(TypeError):
            real_trouble()

    def test_argument_1(self):
        """argument 1 data"""

        @assemble_func
        def real_arg1(arg):
            return arg

        self.assertEqual(real_arg1("Hari Aum"), "~|Hari Aum|~")

    def test_argument_2(self):
        """argument 2 data"""

        @assemble_func
        def real_arg1(arg):
            return arg

        self.assertEqual(
            real_arg1(["Hari Aum", "Tat Sat"]),
            "~|Hari Aum|Tat Sat|~",
        )

    def test_argument_3(self):
        """argument 3 data"""

        @assemble_func
        def real_arg1(arg):
            return arg

        self.assertEqual(
            real_arg1({1: "Hari Aum", 2: "Tat Sat"}),
            "~|Hari Aum|Tat Sat|~",
        )

    def test_argument_4(self):
        """argument 4 data"""

        @assemble_func
        def real_arg2(*args):
            return [a for a in args]

        self.assertEqual(
            real_arg2("Hari Aum", "Tat Sat"),
            "~|Hari Aum|Tat Sat|~",
        )


class TestAssembleAll(unittest.TestCase):
    """Test collection for assemble all function in TPPI"""

    def test_parts(self):
        """basic"""

        isNeeded = False
        fl = 2.43

        self.assertEqual(
            assemble_all(f"Bool:{isNeeded}", f"Float:{fl}"),
            "~|Bool:False|Float:2.43|~",
        )

    def test_single(self):
        """Single Text"""
        self.assertEqual(assemble_all("Hari Aum"), "~|Hari Aum|~")

    def test_mapper(self):
        """Map data type"""

        self.assertEqual(
            assemble_all({"Provision": True, "Data": 13.5}),
            "~|True|13.5|~",
        )

    def test_mixed_parts(self):
        """Mixed types in a list"""

        self.assertEqual(
            assemble_all(["Test", True, 17.34e-4]),
            "~|Test|True|0.001734|~",
        )

    def test_blank_data(self):
        """Blank data"""

        self.assertEqual(assemble_all(None), "~||~")

    def test_no_data(self):
        """No data"""

        self.assertEqual(assemble_all(), "~||~")

    def test_special_chars(self):
        """with special characters"""

        self.assertEqual(
            assemble_all(["Table+3", "P1|P2"]),
            "~|Table\\x2B3|P1\\x7CP2|~",
        )

    def test_wrong(self):
        """wrong data"""

        def real_tuple():
            return (1, 2)

        with self.assertRaises(TypeError):
            assemble_all(real_tuple)


class TestJoinPackets(unittest.TestCase):
    """Test set for the Join Packets feature of TPPI"""

    def test_basic1(self):
        """Basic assembly"""

        self.assertEqual(
            join_packets("~|Bool:False|Float:2.43|~", "~|Hari Aum|Tat Sat|~"),
            "~|Bool:False|Float:2.43|~+~|Hari Aum|Tat Sat|~",
        )

    def test_basic2(self):
        """Assembly passing as an array"""

        self.assertEqual(
            join_packets(["~|Bool:False|Float:2.43|~", "~|Hari Aum|Tat Sat|~"]),
            "~|Bool:False|Float:2.43|~+~|Hari Aum|Tat Sat|~",
        )

    def test_wrong1(self):
        """Failure passing as a Map"""

        with self.assertRaises(TypeError):
            join_packets(
                {1: "~|Bool:False|Float:2.43|~", 12.5: "~|Hari Aum|Tat Sat|~"}
            )

    def test_wrong2(self):
        """Failure passing None"""

        with self.assertRaises(TypeError):
            join_packets(None)

    def test_wrong3(self):
        """Failure passing nothing"""

        with self.assertRaises(ValueError):
            join_packets()

    def test_wrong4(self):
        """Failure passing blanks"""

        with self.assertRaises(ValueError):
            join_packets("", "")

    def test_wrong5(self):
        """Failure passing Blank Array"""

        with self.assertRaises(ValueError):
            join_packets(["", ""])

    def test_wrong6(self):
        """Failure passing None Array"""

        with self.assertRaises(ValueError):
            join_packets([None, None])

    def test_wrong7(self):
        """Failure passing Array with one wrong element"""

        with self.assertRaises(ValueError):
            join_packets(["~||~", 2, "~|Hari Aum|~"])

    def test_wrong8(self):
        """Failure passing Array with wrong symbols in element"""

        with self.assertRaises(ValueError):
            join_packets(["~|Jai|~", "~|~Hari~~Aum~|~Tat~Sat~|~"])

        with self.assertRaises(ValueError):
            join_packets(["~|Jai|~", "~|~Hari+~Aum~|~Tat~Sat~|~"])
