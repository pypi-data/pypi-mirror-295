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
from tppi import specify, discover, assemble_func, assemble_all


class TestSpecify(unittest.TestCase):
    """Test Set for Specify in TPPI"""

    def test_basic1(self):
        """signature with data"""

        self.assertEqual(
            specify("Hari Aum", "S"),
            "S~Hari Aum",
        )

    def test_basic2(self):
        """missing signature only tag"""

        self.assertEqual(
            specify("Hari Aum", tag="Verse"),
            "Hari Aum",
        )

    def test_basic3(self):
        """special symbols in data"""

        self.assertEqual(
            specify("+Hari~ Aum|"),
            "%2BHari%7E Aum%7C",
        )

    def test_basic4(self):
        """signature and tag with data"""

        self.assertEqual(
            specify("Hari Aum", "S", "Verse"),
            "S~Verse~Hari Aum",
        )

    def test_wrong1(self):
        """wrong data type"""

        with self.assertRaises(ValueError):
            specify(["Hari Aum", "S", "Verse"])

    def test_wrong2(self):
        """wrong Signature type"""

        with self.assertRaises(ValueError):
            specify("Hari Aum", 1)

    def test_wrong3(self):
        """wrong Tag type"""

        with self.assertRaises(ValueError):
            specify("Hari Aum", tag=1)

    def test_wrong4(self):
        """blank data"""

        with self.assertRaises(ValueError):
            specify("")

    def test_withAssembleFunc(self):
        """combo with Assemble Func"""

        @assemble_func
        def work():
            return specify("Hari Aum", "S")

        self.assertEqual(
            work(),
            "~|S~Hari Aum|~",
        )

    def test_withAssembleAll(self):
        """combo with Assemble All"""

        self.assertEqual(
            assemble_all(
                specify("Hari Aum", "S"),
                specify(str(True), "B", "field"),
            ),
            "~|S~Hari Aum|B~field~True|~",
        )


class TestDiscover(unittest.TestCase):
    """Test set for Discover in TPPI"""

    def test_basic1(self):
        """Simple discovery of Data and type"""

        self.assertEqual(
            discover("S~Hari Aum"),
            ("Hari Aum", "S", ""),
        )

    def test_basic2(self):
        """missing signature"""

        self.assertEqual(
            discover("Hari Aum"),
            ("Hari Aum", "", ""),
        )

    def test_basic3(self):
        """special symbols in data"""

        self.assertEqual(
            discover("%2BHari%7E Aum%7C"),
            ("+Hari~ Aum|", "", ""),
        )

    def test_basic4(self):
        """signature and tag with data"""

        self.assertEqual(
            discover("S~Verse~Hari Aum"),
            ("Hari Aum", "S", "Verse"),
        )

    def test_unknown_format(self):
        """wrong unknown format"""

        with self.assertRaises(ValueError):
            discover("S~Verse~Hari Aum~TatSat")

    def test_wrong_type(self):
        """wrong type"""

        with self.assertRaises(ValueError):
            discover(["S~Verse~Hari Aum"])

    def test_wrong_blank(self):
        """blank data"""

        with self.assertRaises(ValueError):
            discover("")
