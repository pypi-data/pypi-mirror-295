"""
The Javonet module is a singleton module that serves as the entry point for interacting with Javonet.
It provides functions to activate and initialize the Javonet SDK.
It supports both in-memory and TCP connections.
Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/javonet-static-class>`_ for more information.
"""
from javonet.core.transmitter.Transmitter import Transmitter
from javonet.utils.ConnectionType import ConnectionType
from javonet.sdk.RuntimeFactory import RuntimeFactory
from javonet.sdk.ConfigRuntimeFactory import ConfigRuntimeFactory
from javonet.utils.connectionData.InMemoryConnectionData import InMemoryConnectionData
from javonet.utils.connectionData.TcpConnectionData import TcpConnectionData
from javonet.utils.connectionData.WsConnectionData import WsConnectionData
from javonet.sdk.tools.SdkExceptionHelper import SdkExceptionHelper

try:
    Transmitter.activate("")
except Exception as ex:
    SdkExceptionHelper.send_exception_to_app_insights(ex, "Javonet")
    raise ex


def in_memory():
    """
    Initializes Javonet using an in-memory channel on the same machine.
    
    Returns:
        RuntimeFactory: An instance configured for an in-memory connection.
    Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/in-memory-channel>`_ for more information.
    """
    return RuntimeFactory(InMemoryConnectionData())


def tcp(tcp_connection_data: TcpConnectionData):
    """
    Initializes Javonet with a TCP connection to a remote machine.
    
    Args:
        tcp_connection_data (str): The address of the remote machine.
        
    Returns:
        RuntimeFactory: An instance configured for a TCP connection.
    Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/tcp-channel>`_ for more information.
    """
    return RuntimeFactory(tcp_connection_data)


def ws(ws_connection_data: WsConnectionData):
    """
    Initializes Javonet with a WebSocket connection to a remote machine.

    Args:
        ws_connection_data (str): The address of the remote machine.

    Returns:
        RuntimeFactory: An instance configured for a WebSocket connection.
    Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/websocket-channel>`_ for more information.
    """
    return RuntimeFactory(ws_connection_data)


def with_config(path):
    """
    Initializes Javonet with a configuration taken from external source.
    Currently supported: Configuration file in JSON format
    
    Args:
        path (str): Path to a configuration file.
        
    Returns:
        ConfigRuntimeFactory: An instance configured with configuration data.
    Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/configure-channel>`_ for more information.
    """
    try:
        Transmitter.set_config_source(path)
        return ConfigRuntimeFactory(path)
    except Exception as exception:
        SdkExceptionHelper.send_exception_to_app_insights(exception, "withConfig")
        raise exception


def activate(license_key):
    """
    Activates Javonet with the provided license key.

    Args:
        license_key (str): The license key to activate Javonet.

    Returns:
        int: The activation status code.
    Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/getting-started/activating-javonet>`_ for more information.
    """
    try:
        return Transmitter.activate(license_key)
    except Exception as exception:
        SdkExceptionHelper.send_exception_to_app_insights(exception, license_key)
        raise exception
