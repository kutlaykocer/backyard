package main

import (
	"flag"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/cyber-fighters/backyard/internal/pkg/api"
	"github.com/cyber-fighters/backyard/internal/pkg/tracer"
	"github.com/nats-io/go-nats"
	"github.com/nats-io/go-nats/encoders/protobuf"
	"github.com/sirupsen/logrus"
)

var (
	logLevel = flag.String("l", os.Getenv("LOG_LEVEL"), "Loglevel: one of error, warning, info or debug")
)

func main() {
	flag.Parse()

	// Configure for nano formatting
	customFormatter := new(logrus.TextFormatter)
	customFormatter.TimestampFormat = time.RFC3339Nano
	customFormatter.ForceColors = true
	logrus.SetFormatter(customFormatter)

	// Setup logging
	switch *logLevel {
	case "debug":
		logrus.SetLevel(logrus.DebugLevel)
	case "info":
		logrus.SetLevel(logrus.InfoLevel)
	case "warn":
		logrus.SetLevel(logrus.WarnLevel)
	default:
		logrus.SetLevel(logrus.ErrorLevel)
	}

	natsUrl := os.Getenv("NATS_URL")
	if natsUrl == "" {
		logrus.Fatal("no NATS_URL provided!")
	}

	mongoUrl := os.Getenv("MONGO_URL")
	if mongoUrl == "" {
		logrus.Fatal("no MONGO_URL provided!")
	}

	logrus.Debug("connecting to NATS...")
	nc, err := nats.Connect(natsUrl)
	if err != nil {
		logrus.WithError(err).Fatal("can't connect to NATS")
	}

	enc, _ := nats.NewEncodedConn(nc, protobuf.PROTOBUF_ENCODER)
	defer enc.Close()

	defer func() {
		nc.Close()
		logrus.Debug("NATS connection closed...")
	}()

	_, closer := tracer.Init("analyzer")
	defer closer.Close()

	api.Init(enc)

	logrus.Infof("listening for requests...")

	sigChan := make(chan os.Signal)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	s := <-sigChan
	logrus.Infof("received signal %q", s)
}
