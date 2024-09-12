import anywidget
from traitlets import Unicode, observe
from IPython.display import Javascript, display, HTML

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
    def _observe_count(self, change):
        if change.new != "":
            from ipylab import JupyterFrontEnd
            app = JupyterFrontEnd()
            app.commands.execute('notebook:extend-marked-cells-bottom')
            app.commands.execute('notebook:insert-cell-below')
            app.commands.execute('notebook:replace-selection', { 'text': "%%tee\\n" + change.new})
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
  
    // Initialize Chainlit widget
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

        
// Function to add or update the style element
function addOrUpdateStyle() {
  // Select the shadow DOM root
  const shadowRoot = document.querySelector('#chainlit-copilot').shadowRoot;

  // Check if the style element already exists in the shadow DOM
  let existingStyle = shadowRoot.querySelector('style.custom-style');

  // If the style element exists, update its content, otherwise create a new one
  if (existingStyle) {
    existingStyle.innerHTML = `
      .MuiBox-root.css-1gktu8u {
        background-color: rgb(20, 195, 254) !important;
        color: rgb(255, 255, 255) !important; 
      }`;
  } else {
    // Create a new style element
    const style = document.createElement('style');
    style.classList.add('custom-style'); // Add a class to easily identify it
    style.innerHTML = `
      .MuiBox-root.css-1gktu8u {
        background-color: rgb(20, 195, 254) !important;
        color: rgb(255, 255, 255) !important; 
      }`;

    // Append the new style element to the shadow DOM
    shadowRoot.appendChild(style);
  }
}

// Call the function to add or update the style
addOrUpdateStyle();

    window.chainlitCallback = null;
    
    // Add event listener to handle chainlit-call-fn events
    window.addEventListener("chainlit-call-fn", (e) => {
      const { name, args, callback } = e.detail;
      if (name === "test") {
        runcode(args.msg);
        window.chainlitCallback = callback;
        //callback("ran successfully");  // Send a response back to the Chainlit function
      }
    });
  </script>
</body>
'''

    def run(self):
        widget = CounterWidget()
        display(HTML(self.html_code))