def run(image, a_id, domain):
    # TODO: Run docker image/kubernetes POD creation
    
    print('$ docker run --net=host -e DOMAIN="%s" -e ANALYZER="%s" %s' % (domain, a_id, image))