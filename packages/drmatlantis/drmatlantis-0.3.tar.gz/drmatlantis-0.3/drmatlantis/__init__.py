import anywidget
from traitlets import Unicode, observe
from IPython.display import Javascript, display, HTML
from IPython import get_ipython
from IPython.core import magic_arguments
from IPython.core.magic import register_cell_magic
from IPython.utils.capture import capture_output
import traceback
import json

class CounterWidget(anywidget.AnyWidget):
    _esm = """
    export function render({ model, el }) {
        window.runcode = function(newCode) {
            model.set("code", newCode); // Set the value from the console
            model.save_changes(); // Sync changes with the model
        };
    }
    """

    code = Unicode("").tag(sync=True)

    @observe("code")
    def _observe_code(self, change):
        if change.new != "":
            from ipylab import JupyterFrontEnd
            app = JupyterFrontEnd()
            app.commands.execute('notebook:extend-marked-cells-bottom')
            app.commands.execute('notebook:insert-cell-below')
            app.commands.execute('notebook:replace-selection', { 'text': "%%tee\n" + change.new})
            app.commands.execute('notebook:run-cell')
            self.value = ""

class DrMatlantisServer:
    def __init__(self):
        self.html_code = '''
<head>
  <meta charset="utf-8" />
</head>
<body>
  <!-- Chainlit Widget -->
  <script src="http://localhost:8000/copilot/index.js"></script>
  <script>
    window.mountChainlitWidget({
      chainlitServer: "http://localhost:8000",
      theme: "light",
      button:{
          style:{
              bgcolor: "#01a6de",
              bgcolorHover:"#0180ab",
              borderWidth:0
          }
      }
    });

    function addOrUpdateStyle() {
      const shadowRoot = document.querySelector('#chainlit-copilot').shadowRoot;
      let existingStyle = shadowRoot.querySelector('style.custom-style');
      if (existingStyle) {
        existingStyle.innerHTML = `
          .MuiBox-root.css-1gktu8u {
            background-color: rgb(20, 195, 254) !important;
            color: rgb(255, 255, 255) !important; 
          }`;
      } else {
        const style = document.createElement('style');
        style.classList.add('custom-style');
        style.innerHTML = `
          .MuiBox-root.css-1gktu8u {
            background-color: rgb(20, 195, 254) !important;
            color: rgb(255, 255, 255) !important; 
          }`;
        shadowRoot.appendChild(style);
      }
    }
    addOrUpdateStyle();

    window.chainlitCallback = null;

    window.addEventListener("chainlit-call-fn", (e) => {
      const { name, args, callback } = e.detail;
      if (name === "test") {
        runcode(args.msg);
        window.chainlitCallback = callback;
      }
    });
  </script>
</body>
'''

    def run(self):
        widget = CounterWidget()
        display(HTML(self.html_code))

stderrV = ""
@magic_arguments.magic_arguments()
@magic_arguments.argument('output', type=str, default='', nargs='?',
help="""The name of the variable in which to store output.
This is a utils.io.CapturedIO object with stdout/err attributes
for the text of the captured output.
CapturedOutput also has a show() method for displaying the output,
and __call__ as well, so you can use that to quickly display the
output.
If unspecified, captured output is discarded.
"""
)
@magic_arguments.argument('--no-stderr', action="store_true",
help="""Don't capture stderr."""
)
@magic_arguments.argument('--no-stdout', action="store_true",
help="""Don't capture stdout."""
)
@magic_arguments.argument('--no-display', action="store_true",
help="""Don't capture IPython's rich display."""
)
@register_cell_magic
def tee(line, cell):
    args = magic_arguments.parse_argstring(tee, line)
    out = not args.no_stdout
    err = not args.no_stderr
    disp = not args.no_display

    with capture_output(out, err, disp) as io:
        indented_cell_code = "\n".join(["    " + line for line in cell.splitlines()])
        get_ipython().run_cell(f"""
        global stderrV
        stderrV = ''
        try:
            {indented_cell_code}
        except Exception as inst:
            stderrV = 'Exception occurred: ' + traceback.format_exc()
            raise inst
        """)
    if args.output:
        get_ipython().user_ns[args.output] = io, stderrV

    output_to_llm = ""

    if io.stdout and not io.stdout == "":
        output_to_llm += f"The code produced this text: \n{io.stdout}\n"
    else:
        output_to_llm += "No text output produced by the code. If there should have been any printed text, please try again!\n"

    if io.outputs:
        output_to_llm += f"The code produced {len(io.outputs)} display objects! While you cannot see these objects, the user should be able to see all of them. Check with the user if they see all the displays and if they are correct.\n"
    else:
        output_to_llm += "No videos, images/gifs, audios, graphs, tables, animations, or any other display objects produced by the code. If there should have been any of this, please try again!\n"
    
    if stderrV != "":
        output_to_llm += f"The code produced these errors:\n {stderrV}\n"

    escaped_output = json.dumps(output_to_llm)

    js_code = f"window.chainlitCallback({escaped_output}); console.log({escaped_output});"

    display(Javascript(js_code))

    io()
