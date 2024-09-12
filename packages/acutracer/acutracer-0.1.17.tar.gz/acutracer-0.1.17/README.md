# acutracer (Distributed tracer)
A llm flow tracer


The following repo will have the instrumentors for a agentic system.

The instrumentor will trace all the outgoing calls made through a agentic system.

The following headers will be added to the calls.

X-acuvity-trace-id
X-acuvity-span-id

The headers will be captured by the proxy for further processing.

## Visualization of the traces

All the traces are OTEL compatible, so any OTEL collector can be used to view the traces locally.

# Supported Instrumentors for python

1. Web Frameworks:
   - FastAPIInstrumentor
   - FlaskInstrumentor
   - DjangoInstrumentor

2. HTTP Clients:
   - RequestsInstrumentor
   - URLLibInstrumentor
   - AioHTTPClientInstrumentor

# Future work for Granular Instrumentors in python

3. Databases:
   - MongoInstrumentor

4. gRPC:
   - GRPCInstrumentor

5. AWS:
   - BotoInstrumentor

6. Logging:
   - LoggingInstrumentor

# Jaeger example with FAST API instrumentor:

# Setting up the app:

1st pip install the acutracer

```
pip install acutracer
```

Import the following lines.

```
from acutracer.instrumentors.python.webapi.instrumentor import (
    WebAPIInstrumentor,
)

app = FastAPI(title="Fast-API")

instrumentor = WebAPIInstrumentor(name="acuvity-tracing-example")
tracer = instrumentor.instrument(app=app)
```
# Setting Up and Using Jaeger UI (for macOS)

## Starting Jaeger

Run the following command to start the Jaeger all-in-one Docker container:

```bash
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14317:4317 \
  -p 4318:4318 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest
```

Note: We've changed `-p 4317:4317` to `-p 14317:4317`. This maps the container's internal port 4317 to the host's port 14317.

## Accessing the Jaeger UI

Once the container is running, you can access the Jaeger UI by opening a web browser and navigating to:

```
http://localhost:16686
```

## Viewing Traces

1. Start your instrumented Python application.
2. Make some requests to your application to generate traces.
3. Open the Jaeger UI in your web browser.
4. In the UI:
   - Select your service from the "Service" dropdown (it should be named after your Python application).
   - Set an appropriate time range.
   - Click "Find Traces" to view your traces.

## Troubleshooting

If you don't see any traces:
1. Check that your application is running and generating traffic.
2. Ensure that the Jaeger agent port (6831) is accessible from your application.
3. Verify that the exporter in your Python code is correctly configured to send traces to `localhost:6831`.
4. Check the console output of your Python application for any error messages related to trace export.

Remember to stop the Jaeger container when you're done:

```bash
docker stop jaeger
docker rm jaeger
```
