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

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

from coin_addressing import addresser

from snarkcoin_processor.account import account_creation
from snarkcoin_processor.snarkcoin_payload import SnarkcoinPayload
from snarkcoin_processor.snarkcoin_state import SnarkcoinState


class SnarkcoinHandler(TransactionHandler):

    @property
    def family_name(self):
        return addresser.FAMILY_NAME

    @property
    def namespaces(self):
        return [addresser.NS]

    @property
    def family_versions(self):
        return ['1.0']

    def apply(self, transaction, context):

        state = SnarkcoinState(context=context, timeout=2)
        payload = SnarkcoinPayload(payload=transaction.payload)

        if payload.is_create_account():
            account_creation.handle_account_creation(
                payload.create_account(),
                header=transaction.header,
                state=state)

        else:
            raise InvalidTransaction("Transaction payload type unknown.")
