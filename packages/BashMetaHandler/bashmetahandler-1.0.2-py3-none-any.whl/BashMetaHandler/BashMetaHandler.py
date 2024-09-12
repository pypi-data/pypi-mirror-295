"""start of main script of bash meta handler!"""
import datetime
import time
import typing
from typing import Union

import pexpect  # type: ignore


class MetaBashHandler:
    """Class Handles the interaction with a terminal via meta bash script."""

    def __init__(
        self,
        filename: str = "",
        variable_dict: typing.Dict[str, typing.Any] = {},
        function_dict: typing.Dict[
            str, Union[typing.Callable[..., typing.Any], None]
        ] = {},
    ):
        """Initiation for the MetaBashHandler class.

        Args:
            filename (str): metabash filename. Defaults to "".
            variable_dict (dict): dictionary of variables keys are the variable names. Defaults to {}.
            function_dict (dict): dictionary of functions keys are the function names. Defaults to { "println": println, "print": println, "check": check, "wait": wait, "expect": expect_check, "input": get_input, "not": do_not, "equal": equal, }.
        """
        if function_dict == {}:
            function_dict = {
                "println": println,
                "print": println,
                "check": check,
                "wait": wait,
                "expect": expect_check,
                "input": get_input,
                "not": do_not,
                "equal": equal,
            }

        self.filename = filename
        self.gotoDict: typing.Dict[str, Union[int, None]] = {}
        self.variable_dict = variable_dict
        self.function_dict = function_dict
        self.lines: typing.List[str] = []
        self.bash: Union[None, pexpect.pty_spawn.spawn] = None
        self.history: typing.List[str] = []
        if filename != "":
            self.read_file(filename)

    def new_bash(self) -> None:
        """Generates a new bash terminal."""
        if self.bash is not None:
            self.bash.close()
        self.bash = pexpect.spawn('/bin/bash"')
        self.history = []

    def give_variables(self, variable_dict: typing.Dict[str, typing.Any] = {}) -> None:
        """Gives the Handler a new variable dictionary.

        Args:
            variable_dict (dict, optional): new variable dictionary. Defaults to {}.
        """
        self.variable_dict = variable_dict

    def call_func(self, line: str, i_line: int) -> typing.Any:
        """Funciton for calling a function executed internally.

        Raises:
            BaseException: if the functions isn't a real fuctions or an error occured

        # noqa: DAR401
        # noqa: DAR402

        Args:
            line (str): function line to be called
            i_line (int): Line where its called when not known -1

        Returns:
            Any: result of function when invalid a dictionary {"functincallfailed": -1}
        """
        # checkfunc
        i_f = line.find("(")
        # print(f"func_line = {line}")
        if i_f != -1:
            try:
                i_l = line.rfind(")")
                func_arg = line[i_f + 1 : i_l]
                func_arg = func_arg.strip()
                func_name = line[0:i_f]
                func_names: typing.List[typing.Any] = []

                # check func_arg has functions
                i_last = func_arg.find("(")
                if i_last != -1:
                    i_last = -1
                    i_begin = 0
                    i_b = 0

                    func_args = []
                    results = []
                    i_start = 0
                    # print(f"func_arg {func_arg}")

                    while i_b >= 0:
                        i_open = func_arg.find("(", i_last + 1)
                        i_close = func_arg.find(")", i_last + 1)
                        i_quotes = func_arg.find('"', i_last + 1)
                        i_comma = func_arg.find(",", i_last + 1)
                        if (
                            (i_open < i_close or i_close == -1)
                            and (i_open < i_quotes or i_quotes == -1)
                            and (i_open < i_comma or i_comma == -1)
                            and i_open != -1
                        ):
                            i_last = i_open
                            if i_b == 0:
                                i_begin = i_last + 1
                            i_b = i_b + 1
                            continue
                        elif (
                            (i_close < i_open or i_open == -1)
                            and (i_close < i_quotes or i_quotes == -1)
                            and (i_close < i_comma or i_comma == -1)
                            and i_close != -1
                        ):
                            i_b = i_b - 1
                            i_last = i_close
                            if i_b == 0:
                                func_args.append(func_arg[i_begin:i_close])
                                func_names.append(
                                    func_arg[i_start : i_begin - 1].strip()
                                )
                                i_comma_arg = func_arg.find(",", i_last + 1)
                                if i_comma_arg == -1:
                                    break
                                else:
                                    i_begin = i_comma_arg + 1
                                    i_last = i_comma_arg + 1
                            continue
                        elif (
                            (i_quotes < i_open or i_open == -1)
                            and (i_quotes < i_close or i_close == -1)
                            and (i_quotes < i_comma or i_comma == -1)
                            and i_quotes != -1
                        ):
                            i_quotes = func_arg.find('"', i_quotes + 1)
                            i_last = i_quotes
                        elif (
                            (i_comma < i_close or i_close == -1)
                            and (i_comma < i_open or i_open == -1)
                            and (i_comma < i_quotes or i_quotes == -1)
                            and i_comma != -1
                        ):
                            if i_b == 0:  # when in first loop
                                func_args.append(func_arg[i_start:i_comma].strip())
                                func_names.append(None)
                                i_start = i_comma + 1
                            i_last = i_comma

                        else:  # at the end of the search string
                            func_args.append(func_arg[i_start : len(func_arg)].strip())
                            func_names.append(None)
                            break
                    # print(f"func_names: {func_names}\nfunc_args:{func_args}")
                    for i_in_func in range(len(func_names)):
                        if func_names[i_in_func] is not None:
                            res = self.call_func(
                                func_names[i_in_func]
                                + "("
                                + func_args[i_in_func]
                                + ")",
                                i_line,
                            )
                        else:
                            res = func_args[i_in_func]
                        results.append(res)

                    # print(f"results: {results}")

                # print(f"should execute {func_name}(f{func_arg})")

                # print(f"check 1 funcname:{func_name}")
                # print(f"function_dict2: {self.function_dict}")
                # print(f"check Func: {self.function_dict[func_name]}")
                if func_names == []:
                    res = self.function_dict[func_name](self, func_arg)  # type: ignore
                else:
                    print(f"function_dict:[{func_name}](self,*{results})")
                    res = self.function_dict[func_name](self, *results)  # type: ignore
            except BaseException:
                # print(
                #    f"({i_line+1}) function {func_name}({func_arg}) not executed properly"
                # )
                # raise
                return {"functincallfailed": -1}
                # res = True
            return res

    def execute_file(self, filename: str = "") -> None:
        """Executed the given file when not given takes the set filename.

        Raises:
            BaseException: any line could not be executed

        Args:
            filename (str): filename to be used. Defaults to "".
        """
        if self.filename == "":
            self.read_file(filename)
        if self.bash is None:
            self.new_bash()

        i_line = 0
        i_depth = 0
        func_call_list: typing.List[str] = []
        conditional_terms = ["if", "else", "elif", "else", "while"]
        last_while = -1

        while i_line < len(self.lines):
            # check new incomming lines
            nw_lines = getlines(self.bash)
            if nw_lines is not None:
                for l1 in nw_lines:
                    print(f"(msh) {l1}")
            # if nw_lines is not None: print(f"func_call_list: {func_call_list}")

            if nw_lines is not None:
                self.history = [*self.history, *nw_lines]
            line: str = self.lines[i_line]
            line = line.replace("\n", "").replace("\r", "")

            # variable
            i_f = line.find("$(")
            while i_f != -1:
                i_l = line.find(")")
                var = line[i_f : i_l + 1]
                # print(f"line = {line}")
                try:
                    line = line.replace(var, self.variable_dict[var[2 : len(var) - 1]])
                except BaseException:
                    print(f"variable = {var} not in dict {self.variable_dict}")
                    raise
                i_f = line.find("$(")
            # lred = line.replace("\n", "").replace("\r", "")

            # print(f"(f) {func_call_list}")

            # empty line check
            if line.replace("\t", "").replace(" ", "") != "":
                # check same DepthLevel
                real_depth = 0
                for i in range(len(line)):
                    if line[i] == "\t":
                        real_depth = real_depth + 1
                    else:
                        break

                line = line[real_depth : len(line)]
                l_spl = line.split(" ")

                if l_spl[0][len(l_spl[0]) - 1] == ":":
                    i_line = i_line + 1
                    continue

                # check Depth
                if real_depth == i_depth:
                    # isnormal
                    # print(f'goforward: {line}, real_depth: {real_depth}')
                    print("", end="")
                elif real_depth < i_depth:
                    last_call = func_call_list.pop()
                    # print(f"last_call: {last_call}")
                    # print(f'l_spl = {l_spl[0]=="else"}')
                    if last_call == "if" or last_call == "elif":
                        i_l = i_line + 1
                        # print(f'l_spl = "{l_spl[0]}"')
                        # print(f'l_spl = {l_spl[0]=="else"}')
                        while l_spl[0] == "else" or l_spl[0] == "elif":
                            # print(f"l_spl = {l_spl[0]}")
                            # print(f"viewline: {self.lines[i_l]}")
                            while self.lines[i_l][real_depth] == "\t":
                                i_l = i_l + 1
                                # print(f"({i_line+1})skipped")
                            l_spl = self.lines[i_l][
                                real_depth : len(self.lines[i_l])
                            ].split(" ")
                        i_line = i_l
                        i_depth = real_depth
                        continue
                    elif last_call == "while":
                        # print(f"jump to line {last_while}")
                        i_line = last_while
                        i_depth = i_depth - 1
                        continue
                    elif last_call == "else":
                        i_depth = real_depth
                        continue
                    else:
                        print(f"({i_line+1}) - parsing error {last_call} not known")
                    # print(f"setDepth: {real_depth}")
                    i_depth = real_depth
                else:
                    print(f"({i_line+1}) - parsing error false tab usage")
                    print(f"real_depth: {real_depth}, i_depth: {i_depth}")
                    raise

                # checkif
                i_l = i_line
                if l_spl[0] in conditional_terms:
                    go_into = True
                    while l_spl[0] in conditional_terms:
                        if l_spl[0] == "if" or l_spl[0] == "elif":
                            if self.call_func(
                                line[len(l_spl[0]) + 1 : len(line)], i_line
                            ):
                                i_l = i_l + 1
                                break
                            else:
                                i_l = i_l + 1
                                # print(f"d - i_depth {i_depth} <{self.lines[i_l][i_depth]}>")
                                while self.lines[i_l][i_depth] == "\t":
                                    i_l = i_l + 1
                                    # print("d - "+self.lines[i_l])
                                l_spl = self.lines[i_l][
                                    i_depth : len(self.lines[i_l])
                                ].split(" ")
                                # print(l_spl)
                        elif l_spl[0] == "while":
                            if self.call_func(
                                line[len(l_spl[0]) + 1 : len(line)], i_line
                            ):
                                last_while = i_l
                                i_l = i_l + 1
                                break
                            else:
                                i_l = i_l + 1
                                # print(f"i_depth: {i_depth}")
                                while self.lines[i_l][i_depth] == "\t":
                                    i_l = i_l + 1
                                # print(f"jump to line {i_l+1}")
                                go_into = False
                                break
                        else:
                            i_l = i_line + 1
                            break
                    # if l_spl[0] == "if" or l_spl[0] == "elif" or l_spl[0] == "else":
                    # print("funcCall: "+l_spl[0].replace("\n","").replace("\r",""))
                    if go_into:
                        func_call_list.append(
                            l_spl[0].replace("\n", "").replace("\r", "")
                        )
                        i_depth = i_depth + 1
                    i_line = i_l
                    # print(f"enterred {l_spl[0]} with Depth: {i_depth}")
                    continue

                # check break
                if l_spl[0] == "break":
                    i_l = i_line + 1
                    rev_func_call_list = func_call_list[::-1]
                    r_index = len(rev_func_call_list) - rev_func_call_list.index(
                        "while"
                    )
                    while self.lines[i_l][r_index - 1] == "\t":
                        i_l = i_l + 1
                    i_line = i_l
                    continue

                print(f"(e) {line}")

                # checkfunc
                i_f = line.find("(")
                # print(line)
                if i_f != -1:
                    i_l = line.rfind(")")
                    func_arg = line[i_f + 1 : i_l]
                    func_name = line[0:i_f]

                    if func_name == "goto":
                        i_line = self.gotoDict[func_arg]  # type: ignore
                        i_depth = 0
                        func_call_list = []
                        continue
                    else:
                        # print(f"should execute {func_name}({func_arg})")
                        ret = self.call_func(line, i_line)
                        if str(ret.__class__) == "<class 'dict'>":
                            if "functincallfailed" in ret.keys():
                                self.bash.sendline(line)  # type: ignore
                        i_line = i_line + 1
                        continue

                # print(f"line = {line}")
                self.bash.sendline(line)  # type: ignore

            i_line = i_line + 1
        nw_lines = getlines(self.bash)
        # print(f"nw_lines: {nw_lines}")
        if nw_lines is not None:
            self.history = [*self.history, *nw_lines]
        # for line in self.history:
        #    print(line)

    def read_file(self, filename: str) -> None:
        """Read in file and setup for executing the script.

        Raises:
            BaseException: triggers if file was not Found

        # noqa: DAR401
        # noqa: DAR402

        Args:
            filename (str): name of file
        """
        if filename == "":
            raise
        else:
            print(f"(i) read in {filename}")

            try:
                doc = open(filename)
            except BaseException:
                print(f"(e) failed to open {filename}")

            # read in the goto files
            self.lines = doc.readlines()
            self.gotoDict["end"] = len(self.lines)

            for i_line in range(len(self.lines)):
                line = self.lines[i_line]
                line = line.replace("\n", "").replace("\r", "")
                l_sp = line.split(" ")
                # print(f"i_line = {i_line+1}")
                # print(f"line = {line}")
                # print(f"l_sp[0] = {l_sp[0]}")
                if len(l_sp[0]) == 0:
                    continue
                if l_sp[0][len(l_sp[0]) - 1] == ":":
                    self.gotoDict[l_sp[0][0 : len(l_sp[0]) - 1]] = i_line

            # print(self.gotoDict)


def check(
    bash_handler: MetaBashHandler, search_string: str, search_depth: int = 2
) -> bool:
    """Check function for MetaBashHandler checks whether string is found in gotten line.

    Args:
        bash_handler (MetaBashHandler): MetaBashHandler used
        search_string (str): search string
        search_depth (int): lines to search in

    Returns:
        bool: whether
    """
    # if str(search_string.__class__) != "<class 'str'>":
    # 	search_string = str(search_string)
    if search_string[0] == '"' and search_string[len(search_string) - 1] == '"':
        search_string = search_string[1 : len(search_string) - 1]
    # print(f"history: {bash_handler.history}")
    # print(f"l = \
    # {bash_handler.history[len(bash_handler.history)python import class before defining -1].find(search_string)}")
    for i_k in range(search_depth):
        # print(f"i_k = {i_k}")
        if len(bash_handler.history) - 1 - i_k >= 0:
            i = bash_handler.history[len(bash_handler.history) - 1 - i_k].find(
                search_string
            )
            # print(f"{bash_handler.history[len(bash_handler.history)-1-i_k]} - \
            # {search_string},\
            # {bash_handler.history[len(bash_handler.history)-1-i_k].__class__}\
            #  - {search_string.__class__}\n i = {i}")
            # print(f"len: {len(bash_handler.history)}, index: \
            # {len(bash_handler.history)-1-i}")
            if i != -1:
                # print(f"last: {bash_handler.history[\
                # len(bash_handler.history)-1-i_k]}")
                # print(
                #    f" {search_string} found in {bash_handler.history[len(bash_handler.history)-1-i_k]}"
                # )

                return True
            # print(
            #    f" {search_string} not found in {bash_handler.history[len(bash_handler.history)-i_k-1]}"
            # )
    return False


def do_not(bash_handler: MetaBashHandler, b: Union[bool, str]) -> bool:
    """Return inverse.

    Args:
        bash_handler (MetaBashHandler): MetaBashHandler (not used)
        b (bool or string): input to take inverse

    Returns:
        bool: invers
    """
    if b == "True":
        b = True
    elif b == "False":
        b = False
    return not b


def equal(
    bash_handler: MetaBashHandler,
    args: Union[typing.List[str], str],
    argf: Union[typing.List[str], str] = [],
) -> bool:
    """Check whether arguemtns arge equal.

    Args:
        bash_handler (MetaBashHandler): MetaBashHandler to be used
        args (list or str): first comparison or list of to arguments to be compared
        argf (list or str, optional): second comparispyon. Defaults to [].

    Returns:
        bool: returns whether equal
    """
    if argf == []:
        split_arg = args.split(",", 1)  # type: ignore

        if split_arg[1].find("(") != 0 and (
            split_arg[1][0] != '"' and split_arg[1][len(split_arg[1]) - 1] != '"'
        ):
            try:
                ret = bash_handler.call_func(split_arg[1], -1)
                cmp1 = str(ret)
            except BaseException:
                cmp1 = split_arg[1]
        else:
            cmp1 = split_arg[1]

        if split_arg[0].find("(") != 0 and (
            split_arg[0][0] != '"' and split_arg[0][len(split_arg[0]) - 1] != '"'
        ):
            try:
                ret = bash_handler.call_func(split_arg[0], -1)
                cmp0 = str(ret)
            except BaseException:
                cmp0 = split_arg[0]
        else:
            cmp1 = split_arg[0]

        if cmp0[0] == '"' and cmp0[len(cmp0) - 1] == '"' and len(cmp0) > 2:
            cmp0 = cmp0[1 : len(cmp0) - 1]

        if cmp1[0] == '"' and cmp1[len(cmp1) - 1] == '"' and len(cmp1) > 2:
            cmp1 = cmp1[1 : len(cmp1) - 1]

        # print(f"comparing {cmp0} and {cmp1}")

        return cmp0 == cmp1
    else:
        if args[0] == '"' and args[len(args) - 1] == '"' and len(args) > 2:
            args = args[1 : len(args) - 1]

        if argf[0] == '"' and argf[len(argf) - 1] == '"' and len(argf) > 2:
            argf = argf[1 : len(argf) - 1]
        return args == argf


def expect(bash_handler: MetaBashHandler, search_string_and_timeout: str) -> bool:
    """Check expected output comes with timeout.

    Args:
        bash_handler (MetaBashHandler): MetaBashHandler to use
        search_string_and_timeout (str): string of searchstring and timeout spareted by comma

    Returns:
        bool: whether expected strings found in timeout time
    """
    # print(f"Start expect without")
    spl = search_string_and_timeout.split(",")
    search_string = spl[0]
    if search_string[0] == '"' and search_string[len(search_string) - 1] == '"':
        search_string = search_string[1 : len(search_string) - 1]

    if check(bash_handler, search_string):
        return True
    # print(bash_handler.history)

    timeout = 5

    if len(spl) > 1:
        timeout = int(spl[1])
    try:
        bash_handler.bash.expect(search_string, timeout)  # type: ignore
    except BaseException:
        return False
    return True


def expect_check(
    bash_handler: MetaBashHandler,
    search_string: str,
    timeout: Union[str, int, float] = 5,
) -> typing.Any:
    """Check expected output comes with timeout keeping the gotten lines.

    Args:
        bash_handler (MetaBashHandler): MetaBashHandler to use
        search_string (str): string of searchstring and timeout spareted by comma
        timeout (str,int,float): seconds before getting timeout

    Returns:
        Any: whether expected strings found in timeout time
    """
    print("entered expect_check")

    if search_string[0] == '"' and search_string[len(search_string) - 1] == '"':
        search_string = search_string[1 : len(search_string) - 1]

    if check(bash_handler, search_string):
        return True

    timeout = float(timeout)

    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()

    time_dif = end_time - start_time
    # print(f"timedif: {time_dif.seconds},{time_dif.microseconds}")
    # print(time_dif)
    while time_dif.seconds + 1e-6 * time_dif.microseconds < timeout:
        # print(f"timedif: {time_dif.seconds+1e-6*time_dif.microseconds}")
        nw_lines = getlines(bash_handler.bash)
        if nw_lines is not None:
            for l1 in nw_lines:
                print(f"(msh) {l1}")

        if nw_lines is not None:
            bash_handler.history = [*bash_handler.history, *nw_lines]
            if check(bash_handler, search_string):
                return True
        time.sleep(0.01)
        time_dif = datetime.datetime.now() - start_time
    return False


def getlines(child: pexpect.pty_spawn.spawn) -> Union[typing.List[str], None]:
    """Get nonblocking lines.

    Args:
        child (pexpect.pty_spawn.spawn): terminal object

    Returns:
        list: string list of gotten lines
    """
    lines = []
    l_str = ""
    while True:
        try:
            character = child.read_nonblocking(timeout=0.1)
            l_str += character.decode(errors="ignore")
        except pexpect.exceptions.TIMEOUT:
            break

    lines = l_str.replace("\r", "").split("\n")
    if lines == [""]:
        return None
    return lines


def get_input(bash_handler: MetaBashHandler, text: str) -> str:
    """Get user input.

    Args:
        bash_handler (MetaBashHandler): MetaBashHandler to be used
        text (str): string to write when input is used

    Returns:
        str: return input string
    """
    if text == "":
        return input()
    else:
        return input(text)


def println(bash_handler: MetaBashHandler, text: str) -> bool:
    """Print on screen.

    Args:
        bash_handler (MetaBashHandler): MetaBashHandler to be used
        text (str): string to write

    Returns:
        bool: True always
    """
    print(text)
    return True


def wait(bash_handler: MetaBashHandler, timeout: typing.Any) -> None:
    """Wait function waits seconds.

    Args:
        bash_handler (MetaBashHandler): MetaBashHandler not used
        timeout (Any): something converts to float [s]
    """
    time.sleep(float(timeout))
