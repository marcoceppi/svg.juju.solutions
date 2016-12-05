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
    bundle_file = bottle.request.params.get('bundle-file')
    format = bottle.request.params.get('output', 'svg')

    svg = None
    svg_url = None

    if format not in api.TYPES.keys():
        msg = 'Format {0} not supported: {1}'
        bottle.abort(400, msg.format(format, ','.join(api.TYPES.keys())))

    if not bundle_id and not bundle_file:
        return bottle.template('index')

    if bundle_id and bundle_file:
        bottle.abort(400, 'Calm down satan, too many bundles')

    if bundle_id.startswith('http'):
        bundle_url = bundle_id
    elif bundle_id:
        bundle_url, _ = api.parse_bundle_id(bundle_id)
    else:
        bundle_url = bundle_file

    if not bundle_url:
        bottle.abort(400, 'The bundle ID you provided is not valid. Must be '
                     'either cs:bundle/bundle-name-# or '
                     'cs:~user/bundle/bundle-name-#')

    if svg_url:
        r = requests.get(svg_url)
        try:
            r.raise_for_status()
        except:
            pass
        else:
            svg = r.text.replace('../../', 'https://api.jujucharms.com/v5/')

    if not svg:
        bundle = yaml.safe_load(requests.get(bundle_url).text)
        try:
            svg = api.process_bundle(bundle)
        except api.BundleFormatException as e:
            bottle.abort(400, e.msg)
        except api.JujuSVGException as e:
            bottle.abort(406, "%s: %s" % (e.cmd, e.msg))

    try:
        output = api.output_bundle(svg, format)
    except api.JujuSVGException as e:
        bottle.abort(406, "%s: %s" % (e.cmd, e.msg))

    bottle.response.content_type = api.TYPES.get(format)
    return output


@app.post('/')
def process():
    bundle_file = bottle.request.body.read()
    bundle = yaml.safe_load(bundle_file)
    format = bottle.request.params.get('output', 'svg')

    if format not in api.TYPES.keys():
        msg = 'Format {0} not supported: {1}'
        bottle.abort(400, msg.format(format, ','.join(api.TYPES.keys())))

    try:
        svg = api.process_bundle(bundle)
    except api.BundleFormatException as e:
        bottle.abort(400, e.msg)
    except api.JujuSVGException as e:
        bottle.abort(406, "%s: %s" % (e.cmd, e.msg))

    try:
        output = api.output_bundle(svg, format)
    except api.JujuSVGException as e:
        bottle.abort(406, "%s: %s" % (e.cmd, e.msg))

    bottle.response.content_type = api.TYPES.get(format)
    return output

if __name__ == '__main__':
    bottle.run(app=app,
               host='0.0.0.0',
               port=9090)
