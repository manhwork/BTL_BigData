from importlib import import_module


class LegacyBronzeUploader:
    def upload(self, *, request, spark) -> None:
        legacy_module = import_module("load_rawData.load")

        if request.dataset_type == "meta":
            legacy_module.upload_meta_data(
                spark,
                request.category,
                compression_codec=request.compression_codec,
                clear_hf_cache=request.clear_hf_cache,
            )
            return

        legacy_module.upload_review_data(
            spark,
            request.category,
            compression_codec=request.compression_codec,
            clear_hf_cache=request.clear_hf_cache,
        )
