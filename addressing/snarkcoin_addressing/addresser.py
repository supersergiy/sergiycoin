# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import enum
import hashlib


FAMILY_NAME = 'snarkcoin'


NS = hashlib.sha512(FAMILY_NAME.encode()).hexdigest()[:6]



class AccountSpace(enum.IntEnum):
    START = 0
    STOP = 256

@enum.unique
class AddressSpace(enum.IntEnum):
    ACCOUNT = 0

    OTHER_FAMILY = 100


def _hash(identifier):
    return hashlib.sha512(identifier.encode()).hexdigest()


def _compress(address, start, stop):
    return "%.2X".lower() % (int(address, base=16) % (stop - start) + start)

def make_account_address(account_id):
    full_hash = _hash(account_id)

    return NS + _compress(
        full_hash,
        AccountSpace.START,
        AccountSpace.STOP) + full_hash[:62]


def _contains(num, space):
    return space.START <= num < space.STOP


def address_is(address):

    if address[:len(NS)] != NS:
        return AddressSpace.OTHER_FAMILY

    infix = int(address[6:8], 16)

    if _contains(infix, AccountSpace):
        result = AddressSpace.ACCOUNT

    return result
