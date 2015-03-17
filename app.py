#!/usr/bin/python

import yaml
import bottle
import tempfile
import subprocess

from settings import JUJSVG

app = application = bottle.Bottle()


@app.get('/')
def home():
    '''
    The front "index" page
    '''

    bundle_url = bottle.request.params.get('bundle')

    if not bundle_url:
        return ('Hello, please post the contents of a bundle file as "bundle" '
                'to get an SVG. The bundle file can only have ONE deployment '
                'modeled')

    return "One day I'll support this. Today is not that day"


@app.post('/')
def process():
    bundle_file = bottle.request.body.read()
    bundle = yaml.safe_load(bundle_file)
    if len(bundle) > 1 and 'services' not in bundle:
        bottle.abort(400, 'This has multiple deployments')

    if 'services' not in bundle:
        if 'services' not in bundle.itervalues().next():
            bottle.abort(400, "Can't tell what this bundle is, or if it is")

        bundle = bundle.itervalues().next()

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(yaml.dump(bundle, default_flow_style=False))
        f.flush()
        try:
            svg = subprocess.check_output([JUJSVG, f.name], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            bottle.abort(406, "%s %s" % (e.cmd, e.output))

    bottle.response.content_type = 'image/svg+xml'

    return svg

if __name__ == '__main__':
    bottle.run(app=app,
        host='0.0.0.0',
        port=9090)
