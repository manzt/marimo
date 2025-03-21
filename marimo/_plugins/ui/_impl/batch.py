# Copyright 2024 Marimo. All rights reserved.
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Final,
    Optional,
)

from marimo._output.hypertext import Html
from marimo._output.rich_help import mddoc
from marimo._plugins.core.web_component import JSONType
from marimo._plugins.ui._core.ui_element import UIElement

if TYPE_CHECKING:
    from collections.abc import ItemsView, Iterator, ValuesView


# - Frontend type is a dict {label => value update}
# - Python type is a dict mapping label -> value
class _batch_base(UIElement[dict[str, JSONType], dict[str, object]]):
    """A batch of named UI elements represented by HTML text."""

    _name: Final[str] = "marimo-dict"

    def __init__(
        self,
        html: Html,
        elements: dict[str, UIElement[JSONType, object]],
        label: str = "",
        on_change: Optional[Callable[[dict[str, object]], None]] = None,
    ) -> None:
        self._elements = elements
        super().__init__(
            component_name=_batch_base._name,
            initial_value={
                key: e._initial_value_frontend
                for key, e in self._elements.items()
            },
            label=label,
            args={
                "element-ids": {
                    e._id: key for key, e in self._elements.items()
                },
            },
            slotted_html=html.text,
            on_change=on_change,
        )

        for key, element in self._elements.items():
            element._register_as_view(parent=self, key=key)

    @property
    def elements(self) -> dict[str, UIElement[JSONType, object]]:
        return self._elements

    def __len__(self) -> int:
        return len(self.elements)

    def __getitem__(self, key: str) -> UIElement[JSONType, object]:
        return self.elements[key]

    def __iter__(self) -> Iterator[str]:
        return self.elements.__iter__()

    def __reversed__(self) -> Iterator[str]:
        return self.elements.__reversed__()

    def __contains__(self, item: str) -> bool:
        return item in self.elements

    def get(self, key: str, default: Any | None = None) -> Any:
        """Get a UI element by key with an optional default value.

        Args:
            key (str): The key to look up in the batch.
            default (Any | None, optional): Value to return if key is not found. Defaults to None.

        Returns:
            Any: The UI element if found, otherwise the default value.
        """
        return self.elements.get(key, default)

    def items(self) -> ItemsView[str, UIElement[JSONType, object]]:
        """Return a view of the batch's items (key-value pairs).

        Returns:
            ItemsView[str, UIElement]: A view of the batch's (key, element) pairs.
        """
        return self.elements.items()

    def values(self) -> ValuesView[UIElement[JSONType, object]]:
        """Return a view of the batch's values (UI elements).

        Returns:
            ValuesView[UIElement]: A view of the batch's UI elements.
        """
        return self.elements.values()

    def _convert_value(self, value: dict[str, JSONType]) -> dict[str, object]:
        if self._initialized:
            for k, v in value.items():
                element = self._elements[k]
                # only call update if the value has changed
                if element._value_frontend != v:
                    element._update(v)
        return {
            key: wrapped_element._value
            for key, wrapped_element in self._elements.items()
        }

    def _on_update_completion(self) -> bool:
        any_updated = False
        for element in self._elements.values():
            any_updated |= element._on_update_completion()

        if any_updated:
            self._value = {
                key: wrapped_element._value
                for key, wrapped_element in self._elements.items()
            }
        return any_updated


@mddoc
class batch(_batch_base):
    """Convert an HTML object with templated text into a UI element.

    A `batch` is a UI element that wraps other UI elements, and is
    represented by custom HTML or markdown. You can create
    a `batch` by calling the `batch()` method on `Html` objects.

    Get the value of the wrapped UI elements using the `value` attribute
    of the batch.

    Examples:
        In the below example, `user_info` is a UI Element whose output is markdown
        and whose value is a dict with keys `'name'` and `'birthday'`
        (and values equal to the values of their corresponding elements).

        ```python3
        user_info = mo.md(
            '''
            - What's your name?: {name}
            - When were you born?: {birthday}
            '''
        ).batch(name=mo.ui.text(), birthday=mo.ui.date())
        ```

        To get the value of `name` and `birthday`, use:

        ```
        user_info.value
        ```

        You can also instantiate this class directly:

        ```python3
        markdown = mo.md(
            '''
            - What's your name?: {name}
            - When were you born?: {birthday}
            '''
        )
        batch = mo.ui.batch(
            markdown, {"name": mo.ui.text(), "birthday": mo.ui.date()}
        )
        ```

    Attributes:
        value (dict): A dict of the batched elements' values.
        elements (dict): A dict of the batched elements (clones of the originals).
        on_change (Optional[Callable]): Optional callback to run when this element's value changes.

    Args:
        html (Html): A templated Html object.
        elements (dict[str, UIElement]): The UI elements to interpolate into the HTML template.
        on_change (Optional[Callable[[Dict[str, object]], None]], optional): Optional callback
            to run when this element's value changes.
    """

    def __init__(
        self,
        html: Html,
        elements: dict[str, UIElement[Any, Any]],
        on_change: Optional[Callable[[dict[str, object]], None]] = None,
    ) -> None:
        self._html = html
        elements = {key: element._clone() for key, element in elements.items()}
        super().__init__(
            html=Html(self._html.text.format(**elements)),
            elements=elements,
            on_change=on_change,
        )

    def _clone(self) -> batch:
        return batch(html=self._html, elements=self.elements)
