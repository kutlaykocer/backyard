package dao

import (
	"fmt"
	"github.com/globalsign/mgo"
	"github.com/sirupsen/logrus"
	"io"
)

var (
	db       *mgo.Database
)

const (
	COLLECTION = "analyzer"
)

type BackyardDAO struct {
	Url   string
}

func (m *BackyardDAO) Connect() {
	session, err := mgo.Dial(m.Url)
	if err != nil {
		logrus.WithError(err).Fatal("failed to connect to mongodb")
	}
	db = session.DB("data")
}

func (m *BackyardDAO) SaveScanData(r io.Reader, name string) error {
	storage, err := db.GridFS("fs").Create(name)
	if err != nil {
		return fmt.Errorf("failed to create gridfs entry: %v", err)
	}
	defer storage.Close()

	_, err = io.Copy(storage, r)
	if err != nil {
		return fmt.Errorf("failed to copy image to gridfs: %v", err)
	}

	return err
}
