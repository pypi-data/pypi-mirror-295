from typing import List, Dict
import numpy as np
import easyocr
from tqdm.auto import tqdm
import pandas as pd

def get_cell_coordinates_by_row(table_data: List[Dict]) -> List[Dict]:
    """ Given bounding box of columns and rows, return cell coordinates by row.

    Args:
        table_data (List[Dict]): List of table data with bounding box information of columns and rows

    Returns:
        List[Dict]: List of cell coordinates by row.
    """
    # Extract rows and columns
    rows = [entry for entry in table_data if entry['label'] == 'table row']
    columns = [entry for entry in table_data if entry['label'] == 'table column']

    # Sort rows and columns by their Y and X coordinates, respectively
    rows.sort(key=lambda x: x['bbox'][1])
    columns.sort(key=lambda x: x['bbox'][0])

    # Function to find cell coordinates
    def find_cell_coordinates(row, column):
        cell_bbox = [column['bbox'][0], row['bbox'][1], column['bbox'][2], row['bbox'][3]]
        return cell_bbox

    # Generate cell coordinates and count cells in each row
    cell_coordinates = []

    for row in rows:
        row_cells = []
        for column in columns:
            cell_bbox = find_cell_coordinates(row, column)
            row_cells.append({'column': column['bbox'], 'cell': cell_bbox})

        # Sort cells in the row by X coordinate
        row_cells.sort(key=lambda x: x['column'][0])

        # Append row information to cell_coordinates
        cell_coordinates.append({'row': row['bbox'], 'cells': row_cells, 'cell_count': len(row_cells)})

    # Sort rows from top to bottom
    cell_coordinates.sort(key=lambda x: x['row'][1])

    return cell_coordinates

def apply_ocr(reader: easyocr.Reader,
              cropped_table: np.array, cell_coordinates: List[Dict]) -> List[pd.DataFrame]:
    """ Apply OCR to cell coordinates by row.

    Args:
        reader (easyocr.Reader): EasyOCR reader object
        cropped_table (np.array): Cropped table image in numpy array format
        cell_coordinates (List[Dict]): List of cell coordinates by row

    Returns:
        List[pd.DataFrame]: List of OCR results in DataFrame format
    """
    # let's OCR row by row
    data = dict()
    max_num_columns = 0
    for idx, row in enumerate(tqdm(cell_coordinates)):
      row_text = []
      for cell in row["cells"]:
        # crop cell out of image
        cell_image = np.array(cropped_table.crop(cell["cell"]))
        # apply OCR
        result = reader.readtext(np.array(cell_image))
        if len(result) > 0:
          # print([x[1] for x in list(result)])
          text = " ".join([x[1] for x in result])
          row_text.append(text)

      if len(row_text) > max_num_columns:
          max_num_columns = len(row_text)

      data[idx] = row_text

    print("Max number of columns:", max_num_columns)

    # pad rows which don't have max_num_columns elements
    # to make sure all rows have the same number of columns
    for row, row_data in data.copy().items():
        if len(row_data) != max_num_columns:
          row_data = row_data + ["" for _ in range(max_num_columns - len(row_data))]
        data[row] = row_data

    # convert to DataFrame
    data = pd.DataFrame.from_dict(data, orient='index')

    return data
