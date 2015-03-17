#!/usr/bin/python

import api
import yaml
import bottle

import requests


app = application = bottle.Bottle()


@app.get('/')
def home():
    '''
    The front "index" page
    '''

    bundle_id = bottle.request.params.get('bundle')

    if not bundle_id:
        return ('Hello, please post the contents of a bundle file as "bundle" '
                'to get an SVG. The bundle file can only have ONE deployment '
                'modeled')

    bundle_url = api.parse_bundle_id(bundle_id)
    if not bundle_url:
        bottle.abort(400, 'The bundle ID you provided is not valid. Must be '
                     'either cs:bundle/bundle-name-# or '
                     'cs:~user/bundle/bundle-name-#')

    bundle = yaml.safe_load(requests.get(bundle_url).text)
    try:
        svg = api.process_bundle(bundle)
    except api.BundleFormatException as e:
        bottle.abort(400, e.msg)
    except api.JujuSVGException as e:
        bottle.abort(406, "%s: %s" % (e.cmd, e.msg))

    bottle.response.content_type = 'image/svg+xml'
    return svg


@app.post('/')
def process():
    bundle_file = bottle.request.body.read()
    bundle = yaml.safe_load(bundle_file)

    try:
        svg = api.process_bundle(bundle)
    except api.BundleFormatException as e:
        bottle.abort(400, e.msg)
    except api.JujuSVGException as e:
        bottle.abort(406, "%s: %s" % (e.cmd, e.msg))

    bottle.response.content_type = 'image/svg+xml'
    return svg

if __name__ == '__main__':
    bottle.run(app=app,
        host='0.0.0.0',
        port=9090)
