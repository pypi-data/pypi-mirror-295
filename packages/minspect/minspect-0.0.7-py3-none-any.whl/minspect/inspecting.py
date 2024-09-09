import importlib
import importlib._bootstrap
import importlib.util
import inspect as inspectlib
import logging
import sys
import traceback
from importlib import import_module
from pkgutil import iter_modules
from typing import Any, Dict, Literal

import click
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table


def load_all_modules(mod) -> list[tuple[str, Any]]:
    out = []
    try:
        for module in iter_modules(mod.__path__ if hasattr(mod, "__path__") else []):
            try:
                # Corrected line: Use mod.__name__ for the package name and module.name for the module name
                full_module_name = f"{mod.__name__}.{module.name}"
                imported_module = import_module(full_module_name)

                out.append((module.name, imported_module))
            except Exception as e:
                print(f"Error loading module {module.name}: {e}")
    except Exception as e:
        traceback.print_exc()
        print(f"Error loading modules from {mod.__name__} {e}")

    return out

def is_standard_lib(module):
    if not inspectlib.ismodule(module):
        return False
    try:
        if hasattr(module, "__name__") and  module.__name__ in sys.builtin_module_names:
            return True  # Module is a built-in module
    except Exception as e:
        traceback.print_exc()  
        print(f"Error checking if module {module.__name__} is a standard library module: {e}")
        return False

def get_root_module(module):
    if hasattr(module, "__module__"):
        return get_root_module(module.__module__)
    elif hasattr(module, "__name__"):
        return module.__name__.split(".")[0]
    elif hasattr(module, "name"):
        return module.name.split(".")[0]
    elif hasattr(module, "__package__"):
        return module.__package__
    return None
def is_imported(module, obj):
    try:
        logging.debug(f"root module of obj {obj}: {get_root_module(inspectlib.getmodule(obj))}")
        logging.debug(f"root module of module {module}: {get_root_module(inspectlib.getmodule(module))}")
        if get_root_module(inspectlib.getmodule(obj)) == get_root_module(inspectlib.getmodule(module)):
            return False

        return True
    except Exception as e:
        traceback.print_exc()
        print(f"Error checking if {obj} is imported from {module}: {e}")
        if inspectlib.getmodule(obj) is None:
            print(f"{obj} has no module")

            return False
        return True


def get_full_name(obj):
    """Returns the full package, module, and class name (if applicable) for classes, functions, modules, and class member functions."""
    if inspectlib.isclass(obj):
        return f"{obj.__module__}.{obj.__name__}"
    elif inspectlib.isfunction(obj) or inspectlib.ismethod(obj):
        if hasattr(obj, '__qualname__'):
            return f"{obj.__module__}.{obj.__qualname__}"
        else:
            return f"{obj.__module__}.{obj.__name__}"
    elif inspectlib.ismodule(obj):
        return obj.__name__
    else:
        return "Unknown type"

def collect_info(obj: Any, depth: int = 1, current_depth: int = 0, signatures: bool = True, docs: bool = False, code: bool = False, imports: bool = False) -> Dict[str, Any]:
    """Collect information about the given object and its members.

    Args:
        obj (Any): The object to inspect.
        depth (int): The depth of inspection for nested objects.
        current_depth (int): The current depth of inspection.
        signatures (bool): Whether to include function signatures.
        docs (bool): Whether to include docstrings.
        code (bool): Whether to include source code.
        imports (bool): Whether to include imported modules.

    Returns:
        Dict[str, Any]: A dictionary containing the collected information.
    """
    if current_depth > depth:
        return {}
    
    members_dict = {}
    if inspectlib.isclass(obj) or inspectlib.ismodule(obj):
        members = inspectlib.getmembers(obj)
    else:
        members = [(obj.__name__, obj)]
    
    for member, member_obj in members:
        if member.startswith("__") and member.endswith("__"):
            continue
        
        if is_standard_lib(member_obj) and obj.__name__ != 'math':
            continue
        if is_imported(obj, member_obj) and not imports:
            continue
        if inspectlib.isbuiltin(member_obj) and obj.__name__ != 'math':
            continue

        member_info = {}
        member_info["type"] = "class" if inspectlib.isclass(member_obj) else "module" if inspectlib.ismodule(member_obj) else "function" if inspectlib.isfunction(member_obj) or inspectlib.ismethod(member_obj) else "attribute"
        member_info["path"] = get_full_name(member_obj)

        if docs:
            docstring = inspectlib.getdoc(member_obj)
            if docstring:
                member_info["docstring"] = docstring.strip()

        if signatures and (inspectlib.isfunction(member_obj) or inspectlib.ismethod(member_obj) or inspectlib.isclass(member_obj)):
            try:
                member_info["signature"] = str(inspectlib.signature(member_obj))
            except ValueError:
                member_info["signature"] = "Signature not available"

        if code and (inspectlib.isfunction(member_obj) or inspectlib.ismethod(member_obj)):
            try:
                source_code = inspectlib.getsource(member_obj)
                member_info["code"] = source_code
            except OSError:
                member_info["code"] = "Source code not available"

        if inspectlib.isclass(member_obj) or inspectlib.ismodule(member_obj):
            member_info["members"] = collect_info(member_obj, depth, current_depth + 1, signatures, docs, code, imports)

        members_dict[member] = member_info
    
    # Add docstring for the object itself
    if docs:
        obj_docstring = inspectlib.getdoc(obj)
        if obj_docstring:
            members_dict["docstring"] = obj_docstring.strip()
    
    return members_dict



def render_dict(members_dict: Dict[str, Any], indent: int = 0, depth=0, max_depth=None) -> None:
    if depth > max_depth:
        return
    console = Console()
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Name", style=" white", width=20)
    table.add_column("Type", style=" magenta")
    table.add_column("Path", style="white")
    table.add_column("Signature", style="yellow", no_wrap=True)
    table.add_column("Docstring", style="white")

    def sort_key(item):
        name, info = item
        if not isinstance(info, dict):
            return (3, name)  # Default to the end if not a dict
        docstring_present = 0 if info.get("docstring") else 1
        type_order = {"module": 0, "function": 1, "class": 2}
        type_ = info.get("type", "")
        type_rank = type_order.get(type_, 3)
        return (docstring_present, type_rank, name)

    sorted_members = sorted(members_dict.items(), key=sort_key)
    
    for name, info in sorted_members:
        if isinstance(info, dict):
            type_ = info.get("type", "")
            path = info.get("path", "")
            signature = info.get("signature", "")
            docstring = info.get("docstring", "")
            
            # Truncate long strings
            docstring = (docstring[:50] + '...') if len(docstring) > 50 else docstring
            signature = (signature[:20] + '...') if len(signature) > 20 else signature

            table.add_row(name, type_, path, signature, docstring)
        else:
            # Handle string values
            table.add_row(name, "Value", "", "", str(info))

    for name, info in sorted_members:
        if not isinstance(info, dict):
            continue
        docstring = info.get("docstring", "")
        signature = info.get("signature", "")
        if docstring:
            console.print(Markdown(f"**{name}:**\n```python\n{docstring}\n```"))
        if info.get("members") and depth < max_depth + 1:
            render_dict(info["members"], indent + 2, depth + 1, max_depth)

    console.print(table)

def get_info(module, depth: int = 1, signatures: bool = True, docs: bool = True, code: bool = False, imports: bool = False) -> Dict[str, Any]:
    """Get information about the given module and its members.

    Args:
        module: The module to inspect.
        depth (int): The depth of inspection for nested objects.
        signatures (bool): Whether to include function signatures.
        docs (bool): Whether to include docstrings.
        code (bool): Whether to include source code.
        imports (bool): Whether to include imported modules.

    Returns:
        Dict[str, Any]: A dictionary containing the collected information.
    """
    console = Console()
    console.print(f"[bold cyan]Inspecting: {module.__name__}[/bold cyan]")
    collected_info = collect_info(module, depth, signatures=signatures, docs=docs, code=code, imports=imports)
    render_dict(collected_info, depth=0, max_depth=depth)
    return collected_info

def inspect_library(module_or_class, depth, signatures=True, docs=True, code=False, imports=False, all=False, markdown=False):
    """Inspect a Python module or class. Supports uvicorn-style module or class names or dot-separated paths."""
    parts = module_or_class.split(".")
    module_name = parts[0]
    if ":" in parts[-1]:
        parts[-1] = parts[-1].split(":")[0]
        parts.append(module_or_class.split(":")[-1])
    obj = None

    def import_module_(module_name):

        module = import_module(module_name)
        obj = module
        if obj is None:
            spec = importlib.util.find_spec(module_name)
            module = importlib.util.module_from_spec(spec)
        for part in parts[1:]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                try:
                    obj = import_module(f"{obj.__name__}.{part}")
                except ImportError:
                    print(f"Debug: Attribute or module not found: {part}")
                    raise ImportError(f"Module or attribute not found: {module_or_class}")  # noqa: B904
        return obj
    try:
        obj = import_module_(module_name)
      
    except ModuleNotFoundError as e:
        sys.path.append(".")
        obj = import_module_(module_name)

    except ImportError as e:
        print(f"Debug: Import error: {e}")
        raise
    except AttributeError as e:
        print(f"Debug: Attribute error: {e}")
        raise ImportError(f"Attribute not found: {module_or_class}")

    if all:
        signatures = docs = code = imports = True
    
    try:
        result = get_info(obj, depth, signatures=signatures, docs=docs, code=code, imports=imports)
        if not result:
            print("Debug: get_info returned empty result")
            raise ImportError(f"Unable to inspect module: {module_or_class}")
    except Exception as e:
        print(f"Debug: Exception in get_info: {e}")
        raise ImportError(f"Error inspecting module: {module_or_class}")
    
    return result

def inspect_repo(repo_path, depth, signatures, docs, code, imports, all):
    
    try:
        sys.path.append(repo_path)
        module = import_module(repo_path)
    except ImportError as e:
        print(f"Error importing module {repo_path}: {e}")
        traceback.print_exc()
        return
    except AttributeError as e:
        print(f"Error accessing attribute {repo_path}: {e}")
        traceback.print_exc()
        return

    return get_info(module, depth, signatures, docs, code, imports, all)

# Example usage
@click.command("inspect")
@click.argument("module_or_class", type=click.STRING)
@click.option("--depth" , "-d", type=click.INT, default=0)
@click.option("--sigs", "-s", default=False, is_flag=True)
@click.option("--docs", "-doc", default=False, is_flag=True)
@click.option("--code", "-c", default=False, is_flag=True)
@click.option("--imports", "-imp", default=False, is_flag=True)
@click.option("--all", "-a", type=click.BOOL, is_flag=True)
@click.option("--markdown", "-md", default=False)
def inspect_cli(module_or_class, depth, sigs, docs, code, imports,all, markdown=False):
    """Inspect a Python module or class. Optionally specify the depth of inspection and the level of detail.

    Args:
        module_or_class (str): The name of the module or class to inspect.
        depth (int): The depth of inspection.
        signatures (bool): Include function signatures in the inspection.
        docs (bool): Include docstrings in the inspection.
        code (bool): Include source code in the inspection.
        imports (bool): Include imported modules in the inspection.
        mode (str): The level of detail to include in the inspection.
        markdown (bool): Return the inspection results as Markdown.
    """     
    return inspect_library(module_or_class, depth, sigs, docs, code, imports, all, markdown)

if __name__ == "__main__":
    inspect_cli()


