from pathlib import Path
from unittest import TestCase
from unittest import mock

from tecton import RedshiftConfig
from tecton import v09_compat
from tecton.cli.upgrade_utils import DataSourceGuidance
from tecton.types import Field
from tecton.types import Int64
from tecton.types import String
from tecton.types import Timestamp


class TestUpgrade(TestCase):
    def mockPatch(self, *args, **kwargs):
        patcher = mock.patch(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def setUp(self) -> None:
        self.mock_metadata_service = mock.MagicMock()
        self.mockPatch("tecton._internals.metadata_service.instance", return_value=self.mock_metadata_service)

    def test_push_source(self):
        push_source = v09_compat.PushSource(
            name="PushSource",
            schema=[
                Field(name="content_keyword", dtype=String),
                Field(name="timestamp", dtype=Timestamp),
                Field(name="clicked", dtype=Int64),
            ],
        )

        push_source_guidance = DataSourceGuidance(push_source, str(Path()))._get_upgrade_guidance()
        self.assertEqual(len(push_source_guidance), 2)
        self.assertIn(
            "Replace `PushSource` with `StreamSource` and set `stream_config=PushConfig()", push_source_guidance[0]
        )

    def test_data_source(self):
        batch_source = v09_compat.BatchSource(
            name="redshift_ds", batch_config=RedshiftConfig(endpoint="test_uri", table="test_table")
        )
        push_source_guidance = DataSourceGuidance(batch_source, str(Path()))._get_upgrade_guidance()
        self.assertEqual(len(push_source_guidance), 1)
        self.assertIn("Update import from tecton.v09_compat to tecton.", push_source_guidance[0])
