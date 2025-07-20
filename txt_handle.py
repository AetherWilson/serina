def read_txt_file(file_path):
    """
    Reads a text file and returns its content as a string.
    
    Args:
        file_path (str): Path to the text file
        
    Returns:
        str: Content of the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Example usage:
# content = read_txt_file("example.txt")
# if content:
#     print(content)