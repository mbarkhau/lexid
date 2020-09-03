# pylint:disable=protected-access ; allowed for test code

import random

import lexid


def test_next_id_basic():
    assert lexid.next_id("01") == "02"
    assert lexid.next_id("09") == "110"


def test_next_id_overflow():
    try:
        prev_id = "9999"
        next_id = lexid.next_id(prev_id)
        assert False, (prev_id, "->", next_id)
    except OverflowError:
        pass


def test_next_id_random():
    for _ in range(1000):
        prev_id = str(random.randint(1, 100 * 1000))
        try:
            next_id = lexid.next_id(prev_id)
            assert prev_id < next_id
        except OverflowError:
            assert len(prev_id) == prev_id.count("9")


def test_ord_val():
    assert lexid.ord_val("1"  ) == 1
    assert lexid.ord_val("01" ) == 1
    assert lexid.ord_val("02" ) == 2
    assert lexid.ord_val("09" ) == 9
    assert lexid.ord_val("110") == 10


def test_main(capsys):
    lexid._main()
    captured = capsys.readouterr()
    assert len(captured.err) == 0

    lines  = iter(captured.out.splitlines())
    header = next(lines)

    assert "lexical" in header
    assert "numerical" in header

    ids      = []
    ord_vals = []

    for line in lines:
        if "..." in line:
            continue
        _id, _ord_val = line.split()

        assert _id.endswith(_ord_val)
        assert int(_ord_val) == int(_ord_val, 10)

        ids.append(_id.strip())
        ord_vals.append(int(_ord_val.strip()))

    assert len(ids) > 0
    assert sorted(ids) == ids
    assert sorted(ord_vals) == ord_vals
