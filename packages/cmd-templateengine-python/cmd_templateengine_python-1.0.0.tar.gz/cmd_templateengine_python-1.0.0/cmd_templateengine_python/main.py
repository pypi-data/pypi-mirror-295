import os
import re
import json
import sys
import shutil
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_WORKERS = 10  # Hardcoded constant for max workers

# нужно проработать error codes
# 0 - успешное завершение
# 1 - неизвестная ошибка
# 2 - неправильный шаблон
# 3 - неправильная спецификация
# 4 - ошибка в AI модели
# и тд

class TemplateEngineV1:
    def __init__(self, command, template_dir, input_dir, output_dir, specs, ignore_list, replacements, quiet, verbose):
        self.command = command
        self.template_dir = template_dir
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.specs = specs
        self.ignore_list = ignore_list
        self.replacements = replacements
        self.quiet = quiet
        self.verbose = verbose

        self.task_execution()

    # Main execution
    # Performs command given
    def task_execution(self):
        if not self.quiet: print("\nStarting the process...")
        match self.command:
            case "create_skeleton":
                self.create_skeleton()
            case "create":
                print("Code 3 - create command not implemented")
            case "extend":
                print("Code 3 - extend command not implemented")
            case "fix":
                print("Code 3 - fix command not implemented")
            case _:
                print(f"Code 1 - {self.command} command unknown")

    # Creates new component skeleton from template
    def create_skeleton(self):
        self.process_files()
        self.process_directories()
        if not self.quiet: print("Code 0 - create_skeleton process completed")

    # Replaces keyword with matching case
    def replacement_function(self, match, replace_with):
        matched_text = match.group()
        result = ''
        for original_char, replacement_char in zip(matched_text, replace_with):
            if original_char.isupper():
                result += replacement_char.upper()
            else:
                result += replacement_char.lower()
        result += replace_with[len(result):]
        return result

    # Replaces keywords in file content
    def replace_in_content(self, content):
        for replacement in self.replacements:
            pattern = re.compile(re.escape(replacement['search']), re.IGNORECASE)
            content = pattern.sub(lambda match: self.replacement_function(match, replacement['replace']), content)
        return content

    # Copies file with processed file content
    def process_file(self, file_path, new_file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            new_content = self.replace_in_content(content)

            # Ensure the new file's directory exists
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
        except Exception as e:
            print(f"Code 1 - error processing file at {file_path}: {e}")

    # Checks if path should be ignored
    def should_ignore(self, path):
        for pattern in self.ignore_list:
            # if re.search(pattern, path):
            if pattern == path:
                return True
        return False

    # Renames directories with keywords in output_dir
    # Note: must be performed after process_files()
    def process_directories(self):
        for root, dirs, files in os.walk(self.output_dir):
            # Rename directories
            for dir_name in dirs[:]:  # Iterate over a slice copy of dirs
                if self.should_ignore(dir_name):
                    dirs.remove(dir_name)  # Remove directory from walk
                    continue
                new_dir_name = dir_name
                for replacement in self.replacements:
                    pattern = re.compile(re.escape(replacement['search']), re.IGNORECASE)
                    new_dir_name = pattern.sub(lambda match: self.replacement_function(match, replacement['replace']), new_dir_name)
                if new_dir_name != dir_name:
                    if self.verbose: print(f"Processing {dir_name} -> {new_dir_name}")
                    os.makedirs(os.path.join(root, new_dir_name), exist_ok=True)
                    shutil.copytree(os.path.join(root, dir_name), os.path.join(root, new_dir_name), dirs_exist_ok=True)
                    shutil.rmtree(os.path.join(root, dir_name))

    # Copies files and replaces keywords in file names
    def process_files(self):
        file_tasks = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for root, dirs, files in os.walk(self.input_dir):
                # Calculate relative path
                relative_path = os.path.relpath(root, self.input_dir) if os.path.relpath(root, self.input_dir) != '.' else ''
                new_root = os.path.join(self.output_dir, relative_path)

                # Process files
                for file_name in files:
                    if self.should_ignore(file_name):
                        continue
                    new_file_name = file_name
                    for replacement in self.replacements:
                        pattern = re.compile(re.escape(replacement['search']), re.IGNORECASE)
                        new_file_name = pattern.sub(lambda match: self.replacement_function(match, replacement['replace']),
                                                    new_file_name)

                    file_path = os.path.join(root, file_name)
                    new_file_path = os.path.join(new_root, new_file_name)
                    if self.verbose: print(f"Processing {file_name} -> {new_file_name} at {new_file_path}")
                    file_tasks.append(executor.submit(self.process_file, file_path, new_file_path))

                # Ignore directories
                for dir_name in dirs[:]:  # Iterate over a slice copy of dirs
                    if self.should_ignore(dir_name):
                        dirs.remove(dir_name)  # Remove directory from walk
                        continue

            for task in as_completed(file_tasks):
                task.result()

# # Creates component skeleton
# def template_engine(spec_file, verbose):
#     specs = load_specifications(spec_file)
#     input_dir = specs['input_dir'] # input_dir must come from command line
#     output_dir = specs['output_dir'] # output_dir must come from command line
#     replacements = specs['replacements'] # replacements must come from command line
#     ignore_list = specs.get('ignore', []) # ignore_list must come from input directory

#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     process_files(input_dir, output_dir, replacements, ignore_list, verbose)
#     process_directories(output_dir, replacements, ignore_list, verbose)

# Parses arguments, checks directories, launches Template Engine
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Template Engine V1 - Create software component skeletons from templates. Commercial license required.")
    # parser.add_argument("-c", "--command", default="create_skeleton", help="Command to execute (create, extend, fix, etc.) | Usage: -c <command>, --command=<command> | Default: create_skeleton")
    parser.add_argument("-t", "--template", required=True, help="Dir path to component template | Usage: -t <path>, --template=<path>")
    # parser.add_argument("-i", "--input", help="Dir path to input software component | Usage: -i <path>, --input=<path>")
    parser.add_argument("-o", "--output", required=True, help="Dir path to output software component | Usage: -o <path>, --output=<path>")
    # parser.add_argument("-s", "--spec", required=True, help="File path to component specifications (formal or informal) | Usage: -s <path>, --spec=<path>")
    parser.add_argument("-g", "--ignore", default=".gitignore", help="File name or relative path in input / template dir to list of ignored paths | Usage: -g <filename>, --ignore=<filename> | Default: .gitignore")
    parser.add_argument("-n", "--name", action="append", help="Replacements to perform | Usage: -n <old_name>:<new_name>, --name=<old_name>:<new_name>")
    parser.add_argument("-q", "--quiet", action="store_true", help="Mute line output | Usage: -q, --quiet")
    parser.add_argument("-v", "--verbose", action="store_true", help="Include verbose line output | Usage: -v, --verbose")
    args = parser.parse_args()


    # Load command
    # command = f"{args.command}"
    command = "create_skeleton"
    # Load template
    template_dir = f"{args.template}"
    # Load input
    # input_dir = f"{args.input}"
    # if input_dir == "None": input_dir = template_dir
    input_dir = template_dir
    # Load output
    output_dir = f"{args.output}"
    # Load spec file
    # spec_file = f"{args.spec}"
    # Load ignore file
    ignore_file = f"{args.ignore}"
    # Load quiet
    quiet = args.quiet
    # Load verbose
    verbose = not args.quiet and args.verbose

    # Load replacements from names
    replacements = []
    if args.name != None:
        for i in range(len(args.name)):
            names = args.name[i].split(':')
            if len(names) < 2: continue
            if verbose: print(f"Adding search & replace: {names[0]} -> {names[1]}")
            replacement = {"search": names[0], "replace": names[1]}
            replacements.append(replacement)

    # Check template dir
    if not os.path.isdir(template_dir):
        print(f"Code 2 - Template directory {template_dir} does not exist.")
        sys.exit(1)

    # Check input dir
    # if not os.path.isdir(input_dir):
    #     print(f"Code 2 - Input directory {input_dir} does not exist.")
    #     sys.exit(1)

    # Check output dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check spec file
    # if not os.path.isfile(spec_file):
    #     print(f"Code 3 - Specification file {spec_file} does not exist.")
    #     sys.exit(1)

    # Load specs
    specs = {}
    # try:
    #     with open(spec_file, 'r') as file:
    #         specs = json.load(file)
    # except Exception as e:
    #     print(f"Code 1 - unable to load JSON from specs file at {spec_file}: {e}")
    #     sys.exit(1)

    # Load ignore list
    ignore_list = []
    ignore_list_path = os.path.join(input_dir, ignore_file)
    if not os.path.isfile(ignore_list_path):
        print(f"Code 2 - ignore file {ignore_file} in {input_dir} does not exist.")
        sys.exit(1)

    with open(ignore_list_path, 'r', encoding='utf-8') as file:
        ignore_strs = file.read().splitlines()
        for ignore in ignore_strs:
            ignore = ignore.strip()
            if ignore == "": continue
            if ignore.find("#") > -1: continue
            if verbose: print(f"Adding to ignore: {ignore}")
            ignore_list.append(ignore)

    # Start Template Engine
    # template_engine(spec_file, verbose)
    template_engine = TemplateEngineV1(command, template_dir, input_dir, output_dir, specs, ignore_list, replacements, quiet, verbose)
