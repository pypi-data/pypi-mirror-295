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

from functools import wraps as _wraps

__all__ = [
    "assemble_func",
    "disassemble_func",
    "assemble_all",
    "disassemble",
    "join_packets",
    "split_packets",
    "valid_packet",
    "valid_packet_func",
]


def assemble_func(f):
    """Decorator for functions returning string representations
    with compatible TPPI packet format"""

    @_wraps(f)
    def wrapper(*arg, **kwarg):
        # Execute
        result = f(*arg, **kwarg)
        # Process the Tail
        return assemble_all(result)

    return wrapper


def disassemble_func(f):
    """Decorator for functions that provide a TPPI packet to be
    broken down into TPPI contents"""

    @_wraps(f)
    def wrapper(*arg, **kwarg):
        # Execute
        result = f(*arg, **kwarg)
        # Process tail
        return disassemble(result)

    return wrapper


def valid_packet_func(f):
    """Decorator for function that build TPPI packet.
    This returns both the result and its Validity"""

    @_wraps(f)
    def wrapper(*arg, **kwarg):
        # Execute
        result = f(*arg, **kwarg)
        # Process Tail
        return result, valid_packet(result)

    return wrapper


def assemble_all(*arg: list[str]) -> str:
    """Assemble all the TPPI Contents into TPPI Packet"""

    # Blank packet
    if len(arg) == 0:
        arg = [None]

    parts = []
    # Loop through the items and Filter for types
    for i in arg:
        # Check Type
        if isinstance(i, str):
            parts.append(i)
        elif isinstance(i, (list, tuple)):
            parts.extend([str(r) for r in i])
        elif isinstance(i, dict):
            parts.extend([str(r) for r in i.values()])
        elif i == None:
            parts.append("")
        else:
            raise TypeError("invalid type for assemble")

    # Filter
    parts = [r.replace("|", "\\x7C") for r in parts]
    parts = [r.replace("+", "\\x2B") for r in parts]
    # Join
    pack = "~|" + "|".join(parts) + "|~"
    # Final packet
    return pack


def disassemble(arg: str) -> list[str]:
    """Break a TPPI packet into its TPPI contents"""

    if (not isinstance(arg, str)) or len(arg) == 0:
        raise ValueError("No values provided to disassemble")

    src = str(arg)
    # Check Framing
    frame = src.startswith("~|") and src.endswith("|~")
    if not frame:
        raise ValueError("missing framing in data for disassemble")
    # Remove framing
    src = src.removeprefix("~|")
    src = src.removesuffix("|~")
    # Break into parts
    parts = src.split("|")
    # Check parts for '+'
    for p in parts:
        if "+" in p:
            raise ValueError("wrong + symbol in data for disassemble")
    # Filter parts
    parts = [r.replace("\\x7C", "|") for r in parts]
    parts = [r.replace("\\x2B", "+") for r in parts]
    # Processed parts
    return parts


def join_packets(*args) -> str:
    """Join multiple TPPI Packets together"""

    if len(args) == 0:
        raise ValueError("no values provided to join")

    parts = []
    # Check types
    for a in args:
        if isinstance(a, str):
            parts.append(a)
        elif isinstance(a, type([""])):
            parts.extend(a)
        else:
            raise TypeError("unknown data type passed to join")

    # Check packet Validity
    for p in parts:
        if not valid_packet(p):
            raise ValueError("invalid packet data can't join")
    # Join
    pack = "+".join(parts)
    # Completed Packet
    return pack


def split_packets(arg: str) -> list[str]:
    """Split the packet into multiple TPPI Packets"""

    if (not isinstance(arg, str)) or len(arg) == 0:
        raise ValueError("unknown data passed for split")

    # Split
    parts = arg.split("+")
    # Filter packets
    for p in parts:
        if not valid_packet(p):
            raise ValueError("invalid packet passed in split")
    # return the packets
    return parts


def valid_packet(pack: str) -> bool:
    """Check if the generated packet is indeed a valid TPPI packet"""

    if not isinstance(pack, str):
        return False

    frame = pack.startswith("~|") and pack.endswith("|~")
    if not frame:
        return False
    # Remove framing
    pack = pack.removeprefix("~|")
    pack = pack.removesuffix("|~")
    # Break into parts
    parts = pack.split("|")
    for p in parts:
        # Check for Invalid Chars
        if p.count("~") > 3:
            return False
        if p.count("+") > 0:
            return False

    # All checks pass
    return True
