from characters.boy import Boy


def test_boy_is_created_with_correct_attributes():
    boy = Boy((100, 100), 7.5, (20, 0))
    assert boy.__dict__.keys() == ['brain', 'substance', 'sprite', 'movement']
