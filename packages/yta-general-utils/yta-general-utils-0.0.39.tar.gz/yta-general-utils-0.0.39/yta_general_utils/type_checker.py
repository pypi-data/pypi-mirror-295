import inspect

def variable_is_type(variable, type):
    """
    Checks if the type of the provided 'variable' is the also provided
    'type', returning True if yes or False if not.
    """
    # TODO: Maybe let this accept array of types to check 
    # if one of them (?)
    if isinstance(variable, type):
        return True
    
    return False

def code_file_is(parameter, filename):
    """
    Checks if the provided parameter code is contained in the also
    provided 'filename'. This method is useful to check Enum objects
    or classes as we know the name we use for the files.

    This method was created to be able to check if a function that
    was passed as parameter was part of a custom Enum we created
    and so we could validate the was actually that custom Enum.
    Working with classes was not returning the custom Enum class
    created, so we needed this.
    """
    if inspect.getfile(parameter).endswith(filename):
        return True
    
    return False

# TODO: Move this to another file as this is not actually
# a type checker, is a fact checker (I don't know how to
# explain this)
def is_google_drive_url(google_drive_url: str):
    """
    Checks if the provided 'google_drive_url' is a string with a
    valid Google Drive url format or not. It returns True if yes
    or False if not.
    """
    if google_drive_url.startswith('drive.google.com/file/d/'):
        google_drive_url = 'https://' + google_drive_url

    if google_drive_url.startswith('https://drive.google.com/file/d/'):
        return True
    
    return False