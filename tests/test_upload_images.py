"""Offline coverage for the actual recursive uploader and V3 request metadata."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('uploader', Path(__file__).resolve().parents[1] / 'tools/upload-images.py')
uploader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uploader)


class FakeClient:
  def __init__(self):
    self.files = {}
    self.uploads = []
    self.fail = None

  def existing(self):
    return self.files.copy()

  def upload(self, name, data, digest):
    if name == self.fail:
      raise RuntimeError('interrupted')
    self.uploads.append(name)
    self.files[name, digest] = 'https://cdn.example/' + digest
    return self.files[name, digest]


class UploadTest(unittest.TestCase):
  def setUp(self):
    self.temp = tempfile.TemporaryDirectory()
    self.addCleanup(self.temp.cleanup)
    self.folder = Path(self.temp.name) / 'images'
    self.folder.mkdir()
    (self.folder / 'water.png').write_bytes(b'water')

  def test_recursive_upload_including_nested_directories(self):
    nested = self.folder / 'clothing/special'
    nested.mkdir(parents=True)
    (nested / 'a.webp').write_bytes(b'picture')
    client = FakeClient()
    uploader.run(self.folder, client)
    self.assertEqual(client.uploads, ['clothing/special/a.webp', 'water.png'])

  def test_unchanged_files_are_reused_and_changes_uploaded(self):
    client = FakeClient()
    uploader.run(self.folder, client)
    uploader.run(self.folder, client)
    self.assertEqual(client.uploads, ['water.png'])
    (self.folder / 'water.png').write_bytes(b'new water')
    uploader.run(self.folder, client)
    self.assertEqual(client.uploads, ['water.png', 'water.png'])

  def test_interruption_resumes_from_completed_uploads(self):
    (self.folder / 'z.png').write_bytes(b'z')
    client = FakeClient()
    client.fail = 'z.png'
    with self.assertRaises(RuntimeError):
      uploader.run(self.folder, client)
    client.fail = None
    uploader.run(self.folder, client)
    self.assertEqual(client.uploads, ['water.png', 'z.png'])

  def test_pagination_keeps_only_latest_content_per_name(self):
    client = uploader.Client('not-a-real-token')
    calls = []
    def request(query='', **kwargs):
      calls.append(query)
      page = len(calls)
      return {'data': [{'id': str(page), 'metadata': {'opx_name': 'water.png',
              'opx_sha256': 'new' if page == 1 else 'old', 'opx_uploaded_at': 20 if page == 1 else 10},
              'url': f'https://cdn.example/{page}'}], 'pagination': {'limit': 1, 'total': 2}}
    client.request = request
    found = client.existing()
    self.assertEqual(found, {('water.png', 'new'): 'https://cdn.example/1'})
    self.assertIn('page=2', calls[1])
    self.assertIn('path=opx_images', calls[0])
    # Reverting to an older hash must upload again with a newer timestamp.
    self.assertNotIn(('water.png', 'old'), found)

  def test_multipart_keeps_credential_out_of_metadata_and_uses_name(self):
    client = uploader.Client('not-a-real-token')
    stamp = client.next_stamp
    def request(**kwargs):
      self.assertIn(b'clothing/a.webp', kwargs['body'])
      self.assertIn(b'opx_sha256', kwargs['body'])
      self.assertIn(b'opx_uploaded_at', kwargs['body'])
      self.assertIn(b'\x00\xffpicture', kwargs['body'])
      self.assertNotIn(b'not-a-real-token', kwargs['body'])
      self.assertTrue(kwargs['content_type'].startswith('multipart/form-data; boundary='))
      return {'data': {'url': 'https://cdn.example/a'}}
    client.request = request
    self.assertEqual(client.upload('clothing/a.webp', b'\x00\xffpicture', 'hash'), 'https://cdn.example/a')
    self.assertGreater(client.next_stamp, stamp)

  def test_empty_or_missing_images_directory_is_refused(self):
    (self.folder / 'water.png').unlink()
    with self.assertRaises(RuntimeError):
      uploader.run(self.folder, FakeClient())
    self.folder.rmdir()
    with self.assertRaises(RuntimeError):
      uploader.run(self.folder, FakeClient())

  def test_path_validation(self):
    for name in ('../secret.png', 'clothing/../secret.png', '/x.png', 'a".png', 'a//b.png'):
      self.assertFalse(uploader.valid_name(name))
    self.assertTrue(uploader.valid_name('clothing/a.webp'))
    for url in ('javascript:alert(1)', 'http://cdn.example/x', 'https://token@cdn.example/x'):
      self.assertFalse(uploader.valid_url(url))


if __name__ == '__main__':
  unittest.main()
