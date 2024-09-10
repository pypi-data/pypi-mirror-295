from pathlib import Path 
from time import time
from diskcache import Cache 
from hashlib import md5
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Static, ProgressBar
from textual.containers import Container, Center


class State:
    def __init__(self, input_stream, cache: str, collection_name: str) -> None:
        self.cache = Cache(cache)
        self._collection_name = collection_name
        self._input_stream = input_stream
        self._input_size = len(input_stream) if isinstance(input_stream, list) else None
        self._content_key = "content"
        self._current_example = None
        self._done = False
        self._position = 0

    def mk_hash(self, ex):
        string_repr = ex[self._content_key] + self._collection_name
        return md5(string_repr.encode()).hexdigest()

    def write_annot(self, label):
        if not self._done:
            self.cache[self.mk_hash(self.current_example)] = {
                **self.current_example, 
                'label': label,
                'collection': self._collection_name,
                'timestamp': int(time())
            }
            return self.next_example()
    
    @property
    def stream_size(self):
        return self._input_size

    def stream(self):
        for ex in self._input_stream:
            if self.mk_hash(ex) not in self.cache:
                yield ex
            self._position += 1
    
    @property
    def current_example(self):
        if self._current_example is None:
            try:
                self._current_example = next(self.stream())
            except StopIteration:
                self._current_example = {"content": "No more examples. All done!"}
                self._done = True
        return self._current_example
    
    def next_example(self):
        try:
            self._current_example = next(self.stream())
        except StopIteration:
            self._current_example = {"content": "No more examples. All done!"}
            self._done = True
        return self._current_example


def datatui(cache_name: str, input_stream: list, collection_name: str, pbar: bool = True, description=None):
    class DatatuiApp(App):
        ACTIVE_EFFECT_DURATION = 0.3
        CSS_PATH = Path(__file__).parent / "static" / "app.css"
        BINDINGS = [
            Binding(key="f", action="on_annot('yes')", description="Annotate yes."),
            Binding(key="j", action="on_annot('no')", description="Annotate no."),
            Binding(key="m", action="on_annot('maybe')", description="Annotate maybe."),
            Binding(key="space", action="on_annot('skip')", description="Skip the thing."),
        ]
        state = State(input_stream, cache_name, collection_name)

        def action_on_annot(self, answer: str) -> None:
            self._handle_annot_effect(answer=answer)
            self.state.write_annot(label=answer)
            self.update_view()
        
        def _example_text(self):
            content = self.state.current_example[self.state._content_key]
            if self.state._done:
                return "\n\n" + content + "\n\n"
            if description:
                return f"[bold black]{description}[/]\n\n" + content
            return content

        def update_view(self):
            self.query_one("#content").update(self._example_text())
            if pbar:
                self.query_one("#pbar").update(advance=1)
        
        def _handle_annot_effect(self, answer: str) -> None:
            self.query_one("#content").remove_class("base-card-border")
            class_to_add = "teal-card-border"
            if answer == "yes":
                class_to_add = "green-card-border"
            if answer == "no":
                class_to_add = "red-card-border"
            if answer == "maybe":
                class_to_add = "orange-card-border"
            self.query_one("#content").add_class(class_to_add)
            self.set_timer(
                self.ACTIVE_EFFECT_DURATION,
                lambda: self.query_one("#content").remove_class(class_to_add),
            )
            self.set_timer(
                self.ACTIVE_EFFECT_DURATION,
                lambda: self.query_one("#content").add_class("base-card-border"),
            )

        def compose(self) -> ComposeResult: 
            items = []
            if pbar:
                items.append(Center(ProgressBar(total=self.state.stream_size, show_eta=False, id="pbar")))
            items.append(Static(self._example_text(), id='content', classes='gray-card-border'))
            yield Container(*items, id='container')
            yield Footer()
            
        
        def on_mount(self) -> None:
            self.title = "Datatui - enriching data from the terminal"
            self.icon = None
            if pbar:
                self.query_one("#pbar").update(progress=self.state._position)
    
    DatatuiApp().run()

