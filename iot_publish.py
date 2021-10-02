
import argparse
import json


parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")

parser.add_argument(
        '--config_file',
        dest='config_file',
        type=str,
        default=None,
        help='config file',
    )

parser.add_argument('--endpoint',  help="Your AWS IoT custom endpoint, not including a port. " +
                                                      "Ex: \"abcd123456wxyz-ats.iot.us-east-1.amazonaws.com\"")
parser.add_argument('--port', type=int, default='8883', help="Specify port. AWS IoT supports 443 and 8883.")
parser.add_argument('--cert', default= './certificates/Cardano_node.cert.pem', help="File path to your client certificate, in PEM format.")
parser.add_argument('--key', default= './certificates/Cardano_node.private.key', help="File path to your private key, in PEM format.")
parser.add_argument('--root-ca', default= './certificates/root-CA.crt', help="File path to root certificate authority, in PEM format. " +
                                      "Necessary if MQTT server uses a certificate that's not already in " +
                                      "your trust store.")

args, unknown = parser.parse_known_args()
# Using globals to simplify sample code
args = parser.parse_args()

config = json.load(open('./config_file.json'))
parser.set_defaults(**config)

[
            parser.add_argument(arg)
            for arg in [arg for arg in unknown if arg.startswith('--')]
            if arg.split('--')[-1] in config
        ]

print(args.endpoint)