""" Testing LSS service """

from durand import Node

from ..mock_network import MockNetwork, TxMsg, RxMsg


def test_global_selection():
    """Test example starts with a node with an undefined node id (0xFF).
    After the "switch state global" request to set every responder into configuration mode,
    the node id is set to 1.

    When switching back to waiting state via "switch state global" the node sends
    an boot up message (because the node id was undefined before).

    SDO requests are tested on node 1 to see, if the responder is responding.
    """
    network = MockNetwork()

    # create the node
    node = Node(network, node_id=0xFF)

    network.test(
        [
            RxMsg(
                0x7E5, "04 01 00 00 00 00 00 00"
            ),  # switch state global to configuration state
            RxMsg(0x7E5, "11 01 00 00 00 00 00 00"),  # set node id to 1
            TxMsg(0x7E4, "11 00 00 00 00 00 00 00"),  # receive the acknowledge
            RxMsg(
                0x601, "40 00 10 00 00 00 00 00"
            ),  # requesting via SDO on node 1 will still be unanswered
            RxMsg(
                0x7E5, "04 00 00 00 00 00 00 00"
            ),  # switch state global back to waiting state
            TxMsg(0x701, "00"),  # responder responses with Boot Up message
            RxMsg(0x601, "40 00 10 00 00 00 00 00"),  # requesting via SDO on node 1
            TxMsg(0x581, "43 00 10 00 00 00 00 00"),  # receive the acknowledge
        ]
    )
