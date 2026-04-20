from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
OPENAPI_PATH = ROOT / "spec" / "finance_research_openapi.yaml"


class HttpApiContractTest(unittest.TestCase):
    def test_spec_declares_api_ownership_and_client_boundary(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 7.1 HTTP API ownership and consumer rules", spec_text)
        self.assertIn("The frontend only talks to `/v1/*` backend contracts.", spec_text)
        self.assertIn(
            "The frontend does not call third-party providers directly.", spec_text
        )
        self.assertIn(
            "`Chat` plus `Snapshots` define the run, stream, and render boundary.",
            spec_text,
        )

    def test_openapi_describes_bff_surface_and_backend_mediation(self) -> None:
        openapi_text = OPENAPI_PATH.read_text()
        self.assertIn(
            "The /v1 API is the client-facing backend-for-frontend surface.",
            openapi_text,
        )
        self.assertIn(
            "Clients must not call third-party providers directly.", openapi_text
        )
        self.assertIn(
            "SSE chat streaming is a backend-mediated run transport.", openapi_text
        )
        self.assertIn(
            "Snapshot transforms are backend-mediated interactions over sealed snapshots.",
            openapi_text,
        )


if __name__ == "__main__":
    unittest.main()
