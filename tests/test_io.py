def test_input_single_line():
    with patch('sys.stdin', io.StringIO('single input line')):
        assert run("""
thing Program
    does start
        text input = Input.get_line()
        Output.write("Input is:", input)
        """).output == "Input is: single input line"

