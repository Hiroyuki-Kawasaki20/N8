"""N8の利用者領域をCHから分離する回帰テスト。"""

import pytest
from pathlib import Path
import re

from tests.unit.test_local_output_path import _run_child


def test_current_docs_and_launcher_references_exist():
    root = Path(__file__).resolve().parents[2]
    readme = root / 'README.md'
    guide = root / 'docs' / '環境構築手順書.md'
    manual = root / 'docs' / '利用マニュアル.md'
    for document in (readme, guide, manual):
        text = document.read_text(encoding='utf-8')
        assert 'run_n8_kanban.bat' in text
        for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', text):
            if not re.match(r'\w+://', target):
                assert (document.parent / target).exists(), (document, target)
    bat = (root / 'run_n8_kanban.bat').read_text(encoding='utf-8')
    assert 'scripts\\start_ch_kanban.ps1' in bat
    assert (root / 'scripts' / 'start_ch_kanban.ps1').is_file()


@pytest.mark.parametrize('localappdata', ['local', None, ''])
def test_n8_storage_does_not_adopt_or_modify_ch_data(tmp_path, localappdata):
    _run_child(tmp_path, """
        local = Path(os.environ['LOCALAPPDATA']) if os.environ.get('LOCALAPPDATA') else Path.home() / 'AppData' / 'Local'
        ch = local / 'CHKanban'
        n8 = local / 'N8Kanban'
        ch.mkdir(parents=True)
        settings = ch / 'ch_kanban_settings.json'
        history_file = ch / 'lane_end_times_history.json'
        settings.write_text('{"base_dir": "CH-only"}', encoding='utf-8')
        history_file.write_text('{"history": [{"main": 123}]}', encoding='utf-8')
        before = {path: path.read_bytes() for path in (settings, history_file)}

        from src.services import data_loader, lane_end_times_history, spo_export
        from src.services.export_archive import resolve_archive_dir
        from src.models.constants import LOCAL_OUTPUT_DIR
        assert data_loader.get_config_path() == n8 / 'ch_kanban_settings.json'
        assert lane_end_times_history.get_history_path() == n8 / 'lane_end_times_history.json'
        assert Path(LOCAL_OUTPUT_DIR) == n8 / 'output'
        assert Path(spo_export.DEFAULT_STAGING_DIR) == n8 / 'output' / '_staging'
        assert Path(resolve_archive_dir('unused', local_output_dir=LOCAL_OUTPUT_DIR)) == n8 / 'output' / '_export_archive'
        assert not n8.exists()
        assert data_loader.load_config() == {}
        assert lane_end_times_history.load_lane_end_times_history() == []
        data_loader.save_config({'base_dir': str(sandbox / 'n8-input'), 'keep': True})
        assert lane_end_times_history.save_lane_end_times_history([{'main': 456}])
        assert data_loader.load_config()['keep'] is True
        assert lane_end_times_history.load_lane_end_times_history() == [{'main': 456}]
        assert {path: path.read_bytes() for path in before} == before
    """, localappdata=localappdata)