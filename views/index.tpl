<html>
  <head>
    <title>Juju SVG - Making bundles come to life</title>
  </head>
  <body>
    <h1 id="intro">A web frontend to Juju SVG</h1>
    <p>Hello. This is a web service to allow anyone with a <code>bundle.yaml</code> file to have it translated into an SVG as you would see in the Juju GUI or Charm Store</p>
    <p>Enter a bundle.yaml URL and format type to get started:</p>
    <form method=GET>
      <input type=text size="40" placeholder="Bundle URL" id="bundle" name="bundle">
      <select name="output">
        <option value="svg">SVG</option>
        <option value="png">PNG</option>
        <option value="pdf">PDF</option>
        <option value="xml">XML</option>
      </select>
      <input type=submit value="Generate">
    </form>
    <h2 id="format">Accepted Formats</h2>
    <p>This service only accepts one of two formatted bundles. The preferred bundle format is a "flat" bundle, one which only consists of "services", "relations", and optionally a "series" key. An example of this follows.</p>
    <h3 id="format-preferred">Preferred format</h3>
    <pre><code>services:
  mediawiki:
    charm: cs:trusty/mediawiki
    num_units: 3
    options:
      debug: true
    annotations:
      gui-x: "750"
      gui-y: "500"
  mariadb:
    charm: cs:trusty/mariadb
    num_units: 1
    annotations:
      gui-x: "500"
      gui-y: "250"
series: trusty
relations:
- - wordpress:db
  - mariadb:database
    </code></pre>
    </h3>
    <h3 id="format-old">Other format</h3>
    <p>This, older, format is also accepted, but you can only present ONE deployment routine.</p>
    <pre><code>my-blog:
  services:
    mediawiki:
      charm: cs:trusty/mediawiki
      num_units: 3
      options:
        debug: true
      annotations:
        gui-x: "750"
        gui-y: "500"
    mariadb:
      charm: cs:trusty/mariadb
      num_units: 1
      annotations:
        gui-x: "500"
        gui-y: "250"
  series: trusty
  relations:
  - - wordpress:db
    - mariadb:database
    </code></pre>
    <h2 id="build">Generating an SVG</h2>
    <p>
      There are two ways to get a bundle generated. One is using a GET request and one is using a POST.
    </p>
    <h3 id="build-get">GET bundle</h3>
    <p>For the GET requests two quereis are supported. You can either send a <code>bundle</code> key, which will use the Juju Charm Store to fetch the details or a <code>bundle-file</code> which needs to be an HTTP addressed URL to the raw source of the bundle's YAML. Here are some examples:
      <ul>
        <li>
          <a href=http://svg.juju.solutions/?bundle=openstack-telemetry>svg.juju.solutions/?bundle=openstack-telemetry</a>
        </li>
        <li>
          <a href=http://svg.juju.solutions/?bundle=cs:~bigdata-dev/bundle/apache-analytics-sql-3>svg.juju.solutions/?bundle=cs:~bigdata-dev/bundle/apache-analytics-sql-3</a>
        </li>
        <li>
          <a href=http://svg.juju.solutions/?bundle=https://raw.githubusercontent.com/marcoceppi/bundle-observable-kubernetes/8681c21a5592806ea90fc56825eee488ac0541d1/bundle.yaml>svg.juju.solutions/?bundle=https://raw.githubusercontent.com/marcoceppi/bundle-observable-kubernetes/8681c21a5592806ea90fc56825eee488ac0541d1/bundle.yaml</a>
        </li>
        <li>
          <a href=http://svg.juju.solutions/?bundle=http://bazaar.launchpad.net/~bigdata-dev/charms/trusty/apache-analytics-sql-hue/trunk/download/head:/bundles.yaml-20150420030716-vycsb0pcenhst8wt-1/bundles.yaml>svg.juju.solutions/?bundle-file=http://bazaar.launchpad.net/~bigdata-dev/charms/trusty/apache-analytics-sql-hue/trunk/download/head:/bundles.yaml-20150420030716-vycsb0pcenhst8wt-1/bundles.yaml</a>
        </li>
      </ul>
    </p>
    <h3 id="build-post">POST bundle</h3>
    <p>
      The second way to generate a bundle is to POST the contents of the bundle to the web service. An example in various languages has been included for your convience.
    </p>
    <h4 id="build-post-curl">CURL</h4>
    <pre><code>curl -X POST --data "$(cat bundle.yaml)" http://svg.juju.solutions</code></pre>
    <h4 id="build-post-pythonreq">Python Requests</h4>
    <pre><code>import requests

with open('bundle.yaml') as f:
  bundle = f.read()

r = requests.post('http://svg.juju.solutions', bundle)
# r.content holds SVG, mimetype image/svg+xml</code></pre>
    <h2 id="caveats">Caveats</h2>
    <p>This webservice is still under active development. There's bound to be a few issues. I'll document long standing ones here.</p>
    <h3 id="caveats-annotations">Annotations</h3>
    <p>
      Support for non-annotated bundles is avaiable. However, it's binary support. Either you have annotations for all services or no services. In the case where no annotations are found, networkx will be used to render the bundle to the best of it's ability (thanks <a href="https://github.com/bcsaller">@bcsaller</a>). Initial support is only for the circular plan, but in the future this may become configurable.
    </p><br><br>
    <footer style="text-align: center">
      Made with &lt;3 by <a href="http://marcoceppi.com">Marco Ceppi</a>. An <a href="https://github.com/marcoceppi/svg.juju.solutions">Open Source</a> project.
    </footer>
  </body>
</html>
