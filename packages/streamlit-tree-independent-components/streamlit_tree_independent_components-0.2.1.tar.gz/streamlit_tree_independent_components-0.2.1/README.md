# streamlit tree independent components

![alt text](src/Demo.jpg)

Component is React component designed to render a hierarchical tree view with checkboxes, integrated with Streamlit for use within Streamlit applications. It allows users to navigate and select items in a nested structure, with customizable icons and state management features.

## Features

Hierarchical Tree Structure:

Renders a nested tree structure using TreeView and TreeItem from Material-UI.
Nodes can have multiple child nodes, creating a multi-level hierarchy.
Checkbox Selection:

## Each node includes a checkbox for selection.

The component manages the selection state, ensuring it reflects the user's choices.
Node Icon Customization:

> Nodes can display different icons based on their type **(folder, settings, document, or a default file icon)**.

### Icons are determined using the determineIcon function.

> Disabled Nodes: Nodes can be marked as disabled using the disable property.
> Disabled nodes are visually distinct (grayed out) and cannot be selected.
> The component skips these nodes when managing state changes and rendering.
> Parent-Child Relationship Management:

Includes functions (getChildById and findParentById) to manage selection states across parent and child nodes.

### Ensures consistent selection/deselection of parent and child nodes.

> State Management: Manages the state using selected (to track selected nodes) and setSelected.
> State updates occur whenever a user interacts with the component.

### Integration with Streamlit:

Uses StreamlitComponentBase and the Streamlit API for seamless integration with Streamlit apps.
Sends updated state back to the Streamlit environment for dynamic interactions.
Recursive Rendering:

> The renderTree method handles recursive rendering of the tree structure, ensuring all child nodes are displayed correctly.

> Expandable Nodes: Includes icons for expanding (ExpandMoreIcon) and collapsing (ChevronRightIcon) nodes, enhancing navigation through the tree.

## Installation instructions

```sh
pip pip install -i streamlit-tree-independent-components
```

## Usage instructions

```
import streamlit as st
from streamlit_tree_independent_components import tree_independent_components


st.subheader("Component with input args")


treeItems = {
   "id":"0",
   "name":"Project Dashboard",
   "icon":"",
   "disable":False,
   "children":[
      {
         "id":"1",
         "name":"Technology Expense Summary",
         "icon":"",
         "disable":False,
         "children":[
            {
               "id":"2",
               "name":"Cost Efficiency Analysis",
               "icon":"",
               "disable":False,
               "children":[
                  {
                     "id":"3",
                     "name":"Financial Data Preparation",
                     "icon":"",
                     "disable":False
                  },
                  {
                     "id":"4",
                     "name":"Database Operations Review",
                     "icon":"",
                     "disable":False,
                     "children":[
                        {
                           "id":"5",
                           "name":"Data Entry for Operations",
                           "icon":"",
                           "disable":False,
                           "children":[
                              {
                                 "id":"6",
                                 "name":"User Data Extension",
                                 "icon":"",
                                 "disable":False,
                                 "children":[
                                    {
                                       "id":"7",
                                       "name":"Data Enhancement Process",
                                       "icon":"",
                                       "disable":False,
                                       "children":[
                                          {
                                             "id":"8",
                                             "name":"Business Analysis Report",
                                             "icon":"",
                                             "disable":False
                                          },
                                          {
                                             "id":"9",
                                             "name":"Performance Overview",
                                             "icon":"",
                                             "disable":False,
                                             "children":[
                                                {
                                                   "id":"10",
                                                   "name":"Manual Input for Performance",
                                                   "icon":"",
                                                   "disable":False
                                                },
                                                {
                                                   "id":"11",
                                                   "name":"Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation",
                                                   "icon":"",
                                                   "disable": False
                                                }
                                             ]
                                          }
                                       ]
                                    }
                                 ]
                              }
                           ]
                        }
                     ]
                  }
               ]
            }
         ]
      }
   ]
}

checkItems = ["0","1","2","3","4","5","6","7","9","8"]
if "change" not in st.session_state:
    st.session_state["change"] = checkItems
if "i" not in st.session_state:
    st.session_state["i"] = 0
if "disable" not in st.session_state:
    st.session_state["disable"] = False
if "single_select" not in st.session_state:
    st.session_state["single_select"] = False

change = st.button("Select index from 0 to 9")
if change:
    st.session_state["change"] = ["0", "1", "2", "3", "4", "5", "6", "7", "9", "8"]

change2 = st.button("Deselect all")
if change2:
    st.session_state["change"] = []

disable_toggle = st.button("Toggle Treeview View Enable/Disable")
if disable_toggle:
    st.session_state["disable"] = not st.session_state["disable"]

st.warning(f"Treeview disable! Current set: {st.session_state['disable']}")

single_select = st.button("Toggle Single Select True/False")
if single_select:
    st.session_state["single_select"] = not st.session_state["single_select"]

st.warning(f"Treeview single_select ! Current set: {st.session_state['single_select']}")

with st.container(border=True):
   result = tree_independent_components(treeItems, checkItems=st.session_state["change"],disable=st.session_state['disable'], single_select=st.session_state["single_select"], x_scroll=True, y_scroll=True, x_scroll_width=40, key="demo", frameHeight=40, border=False)

try:
   st.write(sorted(result["setSelected"], key=int))
except:
  pass

```
