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

__all__ = [
    "specify",
    "discover",
]


def specify(data: str, typeSignature: str = "", tag: str = "") -> str:
    """Specify data for TPPI content"""
    spec = []
    # Filter Data
    if (not isinstance(data, str)) or len(data) == 0:
        raise ValueError("Problem in data for specify")
    if not isinstance(tag, str):
        raise ValueError("Problem in tag for specify")
    if not isinstance(typeSignature, str):
        raise ValueError("Problem in signature for specify")
    # Add parts available in order
    if len(typeSignature) > 0:
        spec.append(typeSignature)
        if len(tag) > 0:
            spec.append(tag)
    spec.append(data)
    # Filter
    spec = [r.replace("~", "%7E") for r in spec]
    spec = [r.replace("|", "%7C") for r in spec]
    spec = [r.replace("+", "%2B") for r in spec]
    # Join all
    full = "~".join(spec)
    # Return Specification
    return full


def discover(arg: str) -> tuple:
    """Discover from a TPPI Content"""
    data = ""
    typeSignature = ""
    tag = ""
    if (not isinstance(arg, str)) or len(arg) == 0:
        raise ValueError("Problem in data for discovery")
    # Get Content
    content = arg.split("~")
    # Filter
    content = [r.replace("%7E", "~") for r in content]
    content = [r.replace("%7C", "|") for r in content]
    content = [r.replace("%2B", "+") for r in content]
    # Discover
    if len(content) == 3:
        typeSignature = content[0]
        tag = content[1]
        data = content[2]
    elif len(content) == 2:
        typeSignature = content[0]
        data = content[1]
    elif len(content) == 1:
        data = content[0]
    else:
        raise ValueError("unknown number of items to discover")
    # distribute
    return data, typeSignature, tag
