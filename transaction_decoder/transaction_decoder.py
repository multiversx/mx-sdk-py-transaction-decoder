import base64
import binascii
import re
from typing import Any, Dict, List, Optional

from multiversx_sdk_core.bech32 import bech32_encode, convertbits


class TransactionToDecode:
    def __init__(self):
        self.sender: str = ""
        self.receiver: str = ""
        self.data: str = ""
        self.value: str = "0"


class TransactionMetadata:
    def __init__(self):
        self.sender: str = ""
        self.receiver: str = ""
        self.value: int = 0
        self.function_name: Optional[str] = None
        self.function_args: Optional[List[str]] = None
        self.transfers: Optional[List[TransactionMetadataTransfer]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "value": self.value,
            "function_name": self.function_name,
            "function_args": self.function_args,
            "transfers": [x.to_dict() for x in self.transfers]
            if self.transfers
            else None,
        }


class TransactionMetadataTransfer:
    def __init__(self):
        self.properties: Optional[TokenTransferProperties] = None
        self.value: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "properties": self.properties.to_dict() if self.properties else None,
        }


class TokenTransferProperties:
    def __init__(self):
        self.token: Optional[str] = None
        self.collection: Optional[str] = None
        self.identifier: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "token": self.token,
            "collection": self.collection,
            "identifier": self.identifier,
        }


class TransactionDecoder:
    def getTransactionMetadata(
        self, transaction: TransactionToDecode
    ) -> TransactionMetadata:
        metadata = self.get_normal_transaction_metadata(transaction)

        esdtMetadata = self.getEsdtTransactionMetadata(metadata)
        if esdtMetadata:
            return esdtMetadata

        nftMetadata = self.get_nft_transfer_metadata(metadata)
        if nftMetadata:
            return nftMetadata

        multiMetadata = self.get_multi_transfer_metadata(metadata)
        if multiMetadata:
            return multiMetadata

        return metadata

    def get_normal_transaction_metadata(
        self, transaction: TransactionToDecode
    ) -> TransactionMetadata:
        metadata = TransactionMetadata()
        metadata.sender = transaction.sender
        metadata.receiver = transaction.receiver
        metadata.value = int(transaction.value)

        if transaction.data:
            decoded_data = self.base64Decode(transaction.data)

            data_components = decoded_data.split("@")

            args = data_components[1:]
            if all(self.is_smart_contract_argument(x) for x in args):
                metadata.function_name = data_components[0]
                metadata.function_args = args

        return metadata

    def get_nft_transfer_metadata(
        self, metadata: TransactionMetadata
    ) -> Optional[TransactionMetadata]:
        if metadata.sender != metadata.receiver:
            return None

        if metadata.function_name != "ESDTNFTTransfer":
            return None

        args = metadata.function_args
        if not args:
            return None

        if len(args) < 4:
            return None

        if not self.is_address_valid(args[3]):
            return None

        collection_identifier = self.hex_to_string(args[0])
        nonce = args[1]
        value = self.hex_to_big_int(args[2])
        receiver = self.bech32_encode(args[3])

        result = TransactionMetadata()
        result.sender = metadata.sender
        result.receiver = receiver
        result.value = value
        result.transfers = []

        if len(args) > 4:
            result.function_name = self.hex_to_string(args[4])
            result.function_args = args[5:]

        tx_metadata = TransactionMetadataTransfer()
        tx_metadata.value = value
        tx_metadata.properties = TokenTransferProperties()
        tx_metadata.properties.collection = collection_identifier
        tx_metadata.properties.identifier = f"{collection_identifier}-{nonce}"
        result.transfers.append(tx_metadata)

        return result

    def get_multi_transfer_metadata(
        self,
        metadata: TransactionMetadata,
    ) -> Optional[TransactionMetadata]:
        if metadata.sender != metadata.receiver:
            return None

        if metadata.function_name != "MultiESDTNFTTransfer":
            return None

        args = metadata.function_args
        if not args:
            return None

        if len(args) < 3:
            return None

        if not self.is_address_valid(args[0]):
            return None

        receiver = self.bech32_encode(args[0])
        transfer_count = self.hex_to_number(args[1])

        result = TransactionMetadata()
        if not result.transfers:
            result.transfers = []

        index = 2
        for _ in range(transfer_count):
            identifier = self.hex_to_string(args[index])
            index += 1
            nonce = args[index]
            index += 1
            value = self.hex_to_big_int(args[index])
            index += 1

            if nonce:
                tx_metadata = TransactionMetadataTransfer()

                tx_metadata.value = value
                tx_metadata.properties = TokenTransferProperties()
                tx_metadata.properties.collection = identifier
                tx_metadata.properties.identifier = f"{identifier}-{nonce}"

                result.transfers.append(tx_metadata)
            else:
                tx_metadata = TransactionMetadataTransfer()

                tx_metadata.value = value
                tx_metadata.properties = TokenTransferProperties()
                tx_metadata.properties.collection = identifier

                result.transfers.append(tx_metadata)

        result.sender = metadata.sender
        result.receiver = receiver

        if len(args) > index:
            result.function_name = self.hex_to_string(args[index])
            index += 1
            result.function_args = args[index:]
            index += 1

        return result

    def getEsdtTransactionMetadata(
        self, metadata: TransactionMetadata
    ) -> Optional[TransactionMetadata]:
        if metadata.function_name != "ESDTTransfer":
            return None

        args = metadata.function_args
        if not args:
            return None

        if len(args) < 2:
            return None

        token_identifier = self.hex_to_string(args[0])
        value = self.hex_to_big_int(args[1])

        result = TransactionMetadata()

        result.sender = metadata.sender
        result.receiver = metadata.receiver
        result.transfers = []

        if len(args) > 2:
            result.function_name = self.hex_to_string(args[2])
            result.function_args = args[3:]

        tx_metadata = TransactionMetadataTransfer()
        tx_metadata.value = value

        tx_metadata.properties = TokenTransferProperties()
        tx_metadata.properties.collection = token_identifier
        tx_metadata.properties.identifier = token_identifier

        result.transfers.append(tx_metadata)
        result.value = value

        return result

    def is_address_valid(self, address: str) -> bool:
        return len(binascii.unhexlify(address)) == 32

    def is_smart_contract_argument(self, arg: str) -> bool:
        if not self.is_hex(arg):
            return False
        if len(arg) % 2 != 0:
            return False
        return True

    def is_hex(self, value: str) -> bool:
        return not bool(re.search("[^a-f0-9]", value, re.IGNORECASE))

    def base64_to_hex(self, str: str) -> str:
        return binascii.hexlify(base64.b64decode(str)).decode("ascii")

    def hex_to_string(self, hex: str) -> str:
        return bytes.fromhex(hex).decode("ascii")

    def hex_to_big_int(self, hex: str) -> int:
        if not hex:
            return 0
        return int(hex, 16)

    def base64Encode(self, s: str) -> str:
        return base64.b64encode(s.encode("utf-8")).decode("utf-8")

    def base64Decode(self, s: str) -> str:
        return base64.b64decode(s.encode("utf-8")).decode("utf-8")

    def hex_to_number(self, hex: str) -> int:
        return int(hex, 16)

    def bech32_encode(self, address: str) -> str:
        pub_key = bytes.fromhex(address)
        words = convertbits(pub_key, 8, 5)
        return bech32_encode("erd", words)