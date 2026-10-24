#!/usr/bin/env python3
"""Publish OPX pictures without changing catalogue names or shipping credentials."""
import argparse
import getpass
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parent.parent
API = 'https://api.fivemanage.com/api/v3/file'
MAX_IMAGE = 16 * 1024 * 1024


def valid_name(name):
  return isinstance(name, str) and bool(re.fullmatch(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*', name)) and all(part not in ('.', '..') for part in name.split('/'))


def valid_url(url):
  if not isinstance(url, str):
    return False
  parsed = urllib.parse.urlsplit(url)
  return parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username and not parsed.password


class Client:
  def __init__(self, key):
    self.key = key
    self.next_stamp = int(time.time() * 1000)

  def request(self, query='', body=None, content_type=None):
    headers = {'Authorization': self.key, 'Accept': 'application/json'}
    if content_type:
      headers['Content-Type'] = content_type
    request = urllib.request.Request(API + query, data=body, headers=headers)
    # Do not forward the credential to a redirected host.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
      def redirect_request(self, *args, **kwargs):
        return None
    try:
      with urllib.request.build_opener(NoRedirect).open(request, timeout=90) as response:
        result = json.load(response)
    except urllib.error.HTTPError as exc:
      raise RuntimeError(f'Fivemanage HTTP {exc.code}; check token permissions and quotas. Run again to resume.') from None
    if result.get('status') != 'ok':
      raise RuntimeError('Fivemanage refused the request. Run again to resume.')
    return result

  def existing(self):
    latest = {}
    page = 1
    while True:
      result = self.request('?' + urllib.parse.urlencode({'path': 'opx_images', 'page': page, 'limit': 100}))
      rows = result['data']
      for row in rows:
        meta = row.get('metadata') or {}
        name, digest, url = meta.get('opx_name'), meta.get('opx_sha256'), row.get('url')
        stamp = meta.get('opx_uploaded_at', 0)
        if not isinstance(stamp, int) or stamp < 0 or stamp >= 9007199254740991:
          continue
        self.next_stamp = max(self.next_stamp, stamp + 1)
        if valid_name(name) and isinstance(digest, str) and valid_url(url):
          rank = (stamp, str(row.get('id', '')))
          if name not in latest or rank > latest[name][0]:
            latest[name] = (rank, digest, url)
      pagination = result['pagination']
      if page * int(pagination['limit']) >= int(pagination['total']):
        return {(name, row[1]): row[2] for name, row in latest.items()}
      if not rows or int(pagination['limit']) < 1:
        raise RuntimeError('Invalid Fivemanage pagination.')
      page += 1

  def upload(self, name, data, digest):
    boundary = 'opx-' + uuid.uuid4().hex
    chunks = []
    self.next_stamp = max(self.next_stamp + 1, int(time.time() * 1000))
    fields = {'filename': name.rsplit('/', 1)[-1], 'path': 'opx_images',
              'metadata': json.dumps({'opx_name': name, 'opx_sha256': digest, 'opx_uploaded_at': self.next_stamp}), 'retentionExempt': 'true'}
    for field, value in fields.items():
      chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{field}"\r\n\r\n{value}\r\n'.encode())
    mime = mimetypes.guess_type(name)[0] or 'application/octet-stream'
    chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{fields["filename"]}"\r\nContent-Type: {mime}\r\n\r\n'.encode())
    chunks.extend([data, f'\r\n--{boundary}--\r\n'.encode()])
    result = self.request(body=b''.join(chunks), content_type=f'multipart/form-data; boundary={boundary}')
    url = result['data']['url']
    if not valid_url(url):
      raise RuntimeError('Fivemanage returned an invalid image URL.')
    return url


def pictures(folder):
  if not folder.is_dir():
    raise RuntimeError('The images/ directory is missing.')
  files = {}
  for path in sorted(folder.rglob('*')):
    if not path.is_file():
      continue
    name = path.relative_to(folder).as_posix()
    if not valid_name(name):
      raise RuntimeError(f'Unsupported image name: {name}')
    if path.stat().st_size > MAX_IMAGE:
      raise RuntimeError(f'Image exceeds 16 MiB: {name}')
    files[name] = path
  return files


def run(folder, client):
  files = pictures(folder)
  if not files:
    raise RuntimeError('No images found under images/.')
  existing = client.existing()
  uploaded = 0
  for name, path in files.items():
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if (name, digest) in existing:
      print(f'Unchanged: {name}', flush=True)
      continue
    client.upload(name, data, digest)
    uploaded += 1
    print(f'Uploaded: {name}', flush=True)
  print(f'Ready: {len(files)} files scanned recursively, {uploaded} uploaded. OPX refreshes its image catalogue automatically.')


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.parse_args()
  try:
    key = os.environ.get('FIVEMANAGE_API_KEY') or getpass.getpass('Fivemanage API key (hidden): ')
    if not key.strip():
      raise RuntimeError('An API key is required.')
    run(ROOT / 'images', Client(key.strip()))
  except (RuntimeError, OSError, ValueError, KeyError, TypeError) as exc:
    # Never echo remote response bodies or the token.
    print(f'Upload failed: {exc if isinstance(exc, RuntimeError) else type(exc).__name__}', file=sys.stderr)
    return 1
  except (KeyboardInterrupt, EOFError):
    print('Cancelled. Run again to resume.', file=sys.stderr)
    return 1
  return 0


if __name__ == '__main__':
  sys.exit(main())
