import requests
from flask import Flask, abort, jsonify, Response
from flask_caching import Cache


Dcbtube_url = 'https://menu.dckube.scilifelab.se/api/'

# setup flask config, mainly for cache here
config = {"DEBUG": True,
         "CACHE_TYPE": "SimpleCache",
         "CACHE_DEFAULT_TIMEOUT": 10
}

# instantiate the app
app = Flask(__name__)

# tell Flask to use the above config
app.config.from_mapping(config)
cache = Cache(app)

# the back end processing, can be extended
# or moved to another source file
def backend(res):
  '''
  function to process the response
  check if content is json and return
  otherwise return raw content (in bytes)
  '''
  # print this message for new calls or if cache expired
  # just to test the cache is working
  print(f'new call or cache expired! calling external api')
  
  try:
      'application/json' in res.headers.get('Content-Type')
      content = res.json()

  except:
      content = res.content

  return content

# (alternative) skip json parsing and set mimetype manually (for the last optional question)
#  return Response(res.content, status=200, mimetype="application/json")

# Route to handle error response from the external api
@app.errorhandler(404)
def api_error(e):
  # return error as json
  return jsonify(error=str(e)), 404

# main route
# using type 'path' to allow '/' for subpaths
@app.route("/<path:uri>")
@cache.cached()
def relay(uri): 
    try:
      response = requests.get(Dcbtube_url + uri)
      content = backend(response)
      return content
      
    except:
      # call @app.errorhandler route
      abort(404, description="api error")




if __name__ == "__main__":
  app.run(debug=False, threaded=True)
