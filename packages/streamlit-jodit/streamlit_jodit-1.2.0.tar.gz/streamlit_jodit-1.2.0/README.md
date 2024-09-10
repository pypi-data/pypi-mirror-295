# streamlit-jodit

Streamlit component that allows you to use Jodit HTML editor in streamlit. Jodit is a open source rich text editor
https://xdsoft.net/jodit/

GitHub - https://github.com/akshay1728/streamlit-jodit

## Installation instructions

```sh
pip install streamlit-jodit
```

## Usage instructions


```python
import streamlit as st

from streamlit_jodit import st_jodit

config={
            
            'minHeight':300,
        'uploader': {
            'insertImageAsBase64URI': True,
            'imagesExtensions': ['jpg', 'png', 'jpeg', 'gif', 'svg', 'webp']
                    },
             }
value='Initial text to be displayed in editor'
content = st_jodit(config=config,value=value)
st.write(content)
```
By default code will pass readonly:false as config to the component. List of options for config is available at https://xdsoft.net/jodit/docs/options.html