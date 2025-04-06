'''Load colormap defs into namespace of geo_colormaps

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2025-04-06 08:29:53
'''

import os
import tkinter as tk
from tkinter import ttk
import traceback

#from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .loader import load_colormaps, get_custom_def_folder
from .custom_errors import ColormapLoadError

# If True, the colormap_list.md file is updated in this repo's root folder.

# If False, the colormap_list.md is updated into a file inside user's default
# config folder,
# in Linux/MacOS, this is `$XDG_CONFIG_HOME/geo_colormaps/colormap_list.md`.
# in Windows, it is `%appdata%\geo_colormaps\colormap_list.md`.
# Only set to True when developing this package
IS_DEV = True


#######################################################################
#                            Global params                            #
#######################################################################

# default colormap definition folder
DEFAULT_DEF_FOLDER = os.path.join(os.path.dirname(__file__), 'colormap_defs')

# custom colormap definition folder
CUSTOM_FOLDER = get_custom_def_folder()

# folder to store default images of plotted colorbars
DEFAULT_IMG_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'images')

# folder to store user custom images of plotted colorbars
CUSTOM_IMG_FOLDER = os.path.join(CUSTOM_FOLDER, 'images')

# markdown file to store defeault colormap list
DEFAULT_COLORMAP_LIST_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'colormap_list.md'))

# markdown file to store default + user custom colormap list
CUSTOM_COLORMAP_LIST_FILE = os.path.join(CUSTOM_FOLDER, 'colormap_list.md')





# function for render jinjia2 template
"""
def _render_colormap_list_doc(colormap_group_list: list, colormap_list_file: str,
                             is_default: bool) -> None:

    # load jinja template
    jinja_template_path = os.path.join(os.path.dirname(__file__), 'docs', 'templates')
    env = Environment(loader=FileSystemLoader(jinja_template_path))
    template = env.get_template('colormap_list.md')

    # render jinja template
    colormap_groups = []
    for ii, groupii in enumerate(colormap_group_list):
        if is_default:
            # if render default list, do not add absolute paths
            groupii.base_folder = 'geo_colormaps/colormap_defs'
            groupii.img_folder = os.path.join('images', os.path.split(groupii.img_folder)[1])

        colormap_groups.append(groupii)

    try:
        readme_str = template.render({'colormap_groups': colormap_groups})
    except Exception:
        print('Warning. Failed to render jinja template.')
    else:
        #print(readme_str)
        # save rendered jinja template to text file
        with open(colormap_list_file, 'w') as fout:
            fout.write(readme_str)
        #print(f'colormap list file {colormap_list_file} created.')

    return
"""


# load default colormaps
DEFAULT_CMAP_GROUPS = load_colormaps(DEFAULT_DEF_FOLDER, DEFAULT_IMG_FOLDER)

# load custom colormaps
CUSTOM_CMAP_GROUPS = []
if os.path.exists(CUSTOM_FOLDER):
    try:
        CUSTOM_CMAP_GROUPS = load_colormaps(CUSTOM_FOLDER, CUSTOM_IMG_FOLDER)
    except ColormapLoadError:
        print(f'Failed to load custom colormaps from {CUSTOM_FOLDER}.')
        traceback.print_exc()
    except Exception:
        traceback.print_exc()
    else:
        all_groups = DEFAULT_CMAP_GROUPS + CUSTOM_CMAP_GROUPS


#if IS_DEV:
    # render default colormap list markdown file
    #_render_colormap_list_doc(DEFAULT_CMAP_GROUPS, DEFAULT_COLORMAP_LIST_FILE, True)
#else:
    # render all colormap list markdown file
    #_render_colormap_list_doc(all_groups, CUSTOM_COLORMAP_LIST_FILE, False)


# add default + custom colormaps into this module's namespace
for obj in all_groups:
    name = obj.name.upper()
    try:
        exec(f'{name} = obj')
    except Exception as e:
        print(f'Failed to add name {name} to module namespace. e: {e}')



#######################################################################
#                          Helper functions                           #
#######################################################################


def list_cmaps(verbose: bool=False) -> dict:
    '''Print default colormaps and custom colormaps (defined in csv files)

    Returns:
        all_cmap_dict (dict): keys: cmap name, values: cmap objects
    '''

    all_cmap_dict = {}

    # get default cmap groups
    if verbose:
        print('These are default colormap groups:')

    default_group = DEFAULT_CMAP_GROUPS
    for cmap_group in default_group:
        if verbose:
            print(f'Group name: {cmap_group.name}')

        cmap_list = list(cmap_group.collection.keys())
        cmap_list.sort()
        for cmap_name in cmap_list:
            cmap_obj = cmap_group.collection[cmap_name]
            if verbose:
                print(f'   {cmap_name:<20s}: {cmap_obj}')

            all_cmap_dict[cmap_name] = cmap_obj

    if len(CUSTOM_CMAP_GROUPS) == 0:
        if verbose:
            print("You haven't added any custom colormaps.")
    else:
        if verbose:
            print('These are custom colormap groups:')

        custom_group = CUSTOM_CMAP_GROUPS
        for cmap_group in custom_group:
            if verbose:
                print(f'Group name: {cmap_group.name}')

            cmap_list = list(cmap_group.collection.keys())
            cmap_list.sort()
            for cmap_name in cmap_list:
                cmap_obj = cmap_group.collection[cmap_name]
                if verbose:
                    print(f'   {cmap_name:<20s}: {cmap_obj}')

                all_cmap_dict[cmap_name] = cmap_obj

    return all_cmap_dict


def plot_cmaps() -> None:
    '''Plot demos of default colormaps and custom colormaps (defined in csv files)
    '''

    # get all cmaps in a dict
    all_cmap_dict = list_cmaps()

    # set up table
    n = len(all_cmap_dict)
    nrows = 3
    ncols = n // nrows
    if nrows * ncols < n:
        ncols += 1

    # create figure and axes
    figure, axes = plt.subplots(nrows, ncols, figsize=(ncols*5, nrows*10),
                                dpi=100,
                                constrained_layout=True)

    # loop through cmaps and plot demo
    for ii, (nameii, cmapii) in enumerate(all_cmap_dict.items()):
        rowii, colii = divmod(ii, ncols)
        axii = axes.flat[ii]
        cmapii.plot_demo(ax=axii)

    # turn off unused axes
    for ii in range(n, nrows * ncols):
        axii = axes.flat[ii]
        axii.axis('off')

    #figure.show()
    plt.close(figure)

    #----------------- Save plot ------------
    os.makedirs(CUSTOM_IMG_FOLDER, exist_ok=True)
    plot_save_name = os.path.join(CUSTOM_IMG_FOLDER, 'all_cmaps_demo.png')
    print(f'\n# Saved cmap demo figure to: {plot_save_name}')
    figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

    return


def gui_picker() -> tuple:
    ''' Display a GUI window with a grid of matplotlib plots for selection.
    Includes scrollbars for handling large plot grids.

    Args:
        nrows (int): Number of rows in the plot grid
        ncols (int): Number of columns in the plot grid
    Returns:
        tuple: (row, col) of the selected plot or None if canceled
    '''

    # Create the main window first
    root = tk.Tk()
    root.title("Colormap Picker")
    root.option_add("*Encoding", "UTF-8")
    root.geometry("800x600")  # Set initial window size

    # Import the theme
    try:
        root.tk.call('source', 'Azure-ttk-theme/azure.tcl')
        root.tk.call("set_theme", "light")
    except tk.TclError:
        # Continue if theme not available
        pass

    # Variable to store the selected subplot
    selected = [None, None]
    selected_cmap = [None]

    # get all colormaps defs - this is the time-consuming part
    all_cmap_dict = list_cmaps(verbose=False)

    # set up table
    n = len(all_cmap_dict)
    ncols = 3
    nrows = n // ncols
    if nrows * ncols < n:
        nrows += 1

    # Create a frame with scrollbars
    outer_frame = tk.Frame(root)
    outer_frame.pack(fill=tk.BOTH, expand=True)

    # Create a prominent loading message
    loading_label = tk.Label(outer_frame,
                            text="Creating colormap plots...",
                            font=("fixed", 36),
                            padx=20,
                            pady=20)
    loading_label.pack(expand=True)

    # Create horizontal and vertical scrollbars
    h_scrollbar = ttk.Scrollbar(outer_frame, orient=tk.HORIZONTAL)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    v_scrollbar = ttk.Scrollbar(outer_frame, orient=tk.VERTICAL)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a canvas for scrollable content
    canvas_container = tk.Canvas(outer_frame,
                              xscrollcommand=h_scrollbar.set,
                              yscrollcommand=v_scrollbar.set)
    canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure the scrollbars to scroll the canvas
    h_scrollbar.config(command=canvas_container.xview)
    v_scrollbar.config(command=canvas_container.yview)

    # Create a frame inside the canvas to hold the plot
    plot_frame = tk.Frame(canvas_container)

    # Force the window to update and display the message
    root.update_idletasks()
    root.update()


    # Create matplotlib figure and subplots
    # Make the figure bigger for large grids
    fig_width = ncols*4
    fig_height = nrows*4
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_width, fig_height),
                            dpi=100,
                            constrained_layout=True
                         )

    # Handle the case where there's only one subplot
    if nrows == 1 and ncols == 1:
        axes = [[axes]]
    elif nrows == 1:
        axes = [axes]
    elif ncols == 1:
        axes = [[ax] for ax in axes]

    # Set up the plots and add titles
    cmap_grid_dict = {}  # create a dict to store cmaps using (row, col) as keys

    # loop through cmaps and plot demo
    all_cmap_keys = list(all_cmap_dict.keys())
    all_cmap_keys.sort()
    for ii, nameii in enumerate(all_cmap_keys):
        cmapii = all_cmap_dict[nameii]
        rowii, colii = divmod(ii, ncols)
        axii = axes[rowii][colii]
        cmapii.plot_demo(ax=axii)
        cmap_grid_dict[(rowii, colii)] = cmapii

        # Update the GUI occasionally to keep it responsive
        if ii % 5 == 0:
            root.update_idletasks()

    # turn off unused axes
    for ii in range(n, nrows * ncols):
        rowii, colii = divmod(ii, ncols)
        axii = axes[rowii][colii]
        axii.axis('off')



    # Create a canvas to display the plots
    plot_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    plot_canvas.draw()
    plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add the plot frame to the scrollable canvas
    canvas_window = canvas_container.create_window((0, 0), window=plot_frame, anchor="nw")

    # Remove the loading message
    loading_label.destroy()

    # Function to handle closing the application
    def close_app():
        root.quit()
        root.destroy()

    # Handle clicking the window close button
    root.protocol("WM_DELETE_WINDOW", close_app)

    # Handle click events
    def on_click(event):
        if event.inaxes is not None:
            # Find which subplot was clicked
            for i in range(nrows):
                for j in range(ncols):
                    if axes[i][j] == event.inaxes:
                        selected[0], selected[1] = i, j

                        selected_cmap[0] = cmap_grid_dict[(i, j)]


                        # Show selection dialog
                        dialog = tk.Toplevel(root)
                        dialog.tk.call('set_theme', 'light')
                        dialog.title("Selected colormap")
                        dialog.geometry("500x350")  # Set bigger initial size to ensure buttons are visible
                        dialog.minsize(400, 300)    # Set minimum size to ensure buttons are always visible

                        # Center the dialog
                        dialog.update_idletasks()
                        width = dialog.winfo_width()
                        height = dialog.winfo_height()
                        x = (root.winfo_screenwidth() // 2) - (width // 2)
                        y = (root.winfo_screenheight() // 2) - (height // 2)
                        dialog.geometry(f"{width}x{height}+{x}+{y}")

                        # Use grid layout for more control
                        dialog.grid_columnconfigure(0, weight=1)
                        dialog.grid_rowconfigure(1, weight=1)  # Make text box expandable

                        # Selection label - row 0
                        label_frame = tk.Frame(dialog, padx=20, pady=10)
                        label_frame.grid(row=0, column=0, sticky="ew")

                        label = tk.Label(label_frame,
                                         text=f"Chosen colormap: {selected_cmap[0].full_name}",
                                         font=("Arial", 12))
                        label.pack(anchor="w")

                        # Get text content for the text box
                        text_content = get_selection_text(selected_cmap[0])

                        # Text box with scrollbar for code - row 1
                        text_frame = tk.Frame(dialog, padx=20)
                        text_frame.grid(row=1, column=0, sticky="nsew")

                        text_frame.grid_columnconfigure(0, weight=1)
                        text_frame.grid_rowconfigure(0, weight=1)

                        text_box = tk.Text(text_frame, wrap=tk.WORD, height=10)  # Set fixed height
                        text_box.grid(row=0, column=0, sticky="nsew")

                        text_scrollbar = tk.Scrollbar(text_frame, command=text_box.yview)
                        text_scrollbar.grid(row=0, column=1, sticky="ns")

                        text_box.config(yscrollcommand=text_scrollbar.set)
                        text_box.insert(tk.END, text_content)

                        # Button frame - row 2
                        button_frame = tk.Frame(dialog, padx=20, pady=15)
                        button_frame.grid(row=2, column=0, sticky="ew")

                        # Function to copy text to clipboard
                        def copy_to_clipboard():
                            dialog.clipboard_clear()
                            dialog.clipboard_append(text_box.get("1.0", tk.END))
                            dialog.update()  # Required for clipboard to work properly

                            # Briefly change the copy button text to indicate success
                            copy_button.config(text="Copied!")
                            dialog.after(1000, lambda: copy_button.config(text="Copy"))

                        # OK button to close everything
                        def on_ok():
                            # Store the selection before closing
                            nonlocal selected
                            dialog.destroy()
                            close_app()

                        # Add copy button
                        copy_button = tk.Button(button_frame, text="Copy", command=copy_to_clipboard, width=10, height=1)
                        copy_button.pack(side=tk.LEFT, padx=(0, 10))

                        # Add OK button
                        ok_button = tk.Button(button_frame, text="OK", command=on_ok, width=10, height=1)
                        ok_button.pack(side=tk.LEFT)

                        # Make dialog modal, but handle exceptions
                        dialog.transient(root)
                        try:
                            dialog.grab_set()
                            root.wait_window(dialog)
                        except tk.TclError:
                            # Ignore grab errors
                            pass

                        return

    # Connect the click event
    plot_canvas.mpl_connect('button_press_event', on_click)

    # Update the scroll region when the plot size changes
    def configure_scroll_region(event):
        canvas_container.configure(scrollregion=canvas_container.bbox("all"))

    # Bind events to update the scroll region
    plot_frame.bind("<Configure>", configure_scroll_region)

    # Make the scrollable area properly sized
    def on_canvas_configure(event):
        canvas_container.itemconfig(canvas_window, width=event.width)

    canvas_container.bind("<Configure>", on_canvas_configure)

    # Add mouse wheel scrolling
    def on_mousewheel(event):
        # Scroll vertically with mousewheel
        canvas_container.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_shift_mousewheel(event):
        # Scroll horizontally with Shift+mousewheel
        canvas_container.xview_scroll(int(-1*(event.delta/120)), "units")

    # Bind mousewheel events for Windows
    canvas_container.bind_all("<MouseWheel>", on_mousewheel)
    canvas_container.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)

    # For Linux/Unix systems
    canvas_container.bind_all("<Button-4>", lambda e: canvas_container.yview_scroll(-1, "units"))
    canvas_container.bind_all("<Button-5>", lambda e: canvas_container.yview_scroll(1, "units"))
    canvas_container.bind_all("<Shift-Button-4>", lambda e: canvas_container.xview_scroll(-1, "units"))
    canvas_container.bind_all("<Shift-Button-5>", lambda e: canvas_container.xview_scroll(1, "units"))

    # Add instructions
    instructions = tk.Label(root, text="Click on a colormap to select it. Use scrollbars or mouse wheel to navigate.", font=("Arial", 10))
    instructions.pack(pady=5)

    # Update the scroll region to encompass the contents
    plot_frame.update_idletasks()
    canvas_container.configure(scrollregion=canvas_container.bbox("all"))

    # Start the GUI event loop
    root.mainloop()

    # Return the selected cmap full_name
    if selected_cmap[0] is not None:
        return selected_cmap[0].full_name
    else:
        return None


# Function to generate custom text based on selection
def get_selection_text(cmap_obj):
    return f"""# Usage of colormap:

# {cmap_obj}

import matplotlib.pyplot as plt
import geo_colormaps

my_cmap = geo_colormaps.{cmap_obj.full_name}

# prepare your data ...
XX, YY = ...
data = ...

# plot data
fig, ax = plt.subplots()
ax.pcolormesh(XX, YY, data,
              cmap=my_cmap.cmap,
              norm=my_cmap.norm,
              extend=my_cmap.extend)

# plot colorbar
cbar = cmap_obj.plot_colorbar(ax, orientation='horizontal', spacing='uniform')
fig.show()
"""


# remove these from namespace
#del os, Environment, FileSystemLoader
del all_groups, name, obj, get_custom_def_folder
del IS_DEV
