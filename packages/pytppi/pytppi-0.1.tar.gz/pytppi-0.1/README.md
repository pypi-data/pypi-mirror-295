>
> ॐ भूर्भुवः स्वः
>
> तत्स॑वि॒तुर्वरे॑ण्यं॒
>
> भर्गो॑ दे॒वस्य॑ धीमहि।
>
> धियो॒ यो नः॑ प्रचो॒दया॑त्॥
>

# बोसजी के द्वारा रचित टिप्पी अधिलेखन प्रकृया।

> एक सरल संचार सहायक और संलग्न तंत्र।
>

***एक रचनात्मक भारतीय उत्पाद।***

## `tppi` stands for Tilde Pipe Plus Interface

> A simple communication helper and enclosing mechanism called **`TPPI protocol`**.

There are two parts to this protocol:

- *Organization* - Build the compatible data representation called **`TPPI content`**.
- *Encapsulation* - Prepare a compatible packet with necessary safeguards called **`TPPI packet`**.

This is **`string oriented protocol`** with *special safeguards* for **`TPPI protocol`**.

The following symbols are considered special to **`TPPI protocol`**:

- `~` Tilde Symbol
- `|` Pipe Symbol
- `+` Plus Symbol

These *symbol are replaced* by the following as *safeguards* for **`TPPI packet`**:

- `|` converts to `\\x7C`
- `+` converts to `\\x2B`

These *symbols are replaced* for *safeguards* in data specified for **`TPPI contents`** :

- `~` converts to `%7E`
- `|` converts to `%7C`
- `+` converts to `%2B`

The **`TPPI protocol`** contains special annotations:

- `~|` is used to indicate the **`start`** of the **`TPPI Packet`**
- `|~` is used to indicate the **end** of the **`TPPI Packet`**
- `|` is used to separate the **`TPPI contents`** in a **`TPPI Packet`**
- `~` are used to organize the **`TPPI contents`** with Type, tags, & data.
- `~||~` indicates a **`TPPI packet`** *without any contents*
- `+` is used to join **`TPPI packets`** together.

Collection rule for **`TPPI packets`**:

- If **`TPPI packet`** are sent one at a time then no special addition is needed.
- In case *collection* of **`TPPI packets`** need to be sent then `+` symbol is used.

Rules for **`TPPI content`**:

- The *content mist be filtered* with necessary *safeguards*.
- **`Type Signature`**: Each **T`PPI content`** must have a **`Type Signature`** that tells what type of data it contains and helps in *Discovery process* later. In case no **`Type Signature`** is provided `UN` would be used to indicate `unknown` Type`.
- **`Type Signature`** can't be left blank and recommended to be added.
- **`Tag`**: Each **`TPPI content`** can have a string name or tag that can help better identify the data enclosed. This would later be used for *Discovery process*. This is an *Optional field* and can be omitted in the **`TPPI content`**.
- **`Data`**: The **`TPPI content`** encloses the data provided in *string form*, that can later be retrieved using the *Discovery process*.
- The fields **`Type Signature`**, *(optional)* **`Tag`** and **`Data`** are separated by `~` Symbol in a **`TPPI content`**.

**`TPPI Content Processes`**:

- **`Specify`**: In this process the **`Type Signature`**, *(optional)* **`Tag`** and **`Data`** are joined together in **`TPPI Content`** form. This follows the rules for **`TPPI content`**. This typically happens before preparing the **`TPPI packet`**.
- **`Discover`**: In this process the **`Type Signature`**, *(optional)* **`Tag`** and **`Data`** are recovered from the supplied **`TPPI Content`**. This follows the same rules for **`TPPI content`** in order to find the enclosed data. This is typically done after receiving the TPPI packet and getting the **`TPPI contents`**.

**`TPPI Packet Processes`**:

- **`Assemble`**: In this process the **`TPPI contents`** are *filtered* and *joined together* into a **`TPPI packet`** following respective rules. This however *should not be used* for Joining *multiple TPPI packets*.
- **`Disassemble`**: In this process the incoming **`TPPI packet`** is broken into into multiple **`TPPI contents`** with *filtering/safeguards* removed. This however *should not be used* directly on the *Incoming TPPI packet* as *it would not be able to split apart TPPI packets*.
- **`Join`**: This is the process of *Joining multiple packets* before sending over the **`combined TPPI packets`**.
- **`Split`**: This is process perform as soon as the **`TPPI packets`** are received. *Only after this the process* of *Disassembly can begin*.

*Background behind the name:*

> The name `tppi` has been taken from a story of an imaginative kid
> discovering the mysteries of the Universe and the world all around
> from a remote village in the heart of Karnataka, Bharat(India).
>

## कार्यविधि - Usage

Include into a project:

```sh
pip install pytppi
```

Usage in Transmitter Program:

```py
from datetime import datetime
from src.tppi import assemble_func, specify, disassemble, discover

@assemble_func
def build(timestamp:int, value:float):
    return [
        specify(f"{timestamp}","TS"),
        specify(f"{value}","F"),
    ]

if __name__ == "__main__":
    print("Transmit Packet")
    print(build(datetime.now().timestamp(),12.4))
    parts = disassemble('~|TS~1725869454.327236|F~12.4|~')
    parts = [discover(p) for p in parts]
    print("Found:", parts)
    for p in parts:
        if p[1] == 'TS':
            print("Time Stamp:", datetime.fromtimestamp(float(p[0])))
        elif p[1] == 'F':
            print("Value:", float(p[0]))
```

## Developer Note

In order to perform test and future development use the following process:

Make sure a virtual environment is created and activated already.

Install dependencies:

```sh
pip install -e .[dev]
```

This would install `black`, `build` and `coverage`.

To test out the code:

```sh
coverage run
coverage html
```

To build the project:

```sh
python -m build --wheel --sdist
```

To format the code:

```sh
black .
```

## License

`SPDX: Apache-2.0`

`tppi` stands for Tilde Pipe Plus Interface

Copyright (C) 2024 Abhijit Bose (aka. Boseji). All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
