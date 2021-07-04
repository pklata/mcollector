def test_local_can_be_add_to_building(building, local):
    building.add_local(local)
    assert local in building._locals
