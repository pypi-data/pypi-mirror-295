"""
This module contains related class for generating the graphviz graph.

The following class is available:

    * :class:`Graphviz`
"""

# pylint: disable=missing-module-docstring
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-function-args
# pylint: disable=too-many-instance-attributes
# pylint: disable=trailing-whitespace
# pylint: disable=protected-access
# pylint: disable=no-self-use
import uuid
from hana_ml.visualizers.model_report import TemplateUtil
from hana_ml.visualizers.ui_components import HTMLFrameUtils


def build_frame_html(frame_id, frame_src, frame_height):
    frame_html = """
        <iframe
            id="{iframe_id}"
            width="{width}"
            height="{height}"
            srcdoc="{src}"
            style="border:1px solid #ccc"
            allowfullscreen="false"
            webkitallowfullscreen="false"
            mozallowfullscreen="false"
            oallowfullscreen="false"
            msallowfullscreen="false"
        >
        </iframe>
    """.format(
        iframe_id=frame_id,
        width='100%',
        height=frame_height,
        src=frame_src
    )

    return frame_html


# https://www.graphviz.org/
class Graphviz(object):
    __TEMPLATE = TemplateUtil.get_template('graphviz.html')

    def __init__(self, graphviz_str):
        if graphviz_str is None or graphviz_str == '':
            raise ValueError('No value was passed to the graphviz_str parameter!')
        self.html_str = Graphviz.__TEMPLATE.render(graphviz_str=graphviz_str.replace('\n', '').replace('\r\n', ''))
        self.frame_src_str = HTMLFrameUtils.build_frame_src(self.html_str)
        self.frame_id = '{}'.format(uuid.uuid4()).replace('-', '_').upper()
        self.iframe_html = None

    def generate_notebook_iframe(self, iframe_height: int = 1000):
        """
        Renders the graphviz graph as a notebook iframe.

        Parameters
        ----------
        iframe_height : int, optional
            Frame height.

            Defaults to 1000.
        """
        self.iframe_html = build_frame_html(self.frame_id, self.frame_src_str, iframe_height)
        HTMLFrameUtils.display(self.iframe_html)

    def generate_html(self, filename: str):
        """
        Saves the graphviz graph as a html file.

        Parameters
        ----------
        filename : str
            Html file name.
        """
        TemplateUtil.generate_html_file("{}_graphviz.html".format(filename), self.html_str)
