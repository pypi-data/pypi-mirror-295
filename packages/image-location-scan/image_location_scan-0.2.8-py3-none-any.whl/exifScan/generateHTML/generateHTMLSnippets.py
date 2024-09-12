# a separate module with functions that generate snippets to make the main HTML function more legible.
import json
import hashlib
from datetime import datetime


def stable_hash(name):
    return int(hashlib.md5(name.encode()).hexdigest(), 16)


def cssColors_for_geojson(name, color_list, mapElementsDict):
    # Create a color from a stable hash of name
    index = stable_hash(name) % len(color_list)
    color = color_list.pop(index)
    mapElementsDict[name]['color'] = color
    el_id = name.replace(' ', '_')

    return f'''
.{el_id}{{
    stroke:{color};
    fill:{color};
}}

'''


def year_filter_slider(earliest_year):
    current_year = datetime.now().year
    js = f'''
    function createSliders() {{
        const slider = document.getElementById('sliderContainer');

        noUiSlider.create(slider, {{
            start: [{earliest_year}, {current_year}],
            step: 1,
            tooltips: true,
            range: {{
                'min': {earliest_year},
                'max': {current_year}
            }},
            format: {{
                // 'to' the formatted value. Receives a number.
                to: function (value) {{
                    return Math.round(value);
                }},
                // 'from' the formatted value.
                from: function (value) {{
                   return Math.round(value);
                }}
            }}
        }});
        slider.noUiSlider.on('update', filterByDateRange);
    }}

    // Function to filter elements by date range
    function filterByDateRange(values) {{
        console.log(values)
        // Get all elements with the class 'leaflet-interactive'
        const elements = document.getElementsByClassName('leaflet-interactive');

        for (let i = 0; i < elements.length; i++) {{
            const element = elements[i];
            const yearClass = Array.from(element.classList).find(cls => cls.startsWith('year-'));

            if (yearClass) {{
                const year = parseInt(yearClass.split('-')[1]);
                if (year >= values[0] && year <= values[1]) {{
                    element.style.display = ''; // Show element
                }} else {{
                    element.style.display = 'none'; // Hide element
                }}
            }}
        }}
    }}
    createSliders();
'''
    return js


def HTMLTail(navlinks, tabsContent, jsContent, copyButtonString):
    html = '''
<div class="offcanvas offcanvas-bottom" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="offcanvasScrolling" aria-labelledby="offcanvasScrollingLabel">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasScrollingLabel"></h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div id="offcanvas-body-id" class="offcanvas-body"><div class="nav nav-tabs" id="nav-tab" role="tablist">'''
    html = html + ''.join(navlinks)
    html = html + '</div><div class = "tab-content" id = "tableTabContent" >'
    html = html + ''.join(tabsContent)
    html = html + '</div>  </div></div><script>$(document).ready( function () {'
    html = html + ''.join(jsContent)
    html = html + f' }} );</script><script>{copyButtonString}</script></html>'
    return html


def rightClick(mapElementsDict):
    colors = {}
    for key, value in mapElementsDict.items():
        if 'color' in value:
            colors[key] = value['color']
    colors_json = json.dumps(colors)

    return f'''
<script>
    const colors = {colors_json}
    class ElementToggler {{
        constructor(targetClass, toggleClass) {{
            this.targetClass = targetClass;
            this.toggleClass = toggleClass;
            this.contextEvents = new Map();

        }}

        addEvent() {{
            let elements = document.getElementsByClassName(this.targetClass);
            for (let i = 0; i < elements.length; i++) {{
                const element = elements[i];

                if (!this.contextEvents.has(element)) {{
                    element.addEventListener('contextmenu', (event) => {{
                        event.preventDefault();
                        element.classList.toggle(this.toggleClass);

                    }});
                    this.contextEvents.set(element, true);

                }}

            }}

        }}

    }}

    class ChangeLabelColors{{
         constructor(targetClass) {{
            this.targetClass = targetClass;
        }}
        changeColors(){{
            var checkboxes = document.querySelectorAll(this.targetClass);
            for (var i = 0; i < checkboxes.length; i++) {{
                const checkbox= checkboxes[i];
                const name =checkbox.nextSibling.innerText.trim();
                const color = colors[name];
                checkbox.parentElement.style.color = color;

            }}

        }}


    }}

    const toggler = new ElementToggler('animateVisibility', 'noFill');
    const colorsetup = new ChangeLabelColors('.leaflet-control-layers input[type="checkbox"]');

    window.onload = function() {{
        //add context menu event on click
        const control = document.getElementsByClassName('folium-map')[0]
        control.addEventListener('pointerup',()=>{{
            toggler.addEvent();
            // set timeout to ensure popup is populated.
            setTimeout(makeCopyable,400);


        }});

        colorsetup.changeColors();


    }};

    const copyMap = new WeakMap();

    function makeCopyable(){{
        const copyEL = document.getElementsByClassName('copyText');
        for (var i = 0; i < copyEL.length; i++) {{
            const parent = copyEL[i].parentElement;
            const cellText= parent.textContent;
            if(!copyMap.has(parent)){{

                parent.addEventListener( 'click', () => {{

                    // Copy the cell text to clipboard
                    navigator.clipboard.writeText( cellText )
                        .then( () => {{

                            console.log( `Copied: ${{cellText
                            }}` );
                            parent.classList.add('flashGreen');

                            // Remove the 'flash' class after the animation has completed
                            setTimeout(function() {{
                                parent.classList.remove('flashGreen');

                            }}, 600); // The same duration as your animation


                        }} )
                        .catch( error => {{

                            console.error( 'Error copying text:', error );
                             parent.classList.add('flashRed');

                            // Remove the 'flash' class after the animation has completed
                            setTimeout(function() {{
                                parent.classList.remove('flashRed');

                            }}, 200); // The same duration as your animation

                        }} );

                }} );
                copyMap.set(parent,true);

            }}

        }}

    }}
</script>
'''


def copyButton():

    return '''

function makeCellsCopyable(tableId, headerName) {
    const table = document.getElementById(tableId);
    if (table) {
        const headerCells = table.querySelectorAll("thead tr th");

        headerCells.forEach((headerCell, index) => {
            const columnHeader = headerCell.innerHTML; // Get the header name

            if (columnHeader === headerName) {
                const dataCells = table.querySelectorAll(
                    `tbody tr td:nth-child(${index + 1})`,
                );
                dataCells.forEach((dataCell) => {
                    const cellText = dataCell.textContent;
                    dataCell.textContent = "";

                    // Create a div element
                    const div = document.createElement("div");
                    div.style.display = "flex";
                    div.style.justifyContent = "space-between";
                    div.style.alignItems = "flex-start";

                    // Create a text node for the cell text
                    const textNode = document.createTextNode(cellText);
                    div.appendChild(textNode);

                    // Create a button element
                    const copyButton = document.createElement("button");
                    copyButton.classList.add("btn", "btn-secondary", "d-flex");
                    copyButton.type = "button";
                    copyButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
                        <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z"/>
                        <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z"/>
                    </svg>`;
                    div.appendChild(copyButton);

                    // Append the div to the cell
                    dataCell.appendChild(div);

                    copyButton.addEventListener("click", (e) => {
                        e.stopPropagation();

                        // Copy the cell text to clipboard
                        navigator.clipboard
                            .writeText(cellText)
                            .then(() => {
                                console.log(`Copied: ${cellText}`);
                            })
                            .catch((error) => {
                                console.error("Error copying text:", error);
                            });
                    });
                    // Append the button to the cell
                });
            }
        });
    }
}
'''


def navLink(navId, name, selected=False):
    active = '' if selected is False else ' active'
    return f'<button class="nav-link{active}" id="{navId}-tab" data-bs-toggle="tab" data-bs-target="#target{navId}" type="button" role="tab" aria-controls="{navId}" aria-selected="true">{name}</button>'


def tabDivs(navId, name, content, selected=False):
    classString = '' if selected is False else 'show active'

    return f'''
    <div class = "tab-pane fade {classString}" id = "target{navId}" role = "tabpanel" aria-labelledby="{navId}-tab">
    <h2 class='text-center p-3'>{name}</h2>
    {content.to_html(table_id="table" + navId, classes="table table-striped responsive")}
    </div>
    '''


def tableJs(navId):
    return f"$('#table{navId}').DataTable({{responsive:true}});  document.getElementById('table{navId}').style.width='';"


def zoomOnEl(soup, mapId, tableId, geojsonId):
    script = soup.new_tag('script', type='module')
    script.append(f'''const table = document.getElementById( '{tableId}' );
    const headerCells = table.querySelectorAll( 'thead tr th' );
    headerCells.forEach( ( headerCell, index ) => {{
        const columnHeader = headerCell.innerHTML; // Get the header name
        if ( columnHeader == 'index' ) {{
            const dataCells = table.querySelectorAll( `tbody tr td:nth-child(${{index + 1}})` );
            dataCells.forEach(
                dataCell => {{
                    dataCell.parentElement.addEventListener('click',()=>zoomToFeature({geojsonId},dataCell.textContent));
                }}
             );
        }}
    }} );
function zoomToFeature(geojsonId,index) {{
    if( geojsonId && {mapId}){{
        geojsonId.eachLayer(function (layer) {{
            if (layer.feature.properties.index == index) {{
                {mapId}.addLayer(geojsonId)
                {mapId}.flyToBounds(layer.getBounds(),{{duration:2}});
            }}
        }});
    }}
}}
''')
    return script
