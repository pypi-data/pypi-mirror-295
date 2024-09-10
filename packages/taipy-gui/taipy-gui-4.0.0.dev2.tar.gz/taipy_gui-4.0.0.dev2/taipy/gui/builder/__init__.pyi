from typing import Union

from ._element import _Block, _Control, _Element
from ._element import content as content
from ._element import html as html
from .page import Page as Page

class text(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value: any = "",
        *,
        raw: bool = False,
        mode: str,
        format: str,
        width: Union[str, int] = None,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a text element.\n\nParameters\n----------\n\nvalue (dynamic)\n  The value displayed as text by this control.\n\nraw\n  If set to True, the component renders as an HTML \<span\> element without any default style.\n\nmode\n  Define the way the text is processed:\n  * "raw": synonym for setting the \*raw\* property to True\n  * "pre": keeps spaces and new lines\n  * "markdown" or "md": basic support for Markdown.\n  \n\nformat\n  The format to apply to the value.\n\nwidth\n  The width of the element.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class button(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        label: Union[str, Icon] = "",
        *,
        on_action: Callable,
        width: Union[str, int] = None,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a button element.\n\nParameters\n----------\n\nlabel (dynamic)\n  The label displayed in the button.\n\non_action\n  The name of a function that is triggered when the button is pressed.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the button it it has one.\n  * payload (dict): a dictionary that contains the key "action" set to the name of the action that triggered this callback.\n  \n\nwidth\n  The width of the button element.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class input(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value: any = None,
        *,
        password: bool = False,
        label: str = None,
        multiline: bool = False,
        lines_shown: int = 5,
        type: str = "text",
        change_delay: int,
        on_action: Callable,
        action_keys: str = "Enter",
        width: Union[str, int] = None,
        on_change: Callable,
        propagate: bool,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates an input element.\n\nParameters\n----------\n\nvalue (dynamic)\n  The value represented by this control.\n\npassword\n  If True, the text is obscured: all input characters are displayed as an asterisk ('\*').\n\nlabel\n  The label associated with the input.\n\nmultiline\n  If True, the text is presented as a multi line input.\n\nlines_shown\n  The number of lines shown in the input control, when multiline is True.\n\ntype\n  TODO: The type of input: text, tel, email ... as defined in HTML standards https://developer.mozilla.org/en\-US/docs/Web/HTML/Element/input\#input\_types \n\nchange_delay\n  Minimum time between triggering two calls to the on\_change callback.  \n  The default value is defined at the application configuration level by the **change\_delay** configuration option. if None, the delay is set to 300 ms.  \n  If set to \-1, the input change is triggered only when the user presses the Enter key.\n\non_action\n  Name of a function that is triggered when a specific key is pressed.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the control if it has one.\n  * payload (dict): the details on this callback's invocation.  \n  \n  This dictionary has the following keys:\n  	+ action: the name of the action that triggered this callback.\n  	+ args (list):\n  		- key name\n  		- variable name\n  		- current value\n  \n\naction_keys\n  Semicolon (';')\-separated list of supported key names.  \n  Authorized values are Enter, Escape, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12\.\n\nwidth\n  The width of the element.\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\npropagate\n  Allows the control's main value to be automatically propagated.  \n  The default value is defined at the application configuration level.  \n  If True, any change to the control's value is immediately reflected in the bound application variable.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class number(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value: any,
        *,
        label: str = None,
        step: Union[int, float] = 1,
        step_multiplier: Union[int, float] = 10,
        min: Union[int, float],
        max: Union[int, float],
        change_delay: int,
        on_action: Callable,
        action_keys: str = "Enter",
        width: Union[str, int] = None,
        on_change: Callable,
        propagate: bool,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a number element.\n\nParameters\n----------\n\nvalue (dynamic)\n  The numerical value represented by this control.\n\nlabel\n  The label associated with the input.\n\nstep (dynamic)\n  The amount by which the value is incremented or decremented when the user clicks one of the arrow buttons.\n\nstep_multiplier (dynamic)\n  A factor that multiplies *step* when the user presses the Shift key while clicking one of the arrow buttons.\n\nmin (dynamic)\n  The minimum value to accept for this input.\n\nmax (dynamic)\n  The maximum value to accept for this input.\n\nchange_delay\n  Minimum time between triggering two calls to the on\_change callback.  \n  The default value is defined at the application configuration level by the **change\_delay** configuration option. if None, the delay is set to 300 ms.  \n  If set to \-1, the input change is triggered only when the user presses the Enter key.\n\non_action\n  Name of a function that is triggered when a specific key is pressed.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the control if it has one.\n  * payload (dict): the details on this callback's invocation.  \n  \n  This dictionary has the following keys:\n  	+ action: the name of the action that triggered this callback.\n  	+ args (list):\n  		- key name\n  		- variable name\n  		- current value\n  \n\naction_keys\n  Semicolon (';')\-separated list of supported key names.  \n  Authorized values are Enter, Escape, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12\.\n\nwidth\n  The width of the element.\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\npropagate\n  Allows the control's main value to be automatically propagated.  \n  The default value is defined at the application configuration level.  \n  If True, any change to the control's value is immediately reflected in the bound application variable.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class slider(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value: Union[int, float, str, list[int], list[float], list[str]],
        *,
        min: Union[int, float] = 0,
        max: Union[int, float] = 100,
        step: Union[int, float] = 1,
        text_anchor: str = "bottom",
        labels: Union[bool, dict[str, str]],
        continuous: bool = True,
        change_delay: int,
        width: str = "300px",
        height: str,
        orientation: str = "horizontal",
        on_change: Callable,
        lov: dict[str, any],
        adapter,
        type: str,
        value_by_id: bool = False,
        propagate: bool,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a slider element.\n\nParameters\n----------\n\nvalue (dynamic)\n  The value that is set for this slider.  \n  If this slider is based on a *lov* then this property can be set to the lov element.  \n  This value can also hold an array of numbers to indicate that the slider reflects a range (within the \[*min*,*max*] domain) defined by several knobs that the user can set independently.  \n  If this slider is based on a *lov* then this property can be set to an array of lov elements. The slider is then represented with several knobs, one for each lov value.\n\nmin\n  The minimum value.  \n  This is ignored when *lov* is defined.\n\nmax\n  The maximum value.  \n  This is ignored when *lov* is defined.\n\nstep\n  The step value, which is the gap between two consecutive values the slider set. It is a good practice to have (*max*\-*min*) being divisible by *step*.  \n  This property is ignored when *lov* is defined.\n\ntext_anchor\n  When the *lov* property is used, this property indicates the location of the label.  \n  Possible values are:\n  * "bottom"\n  * "top"\n  * "left"\n  * "right"\n  * "none" (no label is displayed)\n  \n\nlabels\n  The labels for specific points of the slider.  \n  If set to True, this slider uses the labels of the *lov* if there are any.  \n  If set to a dictionary, the slider uses the dictionary keys as a *lov* key or index, and the associated value as the label.\n\ncontinuous\n  If set to False, the control emits an on\_change notification only when the mouse button is released, otherwise notifications are emitted during the cursor movements.  \n  If *lov* is defined, the default value is False.\n\nchange_delay\n  Minimum time between triggering two on\_change callbacks.  \n  The default value is defined at the application configuration level by the **change\_delay** configuration option. if None or 0, there's no delay.\n\nwidth\n  The width of this slider, in CSS units.\n\nheight\n  The height of this slider, in CSS units.  \n  It defaults to the value of *width* when using the vertical orientation.\n\norientation\n  The orientation of this slider.  \n  Valid values are "horizontal" or "vertical".\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\nlov\n  The list of values. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/slider/../../../../../userman/gui/binding/#list-of-values) for details.\n\nadapter\n  The function that transforms an element of *lov* into a *tuple(id:str, label:Union\[str,Icon])*.\n\ntype\n  Must be specified if *lov* contains a non\-specific type of data (ex: dict).  \n  *value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type.\n\nvalue_by_id\n  If False, the selection value (in *value*) is the selected element in *lov*. If set to True, then *value* is set to the id of the selected element in *lov*.\n\npropagate\n  Allows the control's main value to be automatically propagated.  \n  The default value is defined at the application configuration level.  \n  If True, any change to the control's value is immediately reflected in the bound application variable.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class toggle(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value: any,
        *,
        theme: bool = False,
        allow_unselect: bool = False,
        unselected_value: any = None,
        mode: str,
        label: str,
        width: Union[str, int] = None,
        on_change: Callable,
        lov: dict[str, any],
        adapter,
        type: str,
        value_by_id: bool = False,
        propagate: bool,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a toggle element.\n\nParameters\n----------\n\nvalue (dynamic)\n  Bound to the selection value.\n\ntheme\n  If set, this toggle control acts as a way to set the application Theme (dark or light).\n\nallow_unselect\n  If set, this allows de\-selection and the value is set to unselected\_value.\n\nunselected_value\n  Value assigned to *value* when no item is selected.\n\nmode\n  Define the way the toggle is displayed:\n  * "theme": synonym for setting the \*theme\* property to True\n  \n\nlabel\n  The label associated with the toggle.\n\nwidth\n  The width of the element.\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\nlov\n  The list of values. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/toggle/../../../../../userman/gui/binding/#list-of-values) for details.\n\nadapter\n  The function that transforms an element of *lov* into a *tuple(id:str, label:Union\[str,Icon])*.\n\ntype\n  Must be specified if *lov* contains a non\-specific type of data (ex: dict).  \n  *value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type.\n\nvalue_by_id\n  If False, the selection value (in *value*) is the selected element in *lov*. If set to True, then *value* is set to the id of the selected element in *lov*.\n\npropagate\n  Allows the control's main value to be automatically propagated.  \n  The default value is defined at the application configuration level.  \n  If True, any change to the control's value is immediately reflected in the bound application variable.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class date(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        date: datetime,
        *,
        with_time: bool = False,
        format: str,
        editable: bool = True,
        label: str,
        min: datetime,
        max: datetime,
        width: Union[str, int] = None,
        on_change: Callable,
        propagate: bool,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a date element.\n\nParameters\n----------\n\ndate (dynamic)\n  The date that this control represents and can modify.  \n  It is typically bound to a `datetime` object.\n\nwith_time\n  Whether or not to show the time part of the date.\n\nformat\n  The format to apply to the value.\n\neditable (dynamic)\n  Shows the date as a formatted string if not editable.\n\nlabel\n  The label associated with the input.\n\nmin (dynamic)\n  The minimum date to accept for this input.\n\nmax (dynamic)\n  The maximum date to accept for this input.\n\nwidth\n  The width of the date element.\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\npropagate\n  Allows the control's main value to be automatically propagated.  \n  The default value is defined at the application configuration level.  \n  If True, any change to the control's value is immediately reflected in the bound application variable.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class date_range(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        dates: list(datetime),
        *,
        with_time: bool = False,
        format: str,
        editable: bool = True,
        label_start: str,
        label_end: str,
        width: Union[str, int] = None,
        on_change: Callable,
        propagate: bool,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a date_range element.\n\nParameters\n----------\n\ndates (dynamic)\n  The dates that this control represents and can modify.  \n  It is typically bound to a list of two `datetime` object.\n\nwith_time\n  Whether or not to show the time part of the date.\n\nformat\n  The format to apply to the value.\n\neditable (dynamic)\n  Shows the date as a formatted string if not editable.\n\nlabel_start\n  The label associated with the first input.\n\nlabel_end\n  The label associated with the second input.\n\nwidth\n  The width of the date\_range element.\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\npropagate\n  Allows the control's main value to be automatically propagated.  \n  The default value is defined at the application configuration level.  \n  If True, any change to the control's value is immediately reflected in the bound application variable.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class chart(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        data: any,
        *,
        type: str,
        mode: str,
        x: str,
        y: str,
        z: str,
        lon: str,
        lat: str,
        r: str,
        theta: str,
        high: str,
        low: str,
        open: str,
        close: str,
        measure: str,
        locations: str,
        values: str,
        labels: str,
        parents: str,
        text: str,
        base: str,
        title: str,
        render: bool = True,
        on_range_change: Callable,
        columns: Union[str, list[str], dict[str, dict[str, str]]],
        label: str,
        name: str,
        selected: Union[list[int], str],
        color: str,
        selected_color: str,
        marker: dict[str, any],
        line: Union[str, dict[str, any]],
        selected_marker: dict[str, any],
        layout: dict[str, any],
        plot_config: dict[str, any],
        options: dict[str, any],
        orientation: str,
        text_anchor: str,
        xaxis: str,
        yaxis: str,
        width: Union[str, int, float] = "100%",
        height: Union[str, int, float],
        template: dict,
        decimator: taipy.gui.data.Decimator,
        rebuild: bool = False,
        figure: plotly.graph_objects.Figure,
        on_click: Callable,
        on_change: Callable,
        propagate: bool,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a chart element.\n\nParameters\n----------\n\ndata (dynamic)\n  The data object bound to this chart control.  \n  See the section on the [*data* property](#the-data-property) below for details.\n\ntype (indexed)\n  Chart type.  \n  See the Plotly [chart type](https://plotly.com/javascript/reference/) documentation for details.\n\nmode (indexed)\n  Chart mode.  \n  See the Plotly [chart mode](https://plotly.com/javascript/reference/scatter/#scatter-mode) documentation for details.\n\nx (indexed)\n  Column name for the *x* axis.\n\ny (indexed)\n  Column name for the *y* axis.\n\nz (indexed)\n  Column name for the *z* axis.\n\nlon (indexed)\n  Column name for the *longitude* value, for 'scattergeo' charts. See [Plotly Map traces](https://plotly.com/javascript/reference/scattergeo/#scattergeo-lon).\n\nlat (indexed)\n  Column name for the *latitude* value, for 'scattergeo' charts. See [Plotly Map traces](https://plotly.com/javascript/reference/scattergeo/#scattergeo-lat).\n\nr (indexed)\n  Column name for the *r* value, for 'scatterpolar' charts. See [Plotly Polar charts](https://plotly.com/javascript/polar-chart/).\n\ntheta (indexed)\n  Column name for the *theta* value, for 'scatterpolar' charts. See [Plotly Polar charts](https://plotly.com/javascript/polar-chart/).\n\nhigh (indexed)\n  Column name for the *high* value, for 'candlestick' charts. See [Plotly Candlestick charts](https://plotly.com/javascript/reference/candlestick/#candlestick-high).\n\nlow (indexed)\n  Column name for the *low* value, for 'candlestick' charts. See [Ploty Candlestick charts](https://plotly.com/javascript/reference/candlestick/#candlestick-low).\n\nopen (indexed)\n  Column name for the *open* value, for 'candlestick' charts. See [Plotly Candlestick charts](https://plotly.com/javascript/reference/candlestick/#candlestick-open).\n\nclose (indexed)\n  Column name for the *close* value, for 'candlestick' charts. See [Plotly Candlestick charts](https://plotly.com/javascript/reference/candlestick/#candlestick-close).\n\nmeasure (indexed)\n  Column name for the *measure* value, for 'waterfall' charts. See [Plotly Waterfall charts](https://plotly.com/javascript/reference/waterfall/#waterfall-measure).\n\nlocations (indexed)\n  Column name for the *locations* value. See [Plotly Choropleth maps](https://plotly.com/javascript/choropleth-maps/).\n\nvalues (indexed)\n  Column name for the *values* value. See [Plotly Pie charts](https://plotly.com/javascript/reference/pie/#pie-values) or [Plotly Funnel Area charts](https://plotly.com/javascript/reference/funnelarea/#funnelarea-values).\n\nlabels (indexed)\n  Column name for the *labels* value. See [Plotly Pie charts](https://plotly.com/javascript/reference/pie/#pie-labels).\n\nparents (indexed)\n  Column name for the *parents* value. See [Plotly Treemap charts](https://plotly.com/javascript/reference/treemap/#treemap-parents).\n\ntext (indexed)\n  Column name for the text associated to the point for the indicated trace.  \n  This is meaningful only when *mode* has the *text* option.\n\nbase (indexed)\n  Column name for the *base* value. Used in bar charts only.  \n  See the Plotly [bar chart base](https://plotly.com/javascript/reference/bar/#bar-base) documentation for details."\n\ntitle\n  The title of this chart control.\n\nrender (dynamic)\n  If True, this chart is visible on the page.\n\non_range_change\n  The callback function that is invoked when the visible part of the x axis changes.  \n  The function receives three parameters:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the chart control if it has one.\n  * payload (dict\[str, any]): the full details on this callback's invocation, as emitted by [Plotly](https://plotly.com/javascript/plotlyjs-events/#update-data).\n  \n\ncolumns\n  The list of column names\n  * str: ;\-separated list of column names\n  * list\[str]: list of names\n  * dict: {"column\_name": {format: "format", index: 1}} if index is specified, it represents the display order of the columns.\n  If not, the list order defines the index\n  \n\nlabel (indexed)\n  The label for the indicated trace.  \n  This is used when the mouse hovers over a trace.\n\nname (indexed)\n  The name of the indicated trace.\n\nselected (dynamic) (indexed)\n  The list of the selected point indices .\n\ncolor (indexed)\n  The color of the indicated trace (or a column name for scattered).\n\nselected_color (indexed)\n  The color of the selected points for the indicated trace.\n\nmarker (indexed)\n  The type of markers used for the indicated trace.  \n  See [marker](https://plotly.com/javascript/reference/scatter/#scatter-marker) for details.  \n  Color, opacity, size and symbol can be column name.\n\nline (indexed)\n  The configuration of the line used for the indicated trace.  \n  See [line](https://plotly.com/javascript/reference/scatter/#scatter-line) for details.  \n  If the value is a string, it must be a dash type or pattern (see [dash style of lines](https://plotly.com/python/reference/scatter/#scatter-line-dash) for details).\n\nselected_marker (indexed)\n  The type of markers used for selected points in the indicated trace.  \n  See [selected marker for details.](https://plotly.com/javascript/reference/scatter/#scatter-selected-marker)\n\nlayout (dynamic)\n  The *plotly.js* compatible [layout object](https://plotly.com/javascript/reference/layout/).\n\nplot_config\n  The *plotly.js* compatible  [configuration options object](https://plotly.com/javascript/configuration-options/).\n\noptions (indexed)\n  The *plotly.js* compatible [data object where dynamic data will be overridden.](https://plotly.com/javascript/reference/).\n\norientation (indexed)\n  The orientation of the indicated trace.\n\ntext_anchor (indexed)\n  Position of the text relative to the point.  \n  Valid values are: *top*, *bottom*, *left*, and *right*.\n\nxaxis (indexed)\n  The *x* axis identifier for the indicated trace.\n\nyaxis (indexed)\n  The *y* axis identifier for the indicated trace.\n\nwidth\n  The width of this chart, in CSS units.\n\nheight\n  The height of this chart, in CSS units.\n\ntemplate\n  The Plotly [layout template](https://plotly.com/javascript/layout-template/).\n\ndecimator (indexed)\n  A decimator instance for the indicated trace that reduces the volume of the data being sent back and forth.  \n  If defined as *indexed*, it impacts only the indicated trace; if not, it applies to the first trace only.\n\nrebuild (dynamic)\n  Allows dynamic config refresh if set to True.\n\nfigure (dynamic)\n  A figure as produced by plotly.\n\non_click\n  The callback that is invoked when the user clicks in the chart background.  \n  The function receives three parameters:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the chart control if it has one.\n  * payload (dict\[str, any]): a dictionary containing the *x* and *y* coordinates of the click **or** *latitude* and *longitude* in the case of a map. This feature relies on non\-public Plotly structured information.\n  \n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\npropagate\n  Allows the control's main value to be automatically propagated.  \n  The default value is defined at the application configuration level.  \n  If True, any change to the control's value is immediately reflected in the bound application variable.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class table(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        data: any,
        *,
        page_size: int = 100,
        allow_all_rows: bool = False,
        show_all: bool = False,
        auto_loading: bool = False,
        selected: Union[list[int], str],
        page_size_options: Union[list[int], str] = (50, 100, 500),
        columns: Union[str, list[str], dict[str, dict[str, Union[str, int]]]],
        date_format: str = "MM/dd/yyyy",
        number_format: str,
        style: str,
        tooltip: str,
        width: str = "100%",
        height: str = "80vh",
        filter: bool = False,
        nan_value: str = "",
        editable: bool = False,
        on_edit: Callable,
        on_delete: Callable,
        on_add: Callable,
        on_action: Callable,
        size: str = "small",
        rebuild: bool = False,
        downloadable: bool,
        on_compare: Callable,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a table element.\n\nParameters\n----------\n\ndata (dynamic)\n  The data to be represented in this table. This property can be indexed to define other data for comparison.\n\npage_size\n  For a paginated table, the number of visible rows.\n\nallow_all_rows\n  For a paginated table, adds an option to show all the rows.\n\nshow_all\n  For a paginated table, show all the rows.\n\nauto_loading\n  If True, the data will be loaded on demand.\n\nselected (dynamic)\n  The list of the indices of the rows to be displayed as selected.\n\npage_size_options\n  The list of available page sizes that users can choose from.\n\ncolumns\n  The list of the column names to display.\n  * str: Semicolon (';')\-separated list of column names.\n  * list\[str]: The list of column names.\n  * dict: A dictionary with entries matching: {"col name": {format: "format", index: 1}}.  \n  \n  if *index* is specified, it represents the display order of the columns.\n  If *index* is not specified, the list order defines the index.  \n  \n  If *format* is specified, it is used for numbers or dates.\n  \n\ndate_format\n  The date format used for all date columns when the format is not specifically defined.\n\nnumber_format\n  The number format used for all number columns when the format is not specifically defined.\n\nstyle\n  Allows the styling of table lines.  \n  See [below](#dynamic-styling) for details.\n\ntooltip\n  The name of the function that must return a tooltip text for a cell.  \n  See [below](#cell-tooltips) for details.\n\nwidth\n  The width of this table control, in CSS units.\n\nheight\n  The height of this table control, in CSS units.\n\nfilter\n  Indicates, if True, that all columns can be filtered.\n\nnan_value\n  The replacement text for NaN (not\-a\-number) values.\n\neditable (dynamic)\n  Indicates, if True, that all columns can be edited.\n\non_edit\n  TODO: Default implementation and False value. The name of a function that is triggered when a cell edition is validated.  \n  All parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the name of the tabular data variable.\n  * payload (dict): the details on this callback's invocation.  \n  \n  This dictionary has the following keys:\n  	+ index (int): the row index.\n  	+ col (str): the column name.\n  	+ value (any): the new cell value cast to the type of the column.\n  	+ user\_value (str): the new cell value, as it was provided by the user.\n  	+ tz (str): the timezone if the column type is date.\n  \n    \n  If this property is not set, the user cannot edit cells.\n\non_delete\n  TODO: Default implementation and False value. The name of a function that is triggered when a row is deleted.  \n  All parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the name of the tabular data variable.\n  * payload (dict): the details on this callback's invocation.  \n  \n  This dictionary has the following keys:\n  	+ index (int): the row index.\n  \n    \n  If this property is not set, the user cannot delete rows.\n\non_add\n  TODO: Default implementation and False value. The name of a function that is triggered when the user requests a row to be added.  \n  All parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the name of the tabular data variable.\n  * payload (dict): the details on this callback's invocation.  \n  This dictionary has the following keys:\n  	+ index (int): the row index.\n  \n    \n  If this property is not set, the user cannot add rows.\n\non_action\n  The name of a function that is triggered when the user selects a row.  \n  All parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the name of the tabular data variable.\n  * payload (dict): the details on this callback's invocation.  \n  This dictionary has the following keys:\n  	+ action: the name of the action that triggered this callback.\n  	+ index (int): the row index.\n  	+ col (str): the column name.\n  	+ reason (str): the origin of the action: "click", or "button" if the cell contains a Markdown link syntax.\n  	+ value (str): the \*link value\* indicated in the cell when using a Markdown link syntax (that is, *reason* is set to "button").\n  \n  .\n\nsize\n  The size of the rows.  \n  Valid values are "small" and "medium".\n\nrebuild (dynamic)\n  If set to True, this allows to dynamically refresh the columns.\n\ndownloadable\n  If True, a clickable icon is shown so the user can download the data as CSV.\n\non_compare\n  A data comparison function that would return a structure that identifies the differences between the different data passed as name. The default implementation compares the default data with the data\[1] value.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class selector(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        label: str = None,
        *,
        mode: str,
        dropdown: bool = False,
        multiple: bool = False,
        filter: bool = False,
        width: Union[str, int] = "360px",
        height: Union[str, int],
        value: any,
        on_change: Callable,
        lov: dict[str, any],
        adapter,
        type: str,
        value_by_id: bool = False,
        propagate: bool,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a selector element.\n\nParameters\n----------\n\nvalue (dynamic)\n  Bound to the selection value.\n\nlabel\n  The label associated with the selector when in dropdown mode.\n\nmode\n  Define the way the selector is displayed:\n  * "radio": list of radio buttons\n  * "check": list of check buttons\n  * any other value: selector as usual.\n  \n\ndropdown\n  If True, the list of items is shown in a dropdown menu.  \n    \n  You cannot use the filter in that situation.\n\nmultiple\n  If True, the user can select multiple items.\n\nfilter\n  If True, this control is combined with a filter input area.\n\nwidth\n  The width of this selector, in CSS units.\n\nheight\n  The height of this selector, in CSS units.\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\nlov\n  The list of values. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/selector/../../../../../userman/gui/binding/#list-of-values) for details.\n\nadapter\n  The function that transforms an element of *lov* into a *tuple(id:str, label:Union\[str,Icon])*.\n\ntype\n  Must be specified if *lov* contains a non\-specific type of data (ex: dict).  \n  *value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type.\n\nvalue_by_id\n  If False, the selection value (in *value*) is the selected element in *lov*. If set to True, then *value* is set to the id of the selected element in *lov*.\n\npropagate\n  Allows the control's main value to be automatically propagated.  \n  The default value is defined at the application configuration level.  \n  If True, any change to the control's value is immediately reflected in the bound application variable.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class file_download(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        content: Union[path, file, URL, ReadableBuffer, None],
        *,
        label: str,
        on_action: Callable,
        auto: bool = False,
        render: bool = True,
        bypass_preview: bool = True,
        name: str,
        width: Union[str, int] = None,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a file_download element.\n\nParameters\n----------\n\ncontent (dynamic)\n  The content to transfer.  \n  If this is a string, a URL, or a file, then the content is read from this source.  \n  If a readable buffer is provided (such as an array of bytes...), and to prevent the bandwidth from being consumed too much, the way the data is transferred depends on the *data\_url\_max\_size* parameter of the application configuration (which is set to 50kB by default):\n  * If the buffer size is smaller than this setting, then the raw content is generated as a data URL, encoded using base64 (i.e. `"data:<mimetype>;base64,<data>"`).\n  * If the buffer size exceeds this setting, then it is transferred through a temporary file.\n  \n  If this property is set to None, that indicates that dynamic content is generated. Please take a look at the examples below for details on dynamic generation.\n\nlabel (dynamic)\n  The label of the button.\n\non_action\n  The name of a function that is triggered when the download is terminated (or on user action if *content* is None).  \n  All the parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the button if it has one.\n  * payload (dict): the details on this callback's invocation.  \n  \n  This dictionary has two keys:\n  	+ action: the name of the action that triggered this callback.\n  	+ args: A list of two elements: *args\[0]* reflects the *name* property and *args\[1]* holds the file URL.\n  \n\nauto\n  If True, the download starts as soon as the page is loaded.\n\nrender (dynamic)\n  If True, the control is displayed.  \n  If False, the control is not displayed.\n\nbypass_preview\n  If False, allows the browser to try to show the content in a different tab.  \n  The file download is always performed.\n\nname\n  A name proposition for the file to save, that the user can change.\n\nwidth\n  The width of the element.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class file_selector(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        content: str,
        *,
        label: str,
        on_action: Callable,
        multiple: bool = False,
        extensions: str = ".csv,.xlsx",
        drop_message: str = "Drop here to Upload",
        notify: bool = True,
        width: Union[str, int] = None,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a file_selector element.\n\nParameters\n----------\n\ncontent (dynamic)\n  The path or the list of paths of the uploaded files.\n\nlabel\n  The label of the button.\n\non_action\n  The name of the function that will be triggered.  \n  All the parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the button if it has one.\n  * payload (dict): a dictionary that contains the key "action" set to the name of the action that triggered this callback.\n  \n\nmultiple\n  If set to True, multiple files can be uploaded.\n\nextensions\n  The list of file extensions that can be uploaded.\n\ndrop_message\n  The message that is displayed when the user drags a file above the button.\n\nnotify\n  If set to False, the user won't be notified of upload finish.\n\nwidth\n  The width of the element.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class image(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        content: Union[path, URL, file, ReadableBuffer],
        *,
        label: str,
        on_action: Callable,
        width: Union[str, int, float] = "300px",
        height: Union[str, int, float],
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates an image element.\n\nParameters\n----------\n\ncontent (dynamic)\n  The image source.  \n  If a buffer is provided (string, array of bytes...), and in order to prevent the bandwidth to be consumed too much, the way the image data is transferred depends on the *data\_url\_max\_size* parameter of the application configuration (which is set to 50kB by default):\n  * If the size of the buffer is smaller than this setting, then the raw content is generated as a\n   data URL, encoded using base64 (i.e. `"data:<mimetype>;base64,<data>"`).\n  * If the size of the buffer is greater than this setting, then it is transferred through a temporary\n   file.\n  \n\nlabel (dynamic)\n  The label for this image.\n\non_action\n  The name of a function that is triggered when the user clicks on the image.  \n  All the parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the button if it has one.\n  * payload (dict): a dictionary that contains the key "action" set to the name of the action that triggered this callback.\n  \n\nwidth\n  The width of this image control, in CSS units.\n\nheight\n  The height of this image control, in CSS units.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class metric(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value: Union[int, float],
        *,
        type: str = "circular",
        min: Union[int, float] = 0,
        max: Union[int, float] = 100,
        delta: Union[int, float],
        delta_color: str,
        title: str = None,
        negative_delta_color: str,
        threshold: Union[int, float],
        show_value: bool = True,
        format: str,
        delta_format: str,
        bar_color: str,
        color_map: dict,
        width: Union[str, number] = None,
        height: Union[str, number] = None,
        layout: dict[str, any],
        template: dict,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a metric element.\n\nParameters\n----------\n\nvalue (dynamic)\n  The value to represent.\n\ntype\n  The type of the gauge.  \n  Possible values are:\n  * "none"\n  * "circular"\n  * "linear"\n  \n  Setting this value to "none" remove the gauge.\n\nmin\n  The minimum value of this metric control's gauge.\n\nmax\n  The maximum value of this metric control's gauge.\n\ndelta (dynamic)\n  The delta value to display.\n\ndelta_color\n  The color that is used to display the value of the *delta* property.  \n  If *negative\_delta\_color* is set, then this property applies for positive values of *delta* only.  \n  If this property is set to "invert", then values for *delta* are represented with the color used for negative values if delta is positive and *delta* is represented with the color used for positive values if it is negative.\n\ntitle\n  The title of the metric.\n\nnegative_delta_color\n  If set, this represents the color to be used when the value of *delta* is negative (or positive if *delta\_color* is set to "invert").\n\nthreshold (dynamic)\n  The threshold value to display.\n\nshow_value\n  If set to False, the value is not displayed.\n\nformat\n  The format to use when displaying the value.  \n  This uses the `printf` syntax.\n\ndelta_format\n  The format to use when displaying the delta value.  \n  This uses the `printf` syntax.\n\nbar_color\n  The color of the bar in the gauge.\n\ncolor_map\n  Indicates what colors should be used for different ranges of the metric. The *color\_map*'s keys represent the lower bound of each range, which is a number, while the values represent the color for that range.  \n  If the value associated with a key is set to None, the corresponding range is not assigned any color.\n\nwidth\n  The width of the metric control, in CSS units.\n\nheight\n  The height of the metric control, in CSS units.\n\nlayout (dynamic)\n  The *plotly.js* compatible [layout object](https://plotly.com/javascript/reference/layout/).\n\ntemplate\n  The Plotly [layout template](https://plotly.com/javascript/layout-template/).\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class progress(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value: int,
        *,
        linear: bool = False,
        show_value: bool = False,
        render: bool = True,
    ) -> None:
        """Creates a progress element.\n\nParameters\n----------\n\nvalue (dynamic)\n  If set, then the value represents the progress percentage that is shown.TODO \- if unset?\n\nlinear\n  If set to True, the control displays a linear progress indicator instead of a circular one.\n\nshow_value\n  If set to True, the progress value is shown.\n\nrender (dynamic)\n  If False, this progress indicator is hidden from the page.\n\n"""  # noqa: E501
        ...

class indicator(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        display: any,
        *,
        value: int,
        float,
        min: Union[int, float] = 0,
        max: Union[int, float] = 100,
        format: str,
        orientation: str = "horizontal",
        width: str = None,
        height: str = None,
        id: str,
        properties: dict[str, any],
        class_name: str,
    ) -> None:
        """Creates an indicator element.\n\nParameters\n----------\n\ndisplay (dynamic)\n  The label to be displayed.  \n  This can be formatted if it is a numerical value.\n\nvalue (dynamic)\n  The location of the label on the \[*min*, *max*] range.\n\nmin\n  The minimum value of the range.\n\nmax\n  The maximum value of the range.\n\nformat\n  The format to use when displaying the value.  \n  This uses the `printf` syntax.\n\norientation\n  The orientation of this slider.\n\nwidth\n  The width of the indicator, in CSS units (used when orientation is horizontal).\n\nheight\n  The height of the indicator, in CSS units (used when orientation is vertical).\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\n"""  # noqa: E501
        ...

class menu(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        lov: Union[str, list[Union[str, Icon, any]]],
        *,
        adapter,
        type: str,
        label: str,
        inactive_ids: Union[str, list[str]],
        width: str = "15vw",
        on_action: Callable,
        active: bool = True,
    ) -> None:
        """Creates a menu element.\n\nParameters\n----------\n\nlov (dynamic)\n  The list of menu option values.\n\nadapter\n  The function that transforms an element of *lov* into a *tuple(id:str, label:Union\[str,Icon])*.\n\ntype\n  Must be specified if *lov* contains a non specific type of data (ex: dict).  \n  *value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type.\n\nlabel\n  The title of the menu.\n\ninactive_ids (dynamic)\n  Semicolon (';')\-separated list or a list of menu items identifiers that are disabled.\n\nwidth\n  The width of the menu when unfolded, in CSS units.  \n  Note that when running on a mobile device, the property *width\[active]* is used instead.\n\non_action\n  The name of the function that is triggered when a menu option is selected.  \n    \n  All the parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the button if it has one.\n  * payload (dict): the details on this callback's invocation.  \n  \n  This dictionary has the following keys:\n  	+ action: the name of the action that triggered this callback.\n  	+ args: List where the first element contains the id of the selected option.\n  \n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\n"""  # noqa: E501
        ...

class navbar(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        lov: dict[str, any],
        *,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a navbar element.\n\nParameters\n----------\n\nlov\n  The list of pages. The keys should be:\n  * page id (start with "/")\n  * or full URL\n  \n  \n  The values are labels. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/navbar/../../../../../userman/gui/binding/#list-of-values) for details.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class status(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value: Union[tuple, dict, list[dict], list[tuple]],
        *,
        without_close: bool = False,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a status element.\n\nParameters\n----------\n\nvalue\n  The different status items to represent.\n\nwithout_close\n  If True, the user cannot remove the status items from the list.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class login(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        title: str = "Log in",
        *,
        on_action: Callable,
        message: str,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a login element.\n\nParameters\n----------\n\ntitle\n  The title of the login dialog.\n\non_action\n  The name of the function that is triggered when the dialog button is pressed.  \n    \n  All the parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the button if it has one.\n  * payload (dict): the details on this callback's invocation.  \n  \n  This dictionary has the following keys:\n  	+ action: the name of the action that triggered this callback.\n  	+ args: a list with three elements:\n  		- The first element is the username\n  		- The second element is the password\n  		- The third element is the current page name\n  \n  \n  \n    \n  When the button is pressed, and if this property is not set, Taipy will try to find a callback function called *on\_login()* and invoke it with the parameters listed above.\n\nmessage (dynamic)\n  The message shown in the dialog.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class chat(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        messages: list[str],
        *,
        users: list[Union[str, Icon]],
        sender_id: str = "taipy",
        with_input: bool = True,
        on_action: Callable,
        page_size: int = 50,
        height: Union[str, int, float],
        show_sender: bool = True,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a chat element.\n\nParameters\n----------\n\nmessages (dynamic)\n  The list of messages. Each item of this list must consist of a list of three strings: a message identifier, a message content, and a user identifier.\n\nusers (dynamic)\n  The list of users. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/chat/../../../../../userman/gui/binding/#list-of-values) for details.\n\nsender_id\n  The user identifier, as indicated in the *users* list, associated with all messages sent from the input.\n\nwith_input (dynamic)\n  If False, the input field is not rendered.\n\non_action\n  The name of a function that is triggered when the user enters a new message.  \n  All the parameters of that function are optional:\n  * *state* (`State^`): the state instance.\n  * *var\_name* (str): the name of the variable bound to the *messages* property.\n  * *payload* (dict): the details on this callback's invocation.  \n  This dictionary has the following keys:\n  	+ *action*: the name of the action that triggered this callback.\n  	+ *args* (list): A list composed of a reason ("click" or "Enter"), the variable name, message, the user identifier of the sender.\n  \n\npage_size\n  The number of messages retrieved from the application and sent to the frontend. Larger values imply more potential latency.\n\nheight\n  The maximum height of this chat control, in CSS units.\n\nshow_sender\n  If False, the sender avatar and name is not displayed.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class tree(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        expanded: Union[bool, list[str]] = True,
        *,
        multiple: bool = False,
        select_leafs_only: bool = False,
        row_height: str,
        label: str = None,
        value: any,
        on_change: Callable,
        lov: dict[str, any],
        adapter,
        type: str,
        value_by_id: bool = False,
        propagate: bool,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
        mode: str,
        dropdown: bool = False,
        filter: bool = False,
        width: Union[str, int] = "360px",
        height: Union[str, int],
    ) -> None:
        """Creates a tree element.\n\nParameters\n----------\n\nvalue (dynamic)\n  Bound to the selection value.\n\nexpanded (dynamic)\n  If Boolean and False, only one node can be expanded at one given level. Otherwise this should be set to an array of the node identifiers that need to be expanded.\n\nmultiple\n  If True, the user can select multiple items by holding the `Ctrl` key while clicking on items.\n\nselect_leafs_only\n  If True, the user can only select leaf nodes.\n\nrow_height\n  The height of each row of this tree, in CSS units.\n\nlabel\n  The label associated with the selector when in dropdown mode.\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\nlov\n  The list of values. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/tree/../../../../../userman/gui/binding/#list-of-values) for details.\n\nadapter\n  The function that transforms an element of *lov* into a *tuple(id:str, label:Union\[str,Icon])*.\n\ntype\n  Must be specified if *lov* contains a non\-specific type of data (ex: dict).  \n  *value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type.\n\nvalue_by_id\n  If False, the selection value (in *value*) is the selected element in *lov*. If set to True, then *value* is set to the id of the selected element in *lov*.\n\npropagate\n  Allows the control's main value to be automatically propagated.  \n  The default value is defined at the application configuration level.  \n  If True, any change to the control's value is immediately reflected in the bound application variable.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\nmode\n  Define the way the selector is displayed:\n  * "radio": list of radio buttons\n  * "check": list of check buttons\n  * any other value: selector as usual.\n  \n\ndropdown\n  If True, the list of items is shown in a dropdown menu.  \n    \n  You cannot use the filter in that situation.\n\nfilter\n  If True, this control is combined with a filter input area.\n\nwidth\n  The width of this selector, in CSS units.\n\nheight\n  The height of this selector, in CSS units.\n\n"""  # noqa: E501
        ...

class part(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        render: bool = True,
        *,
        class_name: str,
        page: str,
        height: str,
        content: any,
        partial: taipy.gui.Partial,
        id: str,
        properties: dict[str, any],
        hover_text: str,
    ) -> None:
        """Creates a part element.\n\nParameters\n----------\n\nclass_name (dynamic)\n  A list of CSS class names, separated by white spaces, that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-part` class name.\n\nrender (dynamic)\n  If True, this part is visible on the page.  \n  If False, the part is hidden and its content is not displayed.\n\npage (dynamic)\n  The page to show as the content of the block (page name if defined or a URL in an *iframe*).  \n  This should not be defined if *partial* is set.\n\nheight (dynamic)\n  The height, in CSS units, of this block.\n\ncontent (dynamic)\n  The content provided to the part. See the documentation section on content providers.\n\npartial\n  A Partial object that holds the content of the block.  \n  This should not be defined if *page* is set.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class expandable(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        title: str,
        *,
        expanded: bool = True,
        partial: taipy.gui.Partial,
        page: str,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
        on_change: Callable,
    ) -> None:
        """Creates an expandable element.\n\nParameters\n----------\n\ntitle (dynamic)\n  Title of this block element.\n\nexpanded (dynamic)\n  If True, the block is expanded, and the content is displayed.  \n  If False, the block is collapsed and its content is hidden.\n\npartial\n  A Partial object that holds the content of the block.  \n  This should not be defined if *page* is set.\n\npage\n  The page name to show as the content of the block.  \n  This should not be defined if *partial* is set.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\n"""  # noqa: E501
        ...

class dialog(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        open: bool = False,
        *,
        on_action: Callable,
        close_label: str = "Close",
        labels: Union[str, list[str]],
        width: Union[str, int, float],
        height: Union[str, int, float],
        partial: taipy.gui.Partial,
        page: str,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a dialog element.\n\nParameters\n----------\n\nopen\n  If True, the dialog is visible. If False, it is hidden.\n\non_action\n  Name of a function triggered when a button is pressed.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * id (str): the identifier of the dialog if it has one.\n  * payload (dict): the details on this callback's invocation.  \n  This dictionary has the following keys:\n  	+ action: the name of the action that triggered this callback.\n  	+ args: a list where the first element contains the index of the selected label.\n  \n\nclose_label\n  The tooltip of the top\-right close icon button. In the on\_action callback, *args* will be set to \-1\.\n\nlabels\n  A list of labels to show in a row of buttons at the bottom of the dialog. The index of the button in the list is reported as args in the on\_action callback (that index is \-1 for the *close* icon).\n\nwidth\n  The width of this dialog, in CSS units.\n\nheight\n  The height of this dialog, in CSS units.\n\npartial\n  A Partial object that holds the content of the block.  \n  This should not be defined if *page* is set.\n\npage\n  The page name to show as the content of the block.  \n  This should not be defined if *partial* is set.\n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class layout(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        columns: str = "1 1",
        *,
        gap: str = "0.5rem",
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a layout element.\n\nParameters\n----------\n\ncolumns\n  The list of weights for each column.  \n  For example, \`"1 2"\` creates a 2 column grid:\n  * 1fr\n  * 2fr\n  \n    \n  The creation of multiple same size columns can be simplified by using the multiply sign eg. "5\*1" is equivalent to "1 1 1 1 1".\n\ngap\n  The size of the gap between the columns.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...

class pane(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        open: bool = False,
        *,
        on_close: Callable,
        anchor: str = "left",
        width: str = "30vw",
        height: str = "30vh",
        persistent: bool = False,
        show_button: bool = False,
        partial: taipy.gui.Partial,
        page: str,
        on_change: Callable,
        active: bool = True,
        id: str,
        properties: dict[str, any],
        class_name: str,
        hover_text: str,
    ) -> None:
        """Creates a pane element.\n\nParameters\n----------\n\nopen (dynamic)\n  If True, this pane is visible on the page.  \n  If False, the pane is hidden.\n\non_close\n  The name of a function that is triggered when this pane is closed (if the user clicks outside of it or presses the Esc key).  \n  All parameters of that function are optional:\n  * state (`State^`): the state instance.\n  * id (optional\[str]): the identifier of the close button if it has one.\n  \n    \n  If this property is not set, no function is called when this pane is closed.\n\nanchor\n  Anchor side of the pane.  \n  Valid values are "left", "right", "top", or "bottom".\n\nwidth\n  Width, in CSS units, of this pane.  \n  This is used only if *anchor* is "left" or "right".\n\nheight\n  Height, in CSS units, of this pane.  \n  This is used only if *anchor* is "top" or "bottom".\n\npersistent\n  If False, the pane covers the page where it appeared and disappears if the user clicks in the page.  \n  If True, the pane appears next to the page. Note that the parent section of the pane must have the *flex* display mode set.\n\nshow_button\n  If True and when the pane is closed, a button allowing the pane to be opened is shown.\n\npartial\n  A Partial object that holds the content of the block.  \n  This should not be defined if *page* is set.\n\npage\n  The page name to show as the content of the block.  \n  This should not be defined if *partial* is set.\n\non_change\n  The name of a function that is triggered when the value is updated.  \n  The parameters of that function are all optional:\n  * state (`State^`): the state instance.\n  * var\_name (str): the variable name.\n  * value (any): the new value.\n  \n\nactive (dynamic)\n  Indicates if this component is active.  \n  An inactive component allows no user interaction.\n\nid\n  The identifier that is assigned to the rendered HTML component.\n\nproperties\n  Bound to a dictionary that contains additional properties for this element.\n\nclass_name (dynamic)\n  The list of CSS class names that are associated with the generated HTML Element.  \n  These class names are added to the default `taipy-<element_type>` class name.\n\nhover_text (dynamic)\n  The information that is displayed when the user hovers over this element.\n\n"""  # noqa: E501
        ...
