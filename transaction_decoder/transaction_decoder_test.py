from transaction_decoder.transaction_decoder import TransactionDecoder, TransactionToDecode


class TestTransactionDecoder:
    def test_nft_smart_contract_call(self) -> None:
        tx_to_decode = TransactionToDecode()
        tx_to_decode.sender = (
            "erd18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzwsvx7e85"
        )
        tx_to_decode.receiver = (
            "erd18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzwsvx7e85"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = "RVNEVE5GVFRyYW5zZmVyQDRjNGI0ZDQ1NTgyZDYxNjE2MjM5MzEzMEAyZmI0ZTlAZTQwZjE2OTk3MTY1NWU2YmIwNGNAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEA3Mzc3NjE3MDVmNmM2YjZkNjU3ODVmNzQ2ZjVmNjU2NzZjNjRAMGIzNzdmMjYxYzNjNzE5MUA="

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "erd18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzwsvx7e85"
        )
        assert (
            metadata.receiver
            == "erd1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qxct34s"
        )
        assert metadata.value == 1076977887712805212893260
        assert metadata.function_name == "swap_lkmex_to_egld"
        assert metadata.function_args == ["0b377f261c3c7191", ""]
        if metadata.transfers:
            assert metadata.transfers[0].value == 1076977887712805212893260
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.collection == "LKMEX-aab910"
                assert (
                    metadata.transfers[0].properties.identifier == "LKMEX-aab910-2fb4e9"
                )
    
    def test_sc_call(self):
        tx_to_decode = TransactionToDecode()

        tx_to_decode.sender = (
            "erd1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fqvyjnq2"
        )
        tx_to_decode.receiver = (
            "erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = (
            "d2l0aGRyYXdHbG9iYWxPZmZlckAwMTczZDA="
        )

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "erd1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fqvyjnq2"
        )
        assert (
            metadata.receiver
            == "erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th"
        )
        assert (
            metadata.function_name
            == "withdrawGlobalOffer"
        )
        assert (
            metadata.function_args
            == ['0173d0']
        )

    def test_multi_esdt_nft_transfer(self):
        tx_to_decode = TransactionToDecode()
        tx_to_decode.sender = (
            "erd1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqxj43r9"
        )
        tx_to_decode.receiver = (
            "erd1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqxj43r9"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = "TXVsdGlFU0RUTkZUVHJhbnNmZXJAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEAwMkA0YzRiNGQ0NTU4MmQ2MTYxNjIzOTMxMzBAMmZlM2IwQDA5Yjk5YTZkYjMwMDI3ZTRmM2VjQDRjNGI0ZDQ1NTgyZDYxNjE2MjM5MzEzMEAzMTAyY2FAMDEyNjMwZTlhMjlmMmY5MzgxNDQ5MUA3Mzc3NjE3MDVmNmM2YjZkNjU3ODVmNzQ2ZjVmNjU2NzZjNjRAMGVkZTY0MzExYjhkMDFiNUA="

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "erd1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqxj43r9"
        )
        assert (
            metadata.receiver
            == "erd1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qxct34s"
        )
        assert metadata.value == 0
        assert metadata.function_name == "swap_lkmex_to_egld"
        assert metadata.function_args == [
            "0ede64311b8d01b5",
            "",
        ]
        if metadata.transfers:
            assert len(metadata.transfers) == 2
            assert metadata.transfers[0].value == 45925073746530627023852
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.collection == "LKMEX-aab910"
                assert (
                    metadata.transfers[0].properties.identifier == "LKMEX-aab910-2fe3b0"
                )
            assert metadata.transfers[1].value == 1389278024872597502641297
            if metadata.transfers[1].properties:
                assert metadata.transfers[1].properties.collection == "LKMEX-aab910"
                assert (
                    metadata.transfers[1].properties.identifier == "LKMEX-aab910-3102ca"
                )

    def test_esdt_transfer(self):
        tx_to_decode = TransactionToDecode()

        tx_to_decode.sender = (
            "erd1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fqvyjnq2"
        )
        tx_to_decode.receiver = (
            "erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = (
            "RVNEVFRyYW5zZmVyQDU0NDU1MzU0MmQzMjY1MzQzMDY0MzdAMDI1NDBiZTQwMA=="
        )

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "erd1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fqvyjnq2"
        )
        assert (
            metadata.receiver
            == "erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th"
        )
        assert metadata.value == 10000000000
        assert metadata.function_args is None
        if metadata.transfers:
            assert metadata.transfers[0].value == 10000000000
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.collection == "TEST-2e40d7"
                assert metadata.transfers[0].properties.identifier == "TEST-2e40d7"
    
    def test_multi_transfer_fungible_and_meta_esdt(self):
        tx_to_decode = TransactionToDecode()

        tx_to_decode.sender = (
            "erd1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqxj43r9"
        )
        tx_to_decode.receiver = (
            "erd1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqxj43r9"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = (
            "TXVsdGlFU0RUTkZUVHJhbnNmZXJAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEAwMkA0YzRiNGQ0NTU4MmQ2MTYxNjIzOTMxMzBAMmZlM2IwQDA5Yjk5YTZkYjMwMDI3ZTRmM2VjQDU1NTM0NDQzMmQzMzM1MzA2MzM0NjVAMDBAMDEyNjMwZTlhMjlmMmY5MzgxNDQ5MUA3MDYxNzk1ZjZkNjU3NDYxNWY2MTZlNjQ1ZjY2NzU2ZTY3Njk2MjZjNjVAMGVkZTY0MzExYjhkMDFiNUA="
        )

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "erd1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqxj43r9"
        )
        assert (
            metadata.receiver
            == "erd1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qxct34s"
        )

        assert metadata.value == 0
        assert metadata.function_name == "pay_meta_and_fungible"
        assert metadata.function_args == ["0ede64311b8d01b5", ""]

        if metadata.transfers:
            assert metadata.transfers[0].value == 45925073746530627023852
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.collection == "LKMEX-aab910"
                assert metadata.transfers[0].properties.identifier == "LKMEX-aab910-2fe3b0"
            
            assert metadata.transfers[1].value == 1389278024872597502641297
            if metadata.transfers[1].properties:
                assert metadata.transfers[1].properties.token == "USDC-350c4e"

    def test_multi_transfer_fungible_esdt(self):
        tx_to_decode = TransactionToDecode()

        tx_to_decode.sender = (
            "erd1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqxj43r9"
        )
        tx_to_decode.receiver = (
            "erd1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqxj43r9"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = (
            "TXVsdGlFU0RUTkZUVHJhbnNmZXJAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEAwMkA1MjQ5NDQ0NTJkMzAzNTYyMzE2MjYyQDAwQDA5Yjk5YTZkYjMwMDI3ZTRmM2VjQDU1NTM0NDQzMmQzMzM1MzA2MzM0NjVAQDAxMjYzMGU5YTI5ZjJmOTM4MTQ0OTE="
        )

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "erd1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqxj43r9"
        )
        assert (
            metadata.receiver
            == "erd1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qxct34s"
        )
        assert metadata.value == 0

        if metadata.transfers:
            assert metadata.transfers[0].value == 45925073746530627023852
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.token == "RIDE-05b1bb"
            
            assert metadata.transfers[1].value == 1389278024872597502641297
            if metadata.transfers[1].properties:
                assert metadata.transfers[1].properties.token == "USDC-350c4e"
