from ssf.run import ping

def test_ping():
    listen = ping()

    assert listen == "pong"
