import re
import yaml
import tempfile
import subprocess

import networkx as nx

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


def split_rel(r):
    return r.split(':', 1)


def mapply(func, g, **kwargs):
    args = {}
    for name in func.func_code.co_varnames:
        if name in kwargs:
            args[name] = kwargs[name]
    return func(g, **args)


# https://gist.github.com/bcsaller/adca309ba7abef2e8caf#file-place_bundle-py-L46
def layout(bundle, algo, scale=1000.0):
    g = nx.MultiGraph()
    for service in bundle['services']:
        g.add_node(service)

    for relation in bundle['relations']:
        src = split_rel(relation[0])[0]
        tgts = relation[1]
        if isinstance(tgts, (str, unicode)):
            tgts = [tgts]
        for tgt in tgts:
            tgt = split_rel(tgt)[0]
            g.add_edge(src, tgt)
    pos = mapply(algo, g, k=45, iterations=100)

    for service, data in bundle['services'].items():
        data['annotations'] = {
            "gui-x": float(pos[service][0]) * scale,
            "gui-y": float(pos[service][1]) * scale,
        }
    return g


def process_bundle(bundle):
    if len(bundle) > 1 and 'services' not in bundle:
        raise BundleFormatException('This has multiple deployments')

    if 'services' not in bundle:
        if 'services' not in bundle.itervalues().next():
            raise BundleFormatException("This probably isn't a bundle...")

        bundle = bundle.itervalues().next()

    annotations = False
    for service, srvc_data in bundle['services'].iteritems():
        if 'annotations' in srvc_data.keys():
            annotations = True
            break

    if not annotations:
        layout = 'circular'
        algo = getattr(nx, layout + '_layout', None)
        layout(bundle, algo)

    with tempfile.NamedTemporaryFile() as f:
        f.write(yaml.dump(bundle, default_flow_style=False))
        f.flush()
        try:
            svg = subprocess.check_output([JUJSVG, f.name],
                                          stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise JujuSVGException(' '.join(e.cmd), e.output)
    return svg
