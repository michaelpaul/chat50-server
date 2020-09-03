def test_join_room(socket):
    socket.emit('chat50.join', {'channel': 'cs50'})
    assert socket.is_connected()
