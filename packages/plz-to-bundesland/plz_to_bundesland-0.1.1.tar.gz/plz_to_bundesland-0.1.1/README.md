# PLZ to Bundesland Converter

This Python package converts German postal codes (PLZ, Postleitzahl) to their corresponding Bundesland (federal state). It can process individual PLZ inputs or bulk process PLZ data from Excel files.

## Installation

You can install the PLZ to Bundesland Converter using pip:

```
pip install plz-to-bundesland
```

## Usage

### As a Python Module

You can use the `get_bundesland` function in your Python scripts:

```python
from plz_to_bundesland import get_bundesland

bundesland = get_bundesland("10115")
print(bundesland)  # Output: Berlin
```

### Command-line Interface

The package also provides a command-line interface:

1. To convert a single PLZ:
   ```
   plz-to-bundesland -p 10115
   ```

2. To process an Excel file:
   ```
   plz-to-bundesland -f input.xlsx -o output.xlsx
   ```

## Input Excel File Format

The input Excel file should have the following format:

- The file must be in .xlsx format.
- It must contain a column named 'PLZ' (case-sensitive).
- The 'PLZ' column should contain the postal codes to be converted.
- Each PLZ should be in a separate row.

## Output

When processing an Excel file, the script will create a new Excel file with the following columns:
- All original columns from the input file
- A new 'Bundesland' column containing the corresponding federal state for each PLZ

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.