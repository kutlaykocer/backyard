package api

import (
	"github.com/cyber-fighters/backyard/internal/pkg/dao"
	"github.com/nats-io/go-nats"
	"github.com/sirupsen/logrus"
	"os"
)

var (
	enc *nats.EncodedConn
	backyardDao = dao.BackyardDAO{}
	quit = make(chan struct{})
)

func Init(conn *nats.EncodedConn) {
	enc = conn

	_, err := enc.QueueSubscribe("scan.completed.*","analyzer", handleScanCompleted)
	if err != nil {
		logrus.WithError(err).Fatal("Failed subscribing to scan.completed")
	}

	_, err = enc.QueueSubscribe("scan.status.*","analyzer", handleScanStatus)
	if err != nil {
		logrus.WithError(err).Fatal("Failed subscribing to scan.status.*")
	}

	_, err = enc.QueueSubscribe("analyze.request", "analyzer", handleDoAnalysis)
	if err != nil {
		logrus.WithError(err).Fatal("Failed subscribing to analyze.request")
	}

	backyardDao.Url = os.Getenv("MONGO_URL")
	backyardDao.Connect()
}