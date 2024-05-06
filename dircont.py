import os

def list_files(startpath):
    tree = []
    root_depth = startpath.count(os.sep)  # Depth of root
    for root, dirs, files in os.walk(startpath):
        current_depth = root.count(os.sep)
        if current_depth - root_depth > 1:
            del dirs[:]  # Don't go beyond one subdirectory level
        level = current_depth - root_depth
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree.append(f"{subindent}{f}")
    return tree

def copy_file_contents(startpath, extensions):
    contents = []
    root_depth = startpath.count(os.sep)  # Depth of root
    for root, dirs, files in os.walk(startpath):
        current_depth = root.count(os.sep)
        if current_depth - root_depth > 1:
            del dirs[:]  # Don't go beyond one subdirectory level
        for file in files:
            if file.split('.')[-1] in extensions:
                filepath = os.path.join(root, file)
                contents.append(f"\nContents of {filepath}:")
                with open(filepath, 'r', encoding='utf-8') as f:
                    contents.append(f.read())
    return contents

def main():
    startpath = '.'  # Current directory
    output_filename = 'directory_contents.txt'
    
    # List all files and directories up to one subdirectory level
    tree = list_files(startpath)
    # Get contents of .py and .txt files
    #contents = copy_file_contents(startpath, ['py', 'txt'])
    
    # Write everything to a file
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(tree))
        #f.write('\n'.join(contents))
    
    print(f"File '{output_filename}' has been created with the directory tree and file contents.")

if __name__ == '__main__':
    main()
