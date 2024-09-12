import PySimpleGUI as sg

class GUI:
    """
    A class to create and manage a simple graphical user interface (GUI) using PySimpleGUI.
    
    This class is responsible for setting up the window title and creating the window layout.
    """

    def __init__(self, title):
        """Initializes the GUI with a title for the window."""
        self.title = title

    def create_window(self, layout=None):
        """Creates the window with a specified or default layout.
        
        If no layout is provided, a default layout is used that includes fields 
        for entering an order number and additional comments.
        
        Args:
            layout (list, optional): A custom layout for the window. Defaults to None.
        """
        # Set the theme for the window to 'Black'
        sg.theme('Black')
        
        # Define a basic layout if none is provided
        if layout is None:
            layout = [ 
                [sg.Text('Enter Your Order Number Below')], 
                [sg.Text('Order Number', size=(15, 1)), sg.InputText(key='-ORDER-')], 
                [sg.Text('Additional Comment', size=(15, 1)), sg.InputText(key='-COMMENT-')],
                [sg.Text('', key='-ERROR-', visible=False)],  # Placeholder for error messages
                [sg.Button('Submit'), sg.Cancel()] 
            ] 
        
        # Create the window with the specified title and layout
        window = sg.Window(self.title, layout, grab_anywhere=True, finalize=True)
        
        # Set focus on the input field for the order number
        input_field = window['-ORDER-'].set_focus()

        # Store the window instance as a class attribute
        self.window = window
