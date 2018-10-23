#!/usr/bin/env python3

import connexion


def main():
    app = connexion.App(__name__, specification_dir='./')
    # app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Cyber fighters backyard REST API'})
    app.run(port=8080)


if __name__ == '__main__':
    main()
