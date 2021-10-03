# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import json
import time

def send_message(client_id, message):

    endpoint = 'a1rgstrntakbmi-ats.iot.us-east-2.amazonaws.com'
    port = 8883
    cert = './certificates/Cardano_node.cert.pem'
    key = './certificates/Cardano_node.private.key'
    root_ca = './certificates/root-CA.crt'
    topic = 'test/topic'
    use_websocket = True
    region = 'us-east-2'

    # This sample uses the Message Broker for AWS IoT to send and receive messages
    # through an MQTT connection. On startup, the device connects to the server,
    # subscribes to a topic, and begins publishing messages to that topic.
    # The device should receive those same messages back from the message broker,
    # since it is subscribed to that same topic.

    received_all_event = threading.Event()

    # Callback when connection is accidentally lost.
    def on_connection_interrupted(connection, error, **kwargs):
        print("Connection interrupted. error: {}".format(error))


    # Callback when an interrupted connection is re-established.
    def on_connection_resumed(connection, return_code, session_present, **kwargs):
        print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

        if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
            print("Session did not persist. Resubscribing to existing topics...")
            resubscribe_future, _ = connection.resubscribe_existing_topics()

            # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
            # evaluate result with a callback instead.
            resubscribe_future.add_done_callback(on_resubscribe_complete)


    def on_resubscribe_complete(resubscribe_future):
            resubscribe_results = resubscribe_future.result()
            print("Resubscribe results: {}".format(resubscribe_results))

            for topic, qos in resubscribe_results['topics']:
                if qos is None:
                    sys.exit("Server rejected resubscribe to topic: {}".format(topic))

    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    if use_websocket == True:
        credentials_provider = auth.AwsCredentialsProvider.new_default_chain(client_bootstrap)
        mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
            endpoint=endpoint,
            client_bootstrap=client_bootstrap,
            region=region,
            credentials_provider=credentials_provider,
            http_proxy_options=None,
            ca_filepath=root_ca,
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=client_id,
            clean_session=False,
            keep_alive_secs=30)

    else:
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=endpoint,
            port=port,
            cert_filepath=cert,
            pri_key_filepath=key,
            client_bootstrap=client_bootstrap,
            ca_filepath=root_ca,
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=client_id,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=None)

    print("Connecting to {} with client ID '{}'...".format(
        endpoint, client_id))

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Publish message to server desired number of times.
    # This step is skipped if message is blank.
    # This step loops forever if count was set to 0.
    if message:
        message = "{} [{}]".format(message, 1)
        print("Publishing message to topic '{}': {}".format(topic, message))
        message_json = json.dumps(message)
        mqtt_connection.publish(
            topic=topic,
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE)
        time.sleep(1)

    received_all_event.set()
    # if obj:
        #while not q.empty():

    # Wait for all messages to be received.
    # This waits forever if count was set to 0.
    # if args.count != 0 and not received_all_event.is_set():
    #     print("Waiting for all messages to be received...")

    # Prevents the execution of the code below (Disconnet) while received_all_event flag is False
    received_all_event.wait()


    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")