import logging
import time
from pathlib import Path

import click
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown as RichMarkdown

logger = logging.getLogger(__name__)

class Markdown:
    """Stream formatted JSON-like text to the terminal with live updates."""
    
    def __init__(self, data=None, mdargs=None, style="default", save=None):
        logger.debug(f"Initializing Markdown with data: {data}")
        self.data = data or {}

        self.mdargs = mdargs or {}
        self.style = style
        self.console = Console(style=self.style,force_terminal=True)
        self.save = save
        self.lines = [data] if isinstance(data, str  | dict) else data


    def generate_markdown(self, data=None, depth=0):
        """Generate Markdown from JSON with headers based on depth."""
        data = data if data is not None else self.data
        markdown_lines = []
        indent = "  " * (depth)  # Reduce indent by one level

        if isinstance(data, dict):
            for key, value in data.items():
                if key == "name":
                    markdown_lines.append(f"\n{indent}{'#' * (max(1, depth))} {value.rstrip()}\n")
                    continue
                if key.strip().startswith("#"):
                    markdown_lines.append(f"{indent}{'#' * (max(1,depth))} {key.rstrip('#').strip()}\n")
                    markdown_lines.extend(self.generate_markdown(value, depth + 1))
                    continue
                if any("type" in key for key in data) and any("content" in key for key in data):
                    # markdown_lines.append(f"\n{indent}{'# ' * (depth+1)} {data}
                    markdown_lines.append("```python")
                    markdown_lines.extend(data['content'].split('\n'))
                    markdown_lines.append("```")  # Ensure the code block is closed
                    break
                elif isinstance(value, (dict, list)):
                    markdown_lines.extend(self.generate_markdown(value, depth + 1))
                else:
                    print(f"{key}: {value}")

                    markdown_lines.append(f"{indent}{'- **' + key + '**: ' + str(value)}" if key.strip() else f"{indent}{str(value)}")
        elif isinstance(data, list):
            for item in data:
                markdown_lines.extend(self.generate_markdown(item, depth + 1))
        elif isinstance(data, str):
            for line in data.split("\n"):
                markdown_lines.append(f"{indent}{line}")
        
        return markdown_lines

    def generate_markdown(self, data=None, depth=0):
        """Generate Markdown from JSON with headers based on depth."""
        data = data if data is not None else self.data
        markdown_lines = []
        indent = "  " * min(depth, 3)  # Control indent level based on depth

        if isinstance(data, dict):
            for key, value in data.items():
                # Handle 'name' as a header
                if key == "name":
                    markdown_lines.append(f"\n{indent}{'#' * max(1, depth)} {value.rstrip()}\n")
                    continue

                # Handle Markdown-style keys
                if key.strip().startswith("#"):
                    markdown_lines.append(f"{indent}{'#' * max(1, depth)} {key.rstrip('#').strip()}\n")
                    markdown_lines.extend(self.generate_markdown(value, depth + 1))
                    continue

                # Handle code block content
                if any("type" in key for key in data) and any("content" in key for key in data):
                    markdown_lines.append("```python")
                    markdown_lines.extend( [" " * depth + c for c in data['content'].split('\n')])
                    markdown_lines.append("```")
                    break

                # Handle nested dictionaries and lists
                elif isinstance(value, (dict, list)):
                    markdown_lines.extend(self.generate_markdown(value, depth + 1))

                else: 
                    # print(f" " * depth + f"{key}: {value}, depth: {depth}")
                    markdown_lines.append(f"{indent}- **{key}**: {str(value).strip()}\n")
                        
        elif isinstance(data, list):
            for item in data:
                markdown_lines.extend(self.generate_markdown(item, depth + 1))

        elif isinstance(data, str):
            for line in data.split("\n"):
                markdown_lines.append(f"{indent}{line}")

        return markdown_lines
    
    def update(self, renderable: "RenderableType", *, refresh: bool = False) -> None:
        """Update the renderable that is being displayed.

        Args:
            renderable (RenderableType): New renderable to use.
            refresh (bool, optional): Refresh the display. Defaults to False.
        """
        self.live.update(renderable)

        if isinstance(renderable, str):
            renderable = self.live.console.render_str(renderable)
            self.live._renderable = renderable
            if refresh:
                self.live.refresh()
    def stream(self, depth=0):
        """Stream the markdown content with live updates."""
        logger.debug(f"Streaming with depth: {depth}")
        if not self.data:
            logger.warning("No data to display.")
            return
        print(f"lines: len({len(self.data)})")
        # Generate the entire markdown content first
        markdown_content = self.generate_markdown(self.data, depth)


        lines = []
        # Update the live view only once after generating all markdown content
        live = Live(console=self.console,vertical_overflow="visible", auto_refresh=True)
        tic = time.time()
        timeout = 5
        tic = time.time()
        with live as live:
            
            if time.time() - tic > timeout:
                live.auto_refresh = False
                tic = time.time()
            for line in markdown_content:
                lines.append(line)
                line = "\n".join(lines)
                
                live.update(RichMarkdown(line, **self.mdargs, justify="left", code_theme="github-light"))
                # tic = time.time()
                # while time.time() - tic < 0.1:
                #     pass
                time.sleep(0.1)
            # self.live.update(RichMarkdown(markdown_content, **self.mdargs, justify="left", style="magenta on white", code_theme="github-light"))    
            
        # Optional small delay for effect


        if self.save:
            Path(self.save).write_text(markdown_content)
            logger.info(f"Markdown content saved to {self.save}")
def recursive_read(file, include=None):
    include = include or {".json", ".md", ".txt", ".yaml", ".toml", ".py"}
    data = {}
    file_path = Path(file)
    if file_path.is_file() and file_path.suffix in include and "__pycache__" not in str(file_path):
        logger.info(f"Reading file: {file_path}")
        content = file_path.read_text()
        if file_path.suffix == '.py':
            data[str(file_path)] = {'type': 'python', 'content': content}
        else:
            data[str(file_path)] = content
    elif file_path.is_dir():
        for sub_path in file_path.iterdir():
            data.update(recursive_read(sub_path, include))
    return data

@click.command("mdstream")
@click.argument("file", type=click.Path(exists=True))
@click.option("--depth", "-d", default=0, help="Depth of headers")
@click.option("--save", "-s", help="Save markdown content to a file")
def cli(file, depth, save):
    """Stream markdown content from a file."""
    data = recursive_read(file)
    md = Markdown(data=data, save=save)
    md.stream(depth=depth)

def example():
    nested_data = {
        "name": "Example Package",
        "version": "1.0.0",
        "description": "This is a deeply nested structure.",
        "dependencies": [
            {
                "name": "Dependency 1",
                "version": "2.0.0",
                "sub_dependencies": [
                    {
                        "name": "Sub-dependency A",
                        "version": "2.1.1",
                        "details": {
                            "maintainer": "John Doe",
                            "license": "MIT"
                        }
                    },
                    {
                        "name": "Sub-dependency B",
                        "version": "2.1.2",
                        "details": {
                            "maintainer": "Jane Smith",
                            "license": "Apache-2.0"
                        }
                    }
                ]
            },
            {
                "name": "Dependency 2",
                "version": "3.0.0",
                "sub_dependencies": [
                    {
                        "name": "Sub-dependency C",
                        "version": "3.1.0",
                        "details": {
                            "maintainer": "Alice Brown",
                            "license": "GPL-3.0"
                        }
                    }
                ]
            }
        ],
        "urls": {
            "Homepage": "https://example.com",
            "Repository": "https://github.com/example/package"
        }
    }

    md = Markdown(data=nested_data)
    md.stream()

if __name__ == "__main__":
    example()
