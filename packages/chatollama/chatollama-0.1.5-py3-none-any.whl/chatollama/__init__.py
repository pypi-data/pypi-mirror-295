import typing
import re
import json
import threading
import ollama
import shutil


class ChatEngine:
    def __init__(self, model: str = "llama3.1:8b") -> None:
        self.model = model
        self.messages = ChatMessages()
        self.thread = None
        self.stop_event = threading.Event()
        self.response = ""
        self.tool_calls = []
        self.callback = self._default_stream_callback
        self.tool_callback = self._default_tool_callback
        self.append_response_to_messages = True
        self.name = "AI"
        self.tools:list[dict] = []
        self.use_tools = False

    def warmup(self):
        messages = ChatMessages()
        messages.system("Respond with the word 'Ready'")
        messages.user("Respond with the word 'Ready'")
        response = ollama.chat(
            model=self.model, messages=messages.get_logs(), stream=False, keep_alive="5m")
        print(response["message"]["content"])

    def chat(self):
        self.stop_event.clear()
        self.thread = threading.Thread(
            target=self._response_handler, daemon=True)
        self.thread.start()

    def _response_handler(self):
        try:
            if self.use_tools:
                response_stream = ollama.chat(
                    model=self.model, messages=self.messages.get_logs(), stream=False, keep_alive="5m", tools=self.tools)
                self.handle_tool_response(response_stream)
            else:
                response_stream = ollama.chat(
                    model=self.model, messages=self.messages.get_logs(), stream=True, keep_alive="5m")
                self.handle_stream(response_stream)
        except Exception as e:
            print(f"Error: {e}")
            self.stop_event.set()

    def _default_stream_callback(self, mode: int, delta: str, text: str):
        if mode == 0:
            print(f"[{self.name}]: ", flush=True)
        elif mode == 1:
            print(delta, end="", flush=True)
        elif mode == 2:
            print("", flush=True)

    def _default_tool_callback(self, tool_response: list[dict]):
        print(tool_response, flush=True)

    def handle_stream(self, stream):
        self.response = ""
        self.callback(0, "", self.response)
        for chunk in stream:
            if self.stop_event.is_set():
                break
            delta = chunk['message']['content']
            self.response += delta
            self.callback(1, delta, self.response)
        if self.append_response_to_messages:
            self.messages.assistant(self.response)
        self.stop_event.set()
        self.callback(2, "", self.response)

    def handle_tool_response(self, response):
        self.response = response["message"]["content"]
        self.tool_calls = response["message"].get("tool_calls", [])
        self.tool_callback(self.tool_calls)
        self.stop_event.set()

    def wait(self):
        if self.thread:
            self.thread.join()


class ChatMessages:
    class ChatMessageBranch:
        def __init__(self, message: typing.Dict[str, str], master: 'ChatMessages') -> None:
            self.master = master
            self.index = 0
            self.branches: typing.List[typing.Dict[str, typing.Union[typing.Dict, 'ChatMessages.ChatMessageBranch']]] = [{
                "message": message,
                "branch_from": self,
                "branch": None,
            }]

        def add(self, message: typing.Dict[str, str]) -> 'ChatMessages.ChatMessageBranch':
            """
            Add a new message branch to the current branch.
            """
            new_branch = ChatMessages.ChatMessageBranch(message, self.master)
            self.branches[self.index]["branch"] = new_branch
            self.master.current = new_branch
            return new_branch

        def variant(self, message: typing.Dict[str, str]) -> typing.Dict:
            """
            Create a variant branch at the current branch level.
            """
            branch = {
                "message": message,
                "branch_from": self,
                "branch": None,
            }
            self.branches.append(branch)
            self.index = len(self.branches) - 1
            self.master.current = self
            return branch

        def prev(self) -> bool:
            """
            Move to the previous branch variant if available.
            """
            if self.index > 0:
                self.index -= 1
                self.master.current = self
                return True
            return False

        def next(self) -> bool:
            """
            Move to the next branch variant if available.
            """
            if self.index < len(self.branches) - 1:
                self.index += 1
                self.master.current = self
                return True
            return False

        @property
        def current(self) -> typing.Dict:
            """
            Get the current branch.
            """
            return self.branches[self.index]

    def __init__(self) -> None:
        self.root: typing.Optional[ChatMessages.ChatMessageBranch] = None
        self.current: typing.Optional[ChatMessages.ChatMessageBranch] = None

    def _message(self, role: str, content: str) -> 'ChatMessages.ChatMessageBranch':
        """
        Creates a message with the given role and content and adds it to the chat tree.
        """
        message = {"role": role, "content": content}
        if not self.current:
            self.root = ChatMessages.ChatMessageBranch(message, self)
            self.current = self.root
        else:
            self.current = self.current.add(message)
        return self.current

    def user(self, text: str) -> 'ChatMessages.ChatMessageBranch':
        return self._message("user", text)

    def assistant(self, text: str) -> 'ChatMessages.ChatMessageBranch':
        return self._message("assistant", text)

    def system(self, text: str) -> 'ChatMessages.ChatMessageBranch':
        return self._message("system", text)

    def get_logs(self) -> typing.List[typing.Dict[str, str]]:
        """
        Retrieves the linear message log from the root to the current branch.
        """
        messages = []
        branch = self.root
        while branch:
            message_branch = branch.branches[branch.index]
            messages.append(message_branch["message"])
            branch = message_branch["branch"]
        return messages

    def get_logs_with_branches(self) -> typing.List[typing.Dict[str, typing.Union[typing.Dict[str, str], typing.List]]]:
        """
        Retrieves the entire chat log with branches in a nested structure.
        """
        def traverse(branch: typing.Optional[ChatMessages.ChatMessageBranch]) -> typing.List[typing.Dict[str, typing.Union[typing.Dict, typing.List]]]:
            if not branch:
                return []
            messages = []
            for b in branch.branches:
                messages.append({
                    "message": b["message"],
                    "branch": traverse(b["branch"]) if b["branch"] else None,
                })
            return messages

        return traverse(self.root)

    def save(self, file_path: str) -> None:
        """
        Saves the chat tree to a file in JSON format.
        """
        logs = self.get_logs_with_branches()
        with open(file_path, 'w') as file:
            json.dump(logs, file)

    def load(self, file_path: str) -> None:
        """
        Loads the chat tree from a JSON file.
        """
        def reconstruct(branch_logs: typing.List[typing.Dict], master: 'ChatMessages') -> 'ChatMessages.ChatMessageBranch':
            if not branch_logs:
                return None
            root_message = branch_logs[0]["message"]
            root_branch = ChatMessages.ChatMessageBranch(root_message, master)
            for log in branch_logs[1:]:
                if log["branch"]:
                    child_branch = reconstruct(log["branch"], master)
                    root_branch.add(child_branch.branches[0]["message"])
            return root_branch

        with open(file_path, 'r') as file:
            logs = json.load(file)

        if logs:
            self.root = reconstruct(logs, self)
            self.current = self.root

    def print(self, include_system: bool = False):
        # Get terminal size to determine max width
        terminal_width = shutil.get_terminal_size().columns
        logs = self.get_logs()
        longest = 0
        count = len(logs)

        # Filter logs based on the include_system flag
        filtered_logs = [
            log for log in logs if include_system or log["role"] != "system"
        ]
        count = len(filtered_logs)

        print(f"[Message Logs] ({count})")

        # Calculate the longest line after wrapping to the terminal width
        wrapped_logs = []
        for log in filtered_logs:
            prepped_content = log["content"]
            wrapped_content = []

            for line in prepped_content.split("\n"):
                # Wrap line to fit within the terminal width
                while len(line) > terminal_width - 12:  # 12 is for padding in print layout
                    wrapped_content.append(line[:terminal_width - 12])
                    line = line[terminal_width - 12:]
                wrapped_content.append(line)
                longest = max(longest, max(len(l) for l in wrapped_content))
            
            wrapped_logs.append((log["role"], wrapped_content))

        # Set the minimum length for the underscores, to ensure proper formatting
        underscore_length = max(longest + 9, 50)

        # Print each wrapped log with dynamic underscore length
        for role, wrapped_content in wrapped_logs:
            formatted_lines = ["  |-      " + line for line in wrapped_content]
            formatted_content = "\n".join(formatted_lines)

            print(f"""   {"_" * underscore_length}
  |-
  |-      -----------=[{role}]=------------
  |-
{formatted_content}
  |-
   {"_" * underscore_length}""")


def handle_tools(tool_calls):
    for tool in tool_calls:
        fn = tool.get("function", None)
        if fn is None:
            continue
        fn_name = fn.get("name", None)
        parameters = fn.get("arguments", None)
        if fn_name is None:
            continue
        if parameters is None:
            continue

        # Dynamically check if function exists and call it
        func = globals().get(fn_name) or locals().get(fn_name)
        if callable(func):
            try:
                func(**parameters)
            except:
                pass
        else:
            print(f"Function {fn_name} not found")
            pass


def preprocess_json_string(json_string: str) -> str:
    json_string = re.sub(r'[^\x20-\x7E]', '', json_string.strip())
    json_string = re.sub(r',(\s*[\]}])', r'\1', json_string)

    open_brackets, open_braces, cleaned_string = 0, 0, ""
    for char in json_string:
        if char == '[':
            open_brackets += 1
        elif char == ']':
            open_brackets -= 1
        elif char == '{':
            open_braces += 1
        elif char == '}':
            open_braces -= 1
        if open_brackets >= 0 and open_braces >= 0:
            cleaned_string += char

    return cleaned_string + ']' * open_brackets + '}' * open_braces


def replace_single_quotes(json_like_string: str) -> str:
    def find_left_non_space_char(s, index):
        while index >= 0 and s[index].isspace():
            index -= 1
        return index

    def find_right_non_space_char(s, index):
        while index < len(s) and s[index].isspace():
            index += 1
        return index

    result = []
    length = len(json_like_string)
    i = 0
    valid_chars = {':', '{', '}', '[', ']', ',', '(', ')'}

    while i < length:
        if json_like_string[i] == "'":
            left_index = find_left_non_space_char(json_like_string, i - 1)
            if left_index >= 0 and json_like_string[left_index] in valid_chars:
                j = i + 1
                while j < length:
                    if json_like_string[j] == "'":
                        right_index = find_right_non_space_char(
                            json_like_string, j + 1)
                        if right_index < length and json_like_string[right_index] in valid_chars:
                            json_like_string = json_like_string[:i] + '"' + \
                                json_like_string[i+1:j] + \
                                '"' + json_like_string[j+1:]
                            length = len(json_like_string)
                            i = j
                            break
                    j += 1
        i += 1

    return json_like_string
