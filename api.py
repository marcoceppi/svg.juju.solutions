import re
import yaml
import tempfile
import subprocess

from settings import JUJSVG

class JujuSVGException(Exception):
    def __init__(self, cmd, msg):
        self.cmd = cmd
        self.msg = msg


class BundleFormatException(Exception):
    def __init__(self, msg):
        self.msg = msg


def parse_bundle_id(bundle_id):
    m = re.match(r'cs(:~[a-z0-9-_]+/|:)bundle/[a-z0-9-]+-[0-9]+', bundle_id)
    if not m:
        return None

    bundle_path = m.group(0).replace('cs:', '')
    return 'https://api.jujucharms.com/v4/%s/archive/bundle.yaml' % bundle_path


def process_bundle(bundle):
    print(bundle)
    if len(bundle) > 1 and 'services' not in bundle:
        raise BundleFormatException('This has multiple deployments')

    if 'services' not in bundle:
        if 'services' not in bundle.itervalues().next():
            raise BundleFormatException("This probably isn't a bundle...")

        bundle = bundle.itervalues().next()

    with tempfile.NamedTemporaryFile() as f:
        f.write(yaml.dump(bundle, default_flow_style=False))
        f.flush()
        try:
            svg = subprocess.check_output([JUJSVG, f.name],
                                          stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise JujuSVGException(' '.join(e.cmd), e.output)
    return svg
