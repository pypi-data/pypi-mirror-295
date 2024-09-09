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
from tppi import disassemble_func, disassemble, split_packets


class TestDisassembleFunc(unittest.TestCase):
    """Test Collection for Disassemble decorator for TPPI"""

    def test_parts(self):
        """parts disassembly"""

        @disassemble_func
        def process(values):
            return values

        self.assertEqual(
            process("~|Bool:False|Float:2.43|~"),
            ["Bool:False", "Float:2.43"],
        )

    def test_single(self):
        """Single Text"""

        @disassemble_func
        def single(value):
            return value

        self.assertEqual(single("~|Hari Aum|~"), ["Hari Aum"])

    def test_mapper(self):
        """multi type data"""

        @disassemble_func
        def mapper(values):
            return values

        self.assertEqual(mapper("~|True|13.5|~"), ["True", "13.5"])

    def test_blank_data(self):
        """Blank data"""

        @disassemble_func
        def blank(values):
            return values

        self.assertEqual(blank("~||~"), [""])

    def test_special_chars(self):
        """with special characters"""

        @disassemble_func
        def special_chars(val):
            return val

        self.assertEqual(
            special_chars("~|Table\\x2B3|P1\\x7CP2|~"),
            ["Table+3", "P1|P2"],
        )

    def test_none_param(self):
        """no param"""

        @disassemble_func
        def real_tuple():
            pass

        with self.assertRaises(ValueError):
            real_tuple()

    def test_frame(self):
        """frame issues"""

        @disassemble_func
        def real_tuple(value):
            return value

        with self.assertRaises(ValueError):
            real_tuple("~|True|13.5|")

    def test_wrong_type(self):
        """wrong type issues"""

        @disassemble_func
        def real_tuple(value):
            return value

        with self.assertRaises(ValueError):
            real_tuple(True)

    def test_wrong_symbol(self):
        """wrong symbol in packet issues"""

        @disassemble_func
        def real_tuple(value):
            return value

        with self.assertRaises(ValueError):
            real_tuple("~|Hari + Aum|Tat Sat|~")


class TestDisassemble(unittest.TestCase):
    """Test set to check Disassemble feature of TPPI"""

    def test_parts(self):
        """parts disassembly"""

        self.assertEqual(
            disassemble("~|Bool:False|Float:2.43|~"),
            ["Bool:False", "Float:2.43"],
        )

    def test_single(self):
        """Single Text"""

        self.assertEqual(disassemble("~|Hari Aum|~"), ["Hari Aum"])

    def test_mapper(self):
        """multi type data"""

        self.assertEqual(disassemble("~|True|13.5|~"), ["True", "13.5"])

    def test_blank_data(self):
        """Blank data"""

        self.assertEqual(disassemble("~||~"), [""])

    def test_special_chars(self):
        """with special characters"""
        self.assertEqual(
            disassemble("~|Table\\x2B3|P1\\x7CP2|~"),
            ["Table+3", "P1|P2"],
        )

    def test_frame(self):
        """frame issues"""

        with self.assertRaises(ValueError):
            disassemble("~|True|13.5|")

    def test_wrong_type(self):
        """wrong type issues"""

        with self.assertRaises(ValueError):
            disassemble(True)

    def test_wrong_type2(self):
        """wrong type issues2"""

        with self.assertRaises(ValueError):
            disassemble(["~||~", "~|Hare Krishna|~"])

    def test_wrong_symbol(self):
        """wrong symbol in packet issues"""

        with self.assertRaises(ValueError):
            disassemble("~|Hari + Aum|Tat Sat|~")


class TestSplitPacket(unittest.TestCase):
    """Test set for Split operation of TPPI"""

    def test_basic1(self):
        """Basic test for splitting"""

        self.assertEqual(
            split_packets("~||~+~|Hare Krishna|~"),
            ["~||~", "~|Hare Krishna|~"],
        )

    def test_wrong_type(self):
        """wrong type passed for splitting"""

        with self.assertRaises(ValueError):
            split_packets(["", "~|Hare Krishna|~"])

    def test_wrong_empty(self):
        """wrong empty data for splitting"""

        with self.assertRaises(ValueError):
            split_packets("")

    def test_wrong_packet(self):
        """wrong packet splitting"""

        with self.assertRaises(ValueError):
            split_packets("~||+~|Hare Krishna|~")
