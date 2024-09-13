import concurrent.futures
import json
import os
import ssl
from dataclasses import dataclass
from socket import gaierror
from typing import Any, Callable, Dict, Tuple, Union, List
import time
import pika
from pika import SSLOptions
from pika.exceptions import ChannelClosedByBroker, ConnectionClosedByBroker
from pika.exchange_type import ExchangeType
from retry import retry
from neolibrary.monitoring.logger import NeoLogger

from mrsal.config import config
from mrsal.utils import utils

logger = NeoLogger(__name__, rotate_days=config.LOGGER_ROTATE_DAYS)



@dataclass
# NOTE! change the doc style to google or numpy
class Mrsal:
    """
    Mrsal creates a layer on top of Pika's core, providing methods to setup a RabbitMQ broker with multiple functionalities.

    Properties:
        :prop str host: Hostname or IP Address to connect to
        :prop int port: TCP port to connect to
        :prop pika.credentials.Credentials credentials: auth credentials
        :prop str virtual_host: RabbitMQ virtual host to use
        :prop bool verbose: If True then more INFO logs will be printed
        :prop int heartbeat: Controls RabbitMQ's server heartbeat timeout negotiation
            during connection tuning.
        :prop int blocked_connection_timeout: blocked_connection_timeout
            is the timeout, in seconds,
            for the connection to remain blocked; if the timeout expires,
                the connection will be torn down
        :prop int prefetch_count: Specifies a prefetch window in terms of whole messages.
        :prop bool ssl: Set this flag to true if you want to connect externally to the rabbit server.
    """

    host: str
    port: str
    credentials: Tuple[str, str]
    virtual_host: str
    ssl: bool = False
    verbose: bool = False
    prefetch_count: int = 1
    heartbeat: int = 600  # sec
    blocked_connection_timeout: int = 300  # sec
    _connection: pika.BlockingConnection = None
    _channel = None

    def connect_to_server(self, context: Dict[str, str] = None):
        """We can use connect_to_server for establishing a connection to RabbitMQ server specifying connection parameters.

        Parameters
        ----------
        context : Dict[str, str]
            context is the structured map with information regarding the SSL options for connecting with rabbit server via TLS.
        """
        connection_info = f"""
                            Mrsal connection parameters:
                            host={self.host},
                            virtual_host={self.virtual_host},
                            port={self.port},
                            heartbeat={self.heartbeat},
                            ssl={self.ssl}
                            """
        if self.verbose:
            logger.info(f"Establishing connection to RabbitMQ on {connection_info}")
        if self.ssl:
            logger.info("Setting up TLS connection")
            context = self.__ssl_setup()
        ssl_options = SSLOptions(context, self.host) if context else None
        credentials = pika.PlainCredentials(*self.credentials)
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    ssl_options=ssl_options,
                    virtual_host=self.virtual_host,
                    credentials=credentials,
                    heartbeat=self.heartbeat,
                    blocked_connection_timeout=self.blocked_connection_timeout,
                )
            )
            self._channel: pika.adapters.blocking_connection.BlockingChannel = self._connection.channel()
            # Note: prefetch is set to 1 here as an example only.
            # In production you will want to test with different prefetch values to find which one provides the best performance and usability for your solution.
            self._channel.basic_qos(prefetch_count=self.prefetch_count)
            logger.info(f"Connection established with RabbitMQ on {connection_info}")
            return self._connection
        except pika.exceptions.AMQPConnectionError as err:
            msg: str = f"I tried to connect with the RabbitMQ server but failed with: {err}"
            logger.error(msg)
            raise pika.exceptions.AMQPConnectionError(msg)

    def setup_exchange(self, exchange: str, exchange_type: str, arguments: Dict[str, str] = None, durable=True, passive=False, internal=False, auto_delete=False):
        """This method creates an exchange if it does not already exist, and if the exchange exists, verifies that it is of the correct and expected class.

        If passive set, the server will reply with Declare-Ok if the exchange already exists with the same name,
        and raise an error if not and if the exchange does not already exist, the server MUST raise a channel exception with reply code 404 (not found).

        :param str exchange: The exchange name
        :param str exchange_type: The exchange type to use
        :param bool passive: Perform a declare or just check to see if it exists
        :param bool durable: Survive a reboot of RabbitMQ
        :param bool auto_delete: Remove when no more queues are bound to it
        :param bool internal: Can only be published to by other exchanges
        :param dict arguments: Custom key/value pair arguments for the exchange
        :returns: Method frame from the Exchange.Declare-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type `spec.Exchange.DeclareOk`@
        """
        exchange_declare_info = f"""
                                exchange={exchange},
                                exchange_type={exchange_type},
                                durable={durable},
                                passive={passive},
                                internal={internal},
                                auto_delete={auto_delete},
                                arguments={arguments}
                                """
        if self.verbose:
            logger.info(f"Declaring exchange with: {exchange_declare_info}")
        try:
            exchange_declare_result = self._channel.exchange_declare(
                exchange=exchange, exchange_type=exchange_type, arguments=arguments, durable=durable, passive=passive, internal=internal, auto_delete=auto_delete
            )
            if self.verbose:
                logger.info(f"Exchange is declared successfully: {exchange_declare_info}, result={exchange_declare_result}")
            return exchange_declare_result
        except (TypeError, AttributeError, ChannelClosedByBroker, ConnectionClosedByBroker) as err:
            msg: str = f"I tried to declare an exchange but failed with: {err}"
            logger.error(msg)
            raise pika.exceptions.ConnectionClosedByBroker(503, msg)

    def setup_queue(self, queue: str, arguments: Dict[str, str] = None, durable: bool = True, exclusive: bool = False, auto_delete: bool = False, passive: bool = False):
        """Declare queue, create if needed. This method creates or checks a queue.
        When creating a new queue the client can specify various properties that control the durability of the queue and its contents,
        and the level of sharing for the queue.

        Use an empty string as the queue name for the broker to auto-generate one.
        Retrieve this auto-generated queue name from the returned `spec.Queue.DeclareOk` method frame.

        :param str queue: The queue name; if empty string, the broker will create a unique queue name
        :param bool passive: Only check to see if the queue exists and raise `ChannelClosed` if it doesn't
        :param bool durable: Survive reboots of the broker
        :param bool exclusive: Only allow access by the current connection
        :param bool auto_delete: Delete after consumer cancels or disconnects
        :param dict arguments: Custom key/value arguments for the queue
        :returns: Method frame from the Queue.Declare-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type `spec.Queue.DeclareOk`
        """
        queue_declare_info = f"""
                                queue={queue},
                                durable={durable},
                                exclusive={exclusive},
                                auto_delete={auto_delete},
                                arguments={arguments}
                                """
        if self.verbose:
            logger.info(f"Declaring queue with: {queue_declare_info}")

        queue_declare_result = self._channel.queue_declare(queue=queue, arguments=arguments, durable=durable, exclusive=exclusive, auto_delete=auto_delete, passive=passive)
        if self.verbose:
            logger.info(f"Queue is declared successfully: {queue_declare_info},result={queue_declare_result.method}")
        return queue_declare_result


    def setup_queue_binding(self, exchange: str, queue: str, routing_key: str = None, arguments=None):
        """Bind queue to exchange.

        :param str queue: The queue to bind to the exchange
        :param str exchange: The source exchange to bind to
        :param str routing_key: The routing key to bind on
        :param dict arguments: Custom key/value pair arguments for the binding

        :returns: Method frame from the Queue.Bind-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type `spec.Queue.BindOk`
        """
        if self.verbose:
            logger.info(f"Binding queue to exchange: queue={queue}, exchange={exchange}, routing_key={routing_key}")

        bind_result = self._channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key, arguments=arguments)
        if self.verbose:
            logger.info(f"The queue is bound to exchange successfully: queue={queue}, exchange={exchange}, routing_key={routing_key}, result={bind_result}")
        return bind_result
    
    def __ssl_setup(self) -> Dict[str, str]:
        """__ssl_setup is private method we are using to connect with rabbit server via signed certificates and some TLS settings.

        Parameters
        ----------

        Returns
        -------
        Dict[str, str]

        """
        context = ssl.create_default_context(cafile=os.environ.get("RABBITMQ_CAFILE"))
        context.load_cert_chain(certfile=os.environ.get("RABBITMQ_CERT"), keyfile=os.environ.get("RABBITMQ_KEY"))
        return context

    def stop_consuming(self, consumer_tag: str) -> None:
        self._channel.stop_consuming(consumer_tag=consumer_tag)
        logger.info(f"Consumer is stopped, carry on. consumer_tag={consumer_tag}")

    def close_channel(self) -> None:
        self._channel.close()
        logger.info("Channel is closed, carry on")

    def close_connection(self) -> None:
        self.close_channel()
        self._connection.close()
        logger.info("Connection is closed, carry on")

    def queue_delete(self, queue: str):
        self._channel.queue_delete(queue=queue)

    def exchange_delete(self, exchange: str):
        self._channel.exchange_delete(exchange=exchange)

    def confirm_delivery(self):
        self._channel.confirm_delivery()

    def exchange_exist(self, exchange: str, exchange_type: ExchangeType):
        exch_result: pika.frame.Method = self.setup_exchange(exchange=exchange, exchange_type=exchange_type, passive=True)
        return exch_result

    # NOTE! This is not a check but a setup function
    def queue_exist(self, queue: str):
        queue_result = self.setup_queue(queue=queue, passive=True)
        # message_count1 = result1.method.message_count
        return queue_result

    # --------------------------------------------------------------
    # --------------------------------------------------------------
    # TODO NOT IN USE: Need to reformat it to publish messages to dead letters exchange after exceeding retries limit
    def consume_messages_with_retries(
        self,
        queue: str,
        callback: Callable,
        callback_args=None,
        escape_after=-1,
        dead_letters_exchange: str = None,
        dead_letters_routing_key: str = None,
        prop: pika.BasicProperties = None,
        inactivity_timeout=None,
    ):
        logger.info(f"Consuming messages: queue= {queue}")

        try:
            for method_frame, properties, body in self._channel.consume(queue=queue, inactivity_timeout=inactivity_timeout):
                consumer_tags = self._channel.consumer_tags
                # Let the message be in whatever data type it needs to
                message = json.loads(body)
                exchange = method_frame.exchange
                routing_key = method_frame.routing_key
                delivery_tag = method_frame.delivery_tag
                if self.verbose:
                    logger.info(
                        f"consumer_callback info: exchange: {exchange}, routing_key: {routing_key}, delivery_tag: {delivery_tag}, properties: {properties}, consumer_tags: {consumer_tags}"
                    )
                is_processed = callback(*callback_args, message)
                logger.info(f"is_processed= {is_processed}")
                if is_processed:
                    self._channel.basic_ack(delivery_tag=delivery_tag)
                    logger.info("Message acknowledged")

                    if method_frame.delivery_tag == escape_after:
                        logger.info(f"Break! Max messages to be processed is {escape_after}")
                        break
                else:
                    logger.warning(f"Could not process the message= {message}. Process it as dead letter.")
                    is_dead_letter_published = self.publish_dead_letter(
                        message=message, delivery_tag=delivery_tag, dead_letters_exchange=dead_letters_exchange, dead_letters_routing_key=dead_letters_routing_key, prop=prop
                    )
                    if is_dead_letter_published:
                        self._channel.basic_ack(delivery_tag)
        except FileNotFoundError as e:
            logger.error(f"Connection closed with error: {e}")
            self._channel.stop_consuming()

    def start_consumer(
        self,
        queue: str,
        callback: Callable,
        callback_args: Tuple[str, Any] = None,
        auto_ack: bool = False,
        reject_unprocessed: bool = True,
        exchange: str = None,
        exchange_type: str = None,
        routing_key: str = None,
        inactivity_timeout: int = None,
        requeue: bool = False,
        fast_setup: bool = False,
        callback_with_delivery_info: bool = False,
        thread_num: int = None,
    ):
        """
        Setup consumer:
            1- Consumer start consuming the messages from the queue.
            2- If `inactivity_timeout` is given (in seconds) the consumer will be canceled when the time of inactivity exceeds inactivity_timeout.
            3- Send the consumed message to callback method to be processed, and then the message can be either:
                - Processed, then correctly-acknowledge and deleted from QUEUE or
                - Failed to process, negatively-acknowledged and then the message will be rejected and either
                    - Redelivered if 'x-retry-limit' and 'x-retry' are configured in 'BasicProperties.headers'.
                    - Requeued if requeue is True
                    - Sent to dead-letters-exchange if it configured and
                        - requeue is False
                        - requeue is True and requeue attempt fails.
                    - Unless deleted.


        :param str queue: The queue name to consume
        :param Callable callback: Method where received messages are sent to be processed
        :param Tuple callback_args: Tuple of arguments for callback method
        :param bool auto_ack: If True, then when a message is delivered to a consumer, it is automatically marked as acknowledged and removed from the queue without any action needed from the consumer.
        :param bool reject_unprocessed: If True(Default), then when a message is not processed correctly by the callback method, then the message will be rejected.
        :param float inactivity_timeout:
            - if a number is given (in seconds), will cause the method to yield (None, None, None) after the given period of inactivity.
            - If None is given (default), then the method blocks until the next event arrives.
        :param bool requeue: If requeue is true, the server will attempt to
                             requeue the message. If requeue is false or the
                             requeue attempt fails the messages are discarded or
                             dead-lettered.
        :param bool callback_with_delivery_info: Specify whether the callback method needs delivery info.
                - spec.Basic.Deliver: Captures the fields for delivered message. E.g:(consumer_tag, delivery_tag, redelivered, exchange, routing_key).
                - spec.BasicProperties: Captures the client message sent to the server. E.g:(CONTENT_TYPE, DELIVERY_MODE, MESSAGE_ID, APP_ID).
        :param bool fast_setup:
                - when True, the method will create the specified exchange, queue
                and bind them together using the routing kye.
                - If False, this method will check if the specified exchange and queue
                already exist before start consuming.
        """
        print_thread_index = f"Thread={str(thread_num)} -> " if thread_num else ""
        logger.info(f"{print_thread_index}Consuming messages: queue={queue}, requeue={requeue}, inactivity_timeout={inactivity_timeout}")
        if fast_setup:
            # Setting up the necessary connections
            self.setup_exchange(exchange=exchange, exchange_type=exchange_type)
            self.setup_queue(queue=queue)
            self.setup_queue_binding(exchange=exchange, queue=queue, routing_key=routing_key)
        else:
            # Check if the necessary resources (exch & queue) are active
            try:
                if exchange and exchange_type:
                    self.exchange_exist(exchange=exchange, exchange_type=exchange_type)
                self.queue_exist(queue=queue)
            except pika.exceptions.ChannelClosedByBroker as err:
                err_msg: str = f"I tried checking if the exchange and queue exist but failed with: {err}"
                logger.error(err_msg)
                logger.info("Closing the channel")
                self._channel.cancel()
                raise pika.exceptions.ChannelClosedByBroker(404, str(err))
        try:
            self.consumer_tag = None
            method_frame: pika.spec.Basic.Deliver
            properties: pika.spec.BasicProperties
            body: Any
            for method_frame, properties, body in self._channel.consume(queue=queue, auto_ack=auto_ack, inactivity_timeout=inactivity_timeout):
                try:
                    if (method_frame, properties, body) != (None, None, None):
                        consumer_tags = self._channel.consumer_tags
                        self.consumer_tag = method_frame.consumer_tag
                        app_id = properties.app_id
                        msg_id = properties.message_id
                        if self.verbose:
                            logger.info(
                                f"""
                                Consumed message:
                                method_frame={method_frame},
                                redelivered={method_frame.redelivered},
                                exchange={method_frame.exchange},
                                routing_key={method_frame.routing_key},
                                delivery_tag={method_frame.delivery_tag},
                                properties={properties},
                                consumer_tags={consumer_tags},
                                consumer_tag={self.consumer_tag}
                                """
                            )

                        if auto_ack:
                            logger.info(f"{print_thread_index}Message coming from the app={app_id} with messageId={msg_id} is AUTO acknowledged.")
                        if callback_with_delivery_info:
                            is_processed = callback(*callback_args, method_frame, properties, body) if callback_args else callback(method_frame, properties, body)
                        else:
                            is_processed = callback(*callback_args, body) if callback_args else callback(body)

                        if is_processed:
                            logger.info(f"{print_thread_index}Message coming from the app={app_id} with messageId={msg_id} is processed correctly.")
                            if not auto_ack:
                                self._channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                                logger.info(f"{print_thread_index}Message coming from the app={app_id} with messageId={msg_id} is acknowledged.")

                        else:
                            logger.warning(f"{print_thread_index}Could not process the message coming from the app={app_id} with messageId={msg_id}.")
                            if not auto_ack and reject_unprocessed:
                                self._channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=requeue)
                                logger.info(f"{print_thread_index}Message coming from the app={app_id} with messageId={msg_id} is rejected.")
                            if utils.is_redelivery_configured(properties):
                                msg_headers = properties.headers
                                x_retry = msg_headers[config.RETRY_KEY]
                                x_retry_limit = msg_headers[config.RETRY_LIMIT_KEY]
                                logger.warning(f"{print_thread_index}Redelivery options are configured in message headers: x-retry={x_retry}, x-retry-limit={x_retry_limit}")
                                if x_retry < x_retry_limit:
                                    logger.warning(f"{print_thread_index}Redelivering the message with messageId={msg_id}.")
                                    msg_headers[config.RETRY_KEY] = x_retry + 1
                                    prop_redeliver = pika.BasicProperties(
                                        app_id=app_id,
                                        message_id=msg_id,
                                        content_type=config.CONTENT_TYPE,
                                        content_encoding=config.CONTENT_ENCODING,
                                        delivery_mode=pika.DeliveryMode.Persistent,
                                        headers=msg_headers,
                                    )
                                    self._channel.basic_publish(exchange=method_frame.exchange, routing_key=method_frame.routing_key, body=body, properties=prop_redeliver)
                                    logger.warning(f"{print_thread_index}Message with messageId={msg_id} is successfully redelivered.")
                                else:
                                    logger.warning(f"{print_thread_index}Max number of redeliveries ({x_retry_limit}) are reached for messageId={msg_id}.")
                        logger.info(f"[*] {print_thread_index} keep listening on {queue}...")
                    else:
                        logger.warning(f"{print_thread_index}Given period of inactivity {inactivity_timeout} is exceeded. Cancel consumer.")
                        self.stop_consuming(self.consumer_tag)
                        self._channel.cancel()
                except pika.exceptions.ConnectionClosedByBroker as err:
                    logger.error(f"{print_thread_index}I lost the connection with the Mrsal. {err}", exc_info=True)
                    self._channel.cancel()
                    raise pika.exceptions.ConnectionClosedByBroker(503, str(err))
                except KeyboardInterrupt:
                    logger(f"{print_thread_index}Stopping Mrsal consumption.")
                    self.stop_consuming(self.consumer_tag)
                    self.close_connection()
                    break
        except pika.exceptions.ChannelClosedByBroker as err2:
            logger.error(f"{print_thread_index}ChannelClosed is caught while consuming. Channel is closed by broker. Cancel consumer. {str(err2)}")
            self._channel.cancel()
            raise pika.exceptions.ChannelClosedByBroker(404, str(err2))

    def _spawn_mrsal_and_start_new_consumer(
        self,
        thread_num: int,
        queue: str,
        callback: Callable,
        callback_args: Tuple[str, Any] = None,
        exchange: str = None,
        exchange_type: str = None,
        routing_key: str = None,
        inactivity_timeout: int = None,
        requeue: bool = False,
        fast_setup: bool = False,
        callback_with_delivery_info: bool = False,
    ):
        try:
            logger.info(f"thread_num={thread_num} -> Start consumer")
            mrsal_obj = Mrsal(
                host=self.host,
                port=self.port,
                credentials=self.credentials,
                virtual_host=self.virtual_host,
                ssl=self.ssl,
                verbose=self.verbose,
                prefetch_count=self.prefetch_count,
                heartbeat=self.heartbeat,
                blocked_connection_timeout=self.blocked_connection_timeout,
            )
            mrsal_obj.connect_to_server()

            mrsal_obj.start_consumer(
                callback=callback,
                callback_args=callback_args,
                queue=queue,
                requeue=requeue,
                exchange=exchange,
                exchange_type=exchange_type,
                routing_key=routing_key,
                fast_setup=fast_setup,
                inactivity_timeout=inactivity_timeout,
                callback_with_delivery_info=callback_with_delivery_info,
                thread_num=thread_num,
            )

            mrsal_obj.stop_consuming(mrsal_obj.consumer_tag)
            mrsal_obj.close_connection()
            logger.info(f"thread_num={thread_num} -> End consumer")
        except Exception as e:
            logger.error(f"thread_num={thread_num} -> Failed to consumer: {e}")

    def start_concurrence_consumer(
        self,
        total_threads: int,
        queue: str,
        callback: Callable,
        callback_args: Tuple[str, Any] = None,
        exchange: str = None,
        exchange_type: str = None,
        routing_key: str = None,
        inactivity_timeout: int = None,
        requeue: bool = False,
        fast_setup: bool = False,
        callback_with_delivery_info: bool = False,
    ):
        with concurrent.futures.ThreadPoolExecutor(max_workers=total_threads) as executor:
            executor.map(
                self._spawn_mrsal_and_start_new_consumer,
                range(total_threads),
                [queue] * total_threads,
                [callback] * total_threads,
                [callback_args] * total_threads,
                [exchange] * total_threads,
                [exchange_type] * total_threads,
                [routing_key] * total_threads,
                [inactivity_timeout] * total_threads,
                [requeue] * total_threads,
                [fast_setup] * total_threads,
                [callback_with_delivery_info] * total_threads,
            )

    def publish_message(
        self,
        exchange: str,
        routing_key: str,
        message: Any,
        exchange_type: ExchangeType = ExchangeType.direct,
        queue: str = None,
        fast_setup: bool = False,
        prop: pika.BasicProperties = None,
    ):
        """Publish message to the exchange specifying routing key and properties.

        :param str exchange: The exchange to publish to
        :param str routing_key: The routing key to bind on
        :param bytes body: The message body; empty string if no body
        :param pika.spec.BasicProperties properties: message properties
        :param bool fast_setup:
                - when True, will the method create the specified exchange, queue and bind them together using the routing kye.
                - If False, this method will check if the specified exchange and queue already exist before publishing.

        :raises UnroutableError: raised when a message published in publisher-acknowledgments mode (see `BlockingChannel.confirm_delivery`) is returned via `Basic.Return` followed by `Basic.Ack`.
        :raises NackError: raised when a message published in publisher-acknowledgements mode is Nack'ed by the broker. See `BlockingChannel.confirm_delivery`.
        """
        if fast_setup:
            # setting up the necessary connections
            self.setup_exchange(exchange=exchange, exchange_type=exchange_type)
            self.setup_queue(queue=queue)
            self.setup_queue_binding(exchange=exchange, queue=queue, routing_key=routing_key)
        else:
            # Check if the necessary resources (exch & queue) are active
            try:
                self.exchange_exist(exchange=exchange, exchange_type=exchange_type)
                if queue is not None:
                    self.queue_exist(queue=queue)
            except pika.exceptions.ChannelClosedByBroker as err:
                logger.error(f"Failed to check active resources. Cancel consumer. {str(err)}")
                self._channel.cancel()
                raise pika.exceptions.ChannelClosedByBroker(404, str(err))

        try:
            # Publish the message by serializing it in json dump
            self._channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(message), properties=prop)
            logger.info(f"Message ({message}) is published to the exchange {exchange} with a routing key {routing_key}")

            # The message will be returned if no one is listening
            return True
        except pika.exceptions.UnroutableError as err1:
            logger.error(f"Producer could not publish message:{message} to the exchange {exchange} with a routing key {routing_key}: {err1}", exc_info=True)
            raise pika.exceptions.UnroutableError(404, str(err1))

    # TODO NOT IN USE: maybe we will use it in the method consume_messages_with_retries
    # to publish messages to dead letters exchange after retries limit. (remove or use)
    def publish_dead_letter(self, message: str, delivery_tag: int, dead_letters_exchange: str = None, dead_letters_routing_key: str = None, prop: pika.BasicProperties = None):
        if dead_letters_exchange is not None and dead_letters_routing_key is not None:
            logger.warning(f"Re-route the message={message} to the exchange={dead_letters_exchange} with routing_key={dead_letters_routing_key}")
            try:
                self.publish_message(exchange=dead_letters_exchange, routing_key=dead_letters_routing_key, message=json.dumps(message), properties=prop)
                logger.info(f"Dead letter was published: message={message}, exchange={dead_letters_exchange}, routing_key={dead_letters_routing_key}")
                return True
            except pika.exceptions.UnroutableError as e:
                logger.error(f"Dead letter was returned with error: {e}")
                return False
    
    @retry((
        gaierror,
        pika.exceptions.AMQPConnectionError,
        pika.exceptions.StreamLostError,
        pika.exceptions.ConnectionClosedByBroker,
        pika.exceptions.ChannelClosedByBroker,
        ), tries=15, delay=1, jitter=(2, 10), logger=logger)
    def full_setup(
            self,
            exchange: str = None,
            exchange_type: str = None,
            arguments: Dict[str, str] = None,
            routing_key: str = None,
            queue: str = None,
            callback: Callable = None,
            requeue: bool = False,
            callback_with_delivery_info: bool = False,
            auto_ack: bool = False,
            fast_setup: bool = True,
    ) -> None:
        """
        Sets up the connection, exchange, queue, and consumer for interacting with a RabbitMQ server.

        This method configures the connection to the RabbitMQ server and sets up the required messaging
        components such as exchange, queue, and consumer. It also handles retries in case of connection failures.

        Parameters
        ----------
        exchange : str, optional
            The name of the exchange to declare. If `None`, no exchange will be declared. Default is `None`.
        exchange_type : str, optional
            The type of exchange to declare (e.g., 'direct', 'topic', 'fanout', 'headers'). Required if `exchange` is specified.
            Default is `None`.
        arguments : Dict[str, str], optional
            A dictionary of additional arguments to pass when declaring the exchange or queue. Default is `None`.
        routing_key : str, optional
            The routing key to bind the queue to the exchange. This is used to determine which messages go to which queue.
            Default is `None`.
        queue : str, optional
            The name of the queue to declare. If `None`, a randomly named queue will be created. Default is `None`.
        callback : Callable, optional
            A callback function to be executed when a message is received. The function should accept the message as a parameter.
            Default is `None`.
        requeue : bool, optional
            If `True`, failed messages will be requeued. This is used in cases where you want to retry processing a message later.
            Default is `False`.
        callback_with_delivery_info : bool, optional
            If `True`, the callback function will receive additional delivery information (e.g., delivery tag, redelivered flag).
            Default is `False`.
        auto_ack : bool, optional
            If `True`, messages will be automatically acknowledged as soon as they are delivered to the consumer.
            If `False`, messages need to be manually acknowledged. Default is `False`.

        Returns
        -------
        None
            This function does not return any value. It performs the setup and starts consuming messages.

        Raises
        ------
        pika.exceptions.AMQPConnectionError
            Raised if the connection to the RabbitMQ server fails after multiple retry attempts.
        pika.exceptions.ChannelClosedByBroker
            Raised if the channel is closed by the broker for some reason.
        pika.exceptions.ConnectionClosedByBroker
            Raised if the connection is closed by the broker.

        Example
        -------
        >>> major_setup(
                exchange='my_exchange',
                exchange_type='direct',
                routing_key='my_routing_key',
                queue='my_queue',
                callback=my_callback_function
            )
        """
        try:
            if fast_setup:
                logger.info("🗲 Setting up RabbitMQ with fast setup")
            self.connect_to_server()
            if not fast_setup:
                self.setup_exchange(exchange=exchange, exchange_type=exchange_type, arguments=arguments)
                self.setup_queue(queue=queue)
                self.setup_queue_binding(exchange=exchange, queue=queue, routing_key=routing_key)
            self.start_consumer(
                queue=queue,
                callback=callback,
                requeue=requeue,
                callback_with_delivery_info=callback_with_delivery_info,
                auto_ack=auto_ack,
                fast_setup=fast_setup,
                exchange=exchange,
                exchange_type=exchange_type,
                routing_key=routing_key,
            )
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ server: {e}")
            raise pika.exceptions.AMQPConnectionError(503, str(e))
        except pika.exceptions.ChannelClosedByBroker as e:
            logger.error(f"Channel is closed by the broker: {e}")
            raise pika.exceptions.ChannelClosedByBroker(404, str(e))
        except pika.exceptions.ConnectionClosedByBroker as e:
            logger.error(f"Connection is closed by the broker: {e}")
            raise pika.exceptions.ConnectionClosedByBroker(503, str(e))
        except Exception as e:
            logger.error(f"Failed to setup RabbitMQ: {e}")
            raise e



if __name__ == "__main__":

    # Main script testing


    def test_callback(
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
    ) -> None:
        consumer_tag = method.consumer_tag
        exchange = method.exchange
        routing_key = method.routing_key
        app_id = properties.app_id
        message_id = properties.message_id

        # Decode and parse the message body
        enc_payload: Dict[str, Union[str, int, List]] | str = json.loads(body)
        payload = enc_payload if isinstance(enc_payload, dict) else json.loads(enc_payload)

        print(f" [x] Received {payload}")

        print("Simulating a long running process")
        time.sleep(5)
        print("Process completed")
        return True

    # Example test
    print('\n\033[1;35;40m Start NeoCowboy Service \033[0m')

    Mrsal = Mrsal(
        host=config.RABBIT_DOMAIN,
        port=config.RABBITMQ_PORT_TLS,
        credentials=(config.RABBITMQ_CREDENTIALS),
        virtual_host=config.V_HOST,
        ssl=True,
        verbose=True,
    ).full_setup(
        exchange='exchangeRT',
        exchange_type='topic',
        routing_key='exchangeRT.mrsal_testQueue',
        queue='mrsal_testQueue',
        callback=test_callback,
        requeue=False,
        callback_with_delivery_info=True,
        auto_ack=True,
        fast_setup=True,
    )