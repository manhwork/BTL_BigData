import unittest

from main.silver.silver_service import SilverJobRequest, SilverService


class SilverServiceTest(unittest.TestCase):
    def test_clean_returns_silver_target_path(self) -> None:
        service = SilverService()
        request = SilverJobRequest(category="Appliances")

        result = service.clean(request)

        self.assertTrue(result.succeeded)
        self.assertEqual(result.stage, "clean")
        self.assertEqual(
            result.target_path,
            "gs://amazon-reviews-lakehouse-data/silver-zone/clean-data/Appliances",
        )

    def test_enrich_returns_embedding_target_path(self) -> None:
        service = SilverService()
        request = SilverJobRequest(category="Books")

        result = service.enrich(request)

        self.assertTrue(result.succeeded)
        self.assertEqual(result.stage, "enrich")
        self.assertEqual(
            result.target_path,
            "gs://amazon-reviews-lakehouse-data/silver-zone/enriched-data/Books",
        )


if __name__ == "__main__":
    unittest.main()

