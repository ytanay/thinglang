def test_input_single_line():
    with patch('sys.stdin', io.StringIO('single input line')):
        assert run("""
thing Program
    does start
        text input = Input.get_line()
        Output.write("Input is:", input)
        """).output == "Input is: single input line"


def test_input_multiple_lines():
    with patch('sys.stdin', io.StringIO('first line\nsecond line')):
        assert run("""
thing Program
    does start
        text input = Input.get_line()
        Output.write("1:", input)
        Output.write("2:", Input.get_line())
        """).output == "1: first line\n2: second line"


def test_eof():
    with pytest.raises(EOFError), patch('sys.stdin', io.StringIO('')):
        assert run("""
thing Program
    does start
        Input.get_line()
        """)

