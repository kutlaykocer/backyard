import logging
import subprocess


def run(image, a_id, domain):
    # TODO: Run docker image/kubernetes POD creation
    subprocess.Popen(["docker", "run", "-v", "/tmp/data:/data/%s" % domain, "--net=host", "-e",
                      "DOMAIN=%s" % domain, "-e", "ANALYZER=\"%s\"" % a_id,
                      image])
    logging.info('docker run -v /tmp/data:/data/%s --net=host -e DOMAIN="%s" -e ANALYZER="%s" %s' % (domain, domain, a_id, image))
