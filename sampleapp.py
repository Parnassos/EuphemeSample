#!/usr/bin/env python3
""" Sample Application for Eupheme. """

import wsgiref.simple_server
import eupheme.faucets as faucets
import eupheme.application as application


class IndexPage:

    """ The IndexPage class is the handler for two of the routes below.

    See the app.routes.add calls down below for more details on how
    this class is used by the application.

    """

    # Allowed methods on this resource
    allowed_methods = {'GET', 'POST'}

    @faucets.produces('text/html', 'application/json')
    @faucets.consumes('text/html')
    @faucets.template('index.html')
    def get(self, data, name, **query):
        """ Handle the GET request to this resource.

        The method returns a dict which is then used by the outgoing faucets
        to generate the output.

        """
        return {'name': name}

    @faucets.produces('text/html', 'application/json')
    @faucets.consumes('application/x-www-form-urlencoded')
    @faucets.template('index.html')
    def post(self, data, name, **query):
        """ Handle the POST request to this resource.

        Returns a dict which is used by outgoing faucets to generate output
        based on the user's input in the form on the index page.

        """

        # The data returned by this method will be handled by an outgoing
        # faucet, take care to return it to the template engine (Jinja2) the
        # way you want it to be presented.
        if data is not None and 'name' in data:
            return {'name': data['name'][0]}
        else:
            return {}


# Create the application and load the config
app = application.Application('sampleapp.config')

# Add incoming and outgoing faucets (these are used to process incoming and
# outgoing data).
app.faucets.add_outgoing(faucets.JinjaFaucet('templates'))
app.faucets.add_outgoing(faucets.JsonFaucet())
app.faucets.add_incoming(faucets.FormFaucet())

# Add some routes to the application
app.routes.add('^/(\w*)$', IndexPage())
app.routes.add('^/test/([a-zA-Z0-9\.]+)/?$', IndexPage())

# Start the application
print("Making server...")
httpd = wsgiref.simple_server.make_server('0.0.0.0', 8000, app)
print("Serving")
httpd.serve_forever()
