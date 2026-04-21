from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class SnapshotSemanticsContractTest(unittest.TestCase):
    def test_spec_declares_sealed_snapshot_manifest(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("## 10. Snapshot semantics", spec_text)
        self.assertIn("### 10.1 Sealed snapshot manifest", spec_text)
        self.assertIn(
            "A sealed snapshot pins the subject set, `as_of`, basis, normalization, coverage window, source set, bound fact / claim / event refs, and exact `allowed_transforms`.",
            spec_text,
        )
        self.assertIn(
            "`allowed_transforms` is explicit manifest state, not a UI guess derived from block kind alone.",
            spec_text,
        )
        self.assertIn(
            "Persisted chat and analyze artifacts must continue to point at that sealed snapshot rather than reconstructing support opportunistically later.",
            spec_text,
        )

    def test_spec_declares_in_snapshot_transform_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 10.2 In-snapshot transforms", spec_text)
        self.assertIn(
            "A transform is legal inside a sealed snapshot only when it preserves the subject set and does not require fresher evidence than `as_of`.",
            spec_text,
        )
        self.assertIn(
            "In-snapshot transforms may change presentation or range only when the required rows or series are already inside the sealed data boundary.",
            spec_text,
        )
        self.assertIn(
            "Changing `YTD` to `1Y` on a performance chart is allowed only if the requested range end is less than or equal to `as_of`.",
            spec_text,
        )
        self.assertIn(
            "The manifest, not the client, determines whether a transform is allowed.",
            spec_text,
        )

    def test_spec_declares_refresh_boundary_and_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 10.3 Refresh and new-run boundary", spec_text)
        self.assertIn(
            "Any request that changes subject membership, peer set, basis, normalization, or freshness crosses the snapshot boundary.",
            spec_text,
        )
        self.assertIn(
            "Requests for fresher data, different peers, different basis, or different normalization require refresh or a new run.",
            spec_text,
        )
        self.assertIn(
            "Crossing the snapshot boundary must be explicit rather than a silent mutation of a sealed answer.",
            spec_text,
        )
        self.assertIn("### 10.4 Downstream consumer rules for snapshot semantics", spec_text)
        self.assertIn(
            "Block registry versioning and validation (`P2.3`) depends on snapshot rules being stable enough to know which interactions are legal within existing block bindings and which require a new backend result.",
            spec_text,
        )
        self.assertIn(
            "Snapshot assembler and verifier (`P2.4`) depends on the sealed manifest contents, sealing order, and refresh boundary to prove that rendered blocks still correspond to the same evidence-backed snapshot.",
            spec_text,
        )
        self.assertIn(
            "Shared artifact flow (`P4.3`) depends on sealed snapshots remaining reusable product artifacts.",
            spec_text,
        )
        self.assertIn(
            "Frontend renderer (`PX.3`) depends on presentation-only interactions staying local only when they remain inside the sealed snapshot contract.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
