import filters

def test_empty_inputs():
    for filter in filters.FILTERS:
        if filter in [
            filters.Length,
            filters.Blocklist,
            filters.BlocklistFromJSON,
            filters.PersonalInformation
        ]:
            continue
        print(filter)
        assert filter().check("")[0]

def test_blocklist():
    l = {
        "badword",
        "pancake"
    }

    f = filters.Blocklist(l)

    assert f.check("This is a badword.")[0] == False
    assert f.check("This is a ppancakee.")[0] == True

def test_strict_blocklist():
    l = {
        "pancake"
    }

    f = filters.Blocklist(l, mode = "strict")
    
    assert f.check("This is a ppancakee.")[0] == False
    assert f.check("This is a ppanccakee.")[0] == True