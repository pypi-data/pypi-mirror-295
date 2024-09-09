from click.testing import CliRunner
from minspect.main import cli, generate_markdown, generate_panels
from rich.console import Console
from io import StringIO

def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ["minspect", "--depth", "1"])
    assert result.exit_code == 0
    assert "minspect" in result.output

def test_cli_with_options():
    runner = CliRunner()
    result = runner.invoke(cli, ["minspect", "--depth", "1", "--sigs", "--docs"])
    assert result.exit_code == 0
    assert "minspect" in result.output
    assert "Signature:" in result.output
    assert "Docstring:" in result.output
    assert "Type:" in result.output
    assert "Path:" in result.output

def test_cli_with_sigs():
    runner = CliRunner()
    result = runner.invoke(cli, ["minspect", "--sigs"])
    assert result.exit_code == 0
    assert "Debug: sigs=True, docs=False, code=False, imports=False, all=False" in result.output
    assert "Debug: Result keys:" in result.output

def test_cli_with_docs():
    runner = CliRunner()
    result = runner.invoke(cli, ["minspect", "--docs"])
    assert result.exit_code == 0
    assert "Debug: sigs=False, docs=True, code=False, imports=False, all=False" in result.output
    assert "Debug: Result keys:" in result.output

def test_cli_with_code():
    runner = CliRunner()
    result = runner.invoke(cli, ["minspect", "--code"])
    assert result.exit_code == 0
    assert "Debug: sigs=False, docs=False, code=True, imports=False, all=False" in result.output
    assert "Debug: Result keys:" in result.output

def test_cli_with_all():
    runner = CliRunner()
    result = runner.invoke(cli, ["minspect", "--all"])
    assert result.exit_code == 0
    assert "Debug: sigs=True, docs=True, code=True, imports=True, all=True" in result.output
    assert "Debug: Result keys:" in result.output

def test_cli_with_markdown():
    runner = CliRunner()
    result = runner.invoke(cli, ["minspect", "--markdown"])
    assert result.exit_code == 0
    assert "# Inspection Result" in result.output
    assert "**Type:**" in result.output
    assert "**Path:**" in result.output

def test_cli_with_multiple_options():
    runner = CliRunner()
    result = runner.invoke(cli, ["minspect", "--depth", "2", "--sigs", "--docs", "--code"])
    assert result.exit_code == 0
    assert "Signature:" in result.output
    assert "Docstring:" in result.output
    assert "Source Code:" in result.output

def test_cli_with_invalid_module():
    runner = CliRunner()
    result = runner.invoke(cli, ["nonexistent_module"])
    print(f"Debug: CLI output:\n{result.output}")
    print(f"Debug: Exit code: {result.exit_code}")
    assert result.exit_code == 1, f"Expected exit code 1, but got {result.exit_code}"
    assert "Error: Module 'nonexistent_module' not found." in result.output, "Expected error message not found in output"

def test_cli_with_valid_module():
    runner = CliRunner()
    result = runner.invoke(cli, ["minspect"])
    assert result.exit_code == 0
    assert "minspect" in result.output

def test_generate_markdown():
    result = {
        'test_function': {
            'type': 'function',
            'path': 'test.module.test_function',
            'signature': 'def test_function(arg1, arg2)',
            'docstring': 'This is a test function',
            'code': 'def test_function(arg1, arg2):\n    pass'
        }
    }
    md_content = generate_markdown(result, True, True, True)
    assert "# Inspection Result" in md_content
    assert "## test_function" in md_content
    assert "**Type:** function" in md_content
    assert "**Path:** test.module.test_function" in md_content
    assert "**Signature:**" in md_content
    assert "**Docstring:**" in md_content
    assert "**Source Code:**" in md_content

def test_generate_panels():
    console = Console(file=StringIO())
    result = {
        'test_function': {
            'type': 'function',
            'path': 'test.module.test_function',
            'signature': 'def test_function(arg1, arg2)',
            'docstring': 'This is a test function',
            'code': 'def test_function(arg1, arg2):\n    pass'
        }
    }
    generate_panels(console, result, True, True, True)
    output = console.file.getvalue()
    assert "test_function" in output
    assert "Type: function" in output
    assert "Path: test.module.test_function" in output
    assert "Signature:" in output
    assert "Docstring:" in output
    assert "Source Code:" in output

# Add more tests for other combinations as needed
