package tracer

import (
	"github.com/opentracing/opentracing-go"
	"github.com/opentracing/opentracing-go/ext"
	"github.com/opentracing/opentracing-go/log"
	"github.com/sirupsen/logrus"
)

type JaegerTracingHook struct {
	Tracer *opentracing.Tracer
	Tag string
}

func NewJaegerTracingHook(tracer *opentracing.Tracer, tag string) (*JaegerTracingHook, error) {
	return &JaegerTracingHook{tracer, tag}, nil
}

func (hook *JaegerTracingHook) Fire(entry *logrus.Entry) error {
	// If there is a span in the log data, and it's a tracing span, send the information
	// via opentracing.
	if spanI, ok := entry.Data["span"]; ok {
		if span, ok := spanI.(opentracing.Span); ok {
			line, err := entry.String()
			if err != nil {
				return err
			}

			// Add log fields if any others
			fields := []log.Field{log.String("message", line)}
			for key, value := range entry.Data {
				if key != "span" {
					switch v := value.(type) {
					case int:
						fields = append(fields, log.Int(key, v))
					case int32:
						fields = append(fields, log.Int32(key, v))
					case int64:
						fields = append(fields, log.Int64(key, v))
					case uint32:
						fields = append(fields, log.Uint32(key, v))
					case uint64:
						fields = append(fields, log.Uint64(key, v))
					case string:
						fields = append(fields, log.String(key, v))
					default:
						//fmt.Printf("unsupported type \"%T\" for span logging key %q\n", value, key)
					}
				}
			}

			if entry.Level == logrus.PanicLevel || entry.Level == logrus.FatalLevel || entry.Level == logrus.ErrorLevel {
				fields = append(fields, log.String("event", "error"))
				ext.Error.Set(span, true)
			}

			span.LogFields(fields...)
		}
	}

	return nil
}

func (hook *JaegerTracingHook) Levels() []logrus.Level {
	return logrus.AllLevels
}