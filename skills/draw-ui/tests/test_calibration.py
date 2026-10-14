"""验证静态图片比较的尺寸与区域前提。"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'


class CalibrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for name in ('reference', 'candidate'):
            Image.new('RGB', (32, 64), 'white').save(self.root / (name+'.png'))

    def tearDown(self):
        self.temp.cleanup()

    def compare(self, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPTS/'compare_mockup.py'), '--reference', str(self.root/'reference.png'), '--candidate', str(self.root/'candidate.png'), '--out-dir', str(self.root/'comparison'), *extra],
            capture_output=True,
            text=True,
        )

    def test_equal_and_invalid_clip(self):
        self.assertEqual(self.compare().returncode, 0)
        metrics = json.loads((self.root/'comparison/comparison-metrics.json').read_text(encoding='utf-8'))
        self.assertFalse(metrics['resized'])
        self.assertEqual(metrics['regions'][0]['mean_abs_diff'], 0)
        for clip in ['bad:0,0,33,2', '../escape:0,0,1,1', 'full:0,0,1,1', 'bad:0,0,-1,1']:
            with self.subTest(clip=clip):
                self.assertNotEqual(self.compare('--clip', clip).returncode, 0)

    def test_width_mismatch(self):
        Image.new('RGB', (33, 64), 'white').save(self.root/'candidate.png')
        self.assertNotEqual(self.compare('--allow-height-difference').returncode, 0)
        self.assertFalse((self.root/'comparison').exists())

    def test_short_page_preserves_missing_tail(self):
        Image.new('RGB', (32, 50), 'white').save(self.root/'candidate.png')
        self.assertNotEqual(self.compare().returncode, 0)
        self.assertEqual(self.compare('--allow-height-difference', '--clip', 'tail:0,50,32,14').returncode, 0)
        metrics = json.loads((self.root/'comparison/comparison-metrics.json').read_text(encoding='utf-8'))
        self.assertEqual(metrics['height_delta'], -14)
        self.assertFalse(metrics['geometry_match'])
        with Image.open(metrics['unmatched_tails']['reference']) as tail:
            self.assertEqual(tail.size, (32, 14))
        self.assertIn('status', metrics['regions'][-1])


if __name__ == '__main__':
    unittest.main()
