package api

import (
	"fmt"
	"github.com/cyber-fighters/backyard/proto"
	"github.com/golang/protobuf/proto"
	"github.com/google/uuid"
	"github.com/sirupsen/logrus"
	"time"
)

type ScannerRun struct {
	name        string
	status      busapi.Status
	description string
	completed   uint32
}

type AnalysisRun struct {
	pendingScanners []*ScannerRun
}

var (
	pendingAnalysis map[string]*AnalysisRun
)

func handleDoAnalysis(_, reply string, request *busapi.AnalyserRequest) {
	logrus.Infof("incoming analysis request for %q", request.Domain)

	resp := &busapi.AnalyserResponse{}
	defer enc.Publish(reply, resp)

	// Create new analyser request
	analysisId, err := uuid.NewRandom()
	if err != nil {
		logrus.WithError(err).Errorf("failed to generate random UUID")
		resp.Code = busapi.ResultCode_FAIL
		return
	}

	run := AnalysisRun{}

	if uint32(request.Scanner)&uint32(busapi.Scanner_HARVESTER) > 0 {
		run.pendingScanners = append(run.pendingScanners, &ScannerRun{name: "harvester"})
	}
	if uint32(request.Scanner)&uint32(busapi.Scanner_SPIDERFOOT) > 0 {
		run.pendingScanners = append(run.pendingScanners, &ScannerRun{name: "spiderfoot"})
	}

	if len(run.pendingScanners) == 0 {
		logrus.Warn("no scanners selected")
		resp.Code = busapi.ResultCode_FAIL
		return
	}

	// Send scanner requests for each desired scanner
	for _, scanner := range run.pendingScanners {
		scanResponse := &busapi.ScanResponse{}
		err := enc.Request(fmt.Sprintf("scan.request.%s", scanner.name),
			&busapi.ScanRequest{Domain: request.Domain},
			scanResponse, 500*time.Millisecond)
		if err != nil {
			logrus.WithError(err).Errorf("failed to send scan request to scanner %q", scanner.name)
			resp.Code = busapi.ResultCode_FAIL
			return
		}

		if scanResponse.Code != busapi.ResultCode_OK {
			logrus.WithError(err).Errorf("failed to setup scanner %q", scanner.name)
			resp.Code = busapi.ResultCode_FAIL
			return
		}
	}

	pendingAnalysis[analysisId.String()] = &run
}

func handleScanCompleted(subject string, msg *busapi.ScanCompleted) {
	logrus.Infof("received %q", subject)
	fmt.Println(subject)
	fmt.Println(proto.MarshalTextString(msg))

	// TODO: If all scans are completed -> ready
	ready := true
	for _, scan := range pendingAnalysis[msg.Id].pendingScanners {
		if scan.completed != 100 {
			ready = false
			break
		}
	}

	if ready {
		fmt.Println("*** all scans done")
	}
}

func handleScanStatus(subject string, msg *busapi.ScanCompleted) {
	logrus.Infof("received %q", subject)
	fmt.Println(subject)
	fmt.Println(proto.MarshalTextString(msg))

	// Dummy calculation for the over all percentage

}
