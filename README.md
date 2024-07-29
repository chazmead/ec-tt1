# EdgeConnect Average Commodity Value

## Setup

### Python Setup

To setup the project, run the setup script:

```
$ ./scripts/setup
```

### Run Tests & Linters
Once setup, you can run testing and linting using the appropriate scripts:
```
$ ./scripts/lint
$ ./scripts/test
```

### Run the Webserver locally

To build and run the docker container use the run script:
```
$ ./scripts/run
```

### Run the Native runtime
To run the native python program, simply run the edgeconnect.http module while the virtualenv is activated
```
$ . env/bin/activate
$ (env) PYTHONPATH=./src python -m edgeconnect.http
```

This will setup the server listening on `0.0.0.0:8000`.  You can test the server by
running an example discovery curl request:

```
$ curl http://127.0.0.1:8000/healthz/readiness -i
```

#### OpenAPI Spec
When the API is running locally you can visit:
- http://127.0.0.1:8000/docs

Or get the json version from:
```
$ curl http://127.0.0.1:8000/openapi.json
```


## Deploying to Kubernetes with helm
Providing you have a valid `kubectl` context configured and activated, you can simply run the
deploy script:
```
$ ./scripts/deploy
```
