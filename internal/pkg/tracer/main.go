package tracer

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"strings"
	"time"

	"github.com/opentracing/opentracing-go"
	"github.com/sirupsen/logrus"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/config"
	"github.com/uber/jaeger-client-go/transport"
)

type logrusWrapper struct{}

func (l logrusWrapper) Error(msg string) {
	logrus.Error(msg)
}

func (l logrusWrapper) Infof(msg string, args ...interface{}) {
	logrus.Infof(msg, args...)
}

func Init(service string) (opentracing.Tracer, io.Closer) {
	cfg := config.Configuration{
		ServiceName: service,
		Sampler: &config.SamplerConfig{
			Type:  "const",
			Param: 1,
		},
	}

	var sender jaeger.Transport
	jaegerHostPort := os.Getenv("JAEGER_ENDPOINT")
	if strings.HasPrefix(jaegerHostPort, "http://") {
		logrus.Debugf("using JAEGER collector as HTTP endpoint: %s", jaegerHostPort)
		sender = transport.NewHTTPTransport(
			os.Getenv("JAEGER_ENDPOINT"),
			transport.HTTPBatchSize(1),
		)
	} else {
		logrus.Debugf("using JAEGER agent as UDP endpoint: %s", jaegerHostPort)
		if s, err := jaeger.NewUDPTransport(jaegerHostPort, 0); err != nil {
			logrus.WithError(err).Panic("failed to setup UPD transpport")
		} else {
			sender = s
		}
	}

	lw := logrusWrapper{}
	tracer, closer, err := cfg.NewTracer(
		config.Reporter(jaeger.NewRemoteReporter(
			sender,
			jaeger.ReporterOptions.BufferFlushInterval(1*time.Second),
			jaeger.ReporterOptions.Logger(lw),
		)),
		config.Logger(lw),
	)
	if err != nil {
		logrus.WithError(err).Panic(fmt.Sprintf("cannot init Jaeger"))
	}

	opentracing.SetGlobalTracer(tracer)

	hook, err := NewJaegerTracingHook(&tracer, "tracer")
	if err != nil {
		logrus.WithError(err).Error("unable to initialize tracing hook")
	}
	logrus.AddHook(hook)

	return tracer, closer
}

// Inject serializes the context into the carrier byte slice.
func InjectSpanContext(ctx opentracing.SpanContext, carrier *bytes.Buffer) error {
	return opentracing.GlobalTracer().Inject(ctx, opentracing.Binary, carrier)
}

// Extract deserializes the context from the carrier byte slice.
func ExtractSpanContext(carrier []byte) (opentracing.SpanContext, error) {
	return opentracing.GlobalTracer().Extract(opentracing.Binary, bytes.NewBuffer(carrier))
}

