import typing
import csv

class MapperLocation:
    def __init__(self, csv_column_name: str=None, csv_column_position: int=None, column_name: str=None, coalesce_value: typing.Any=None, 
                 if_missing: str='ignore', if_column_missing: str='fail', convert_function: typing.Callable=None, pass_type=None):
        
        """Maps a specific location from a dict object to a DictCruncher "column"

        Args:
        csv_column_name (str): A specific column that already exists in the CSV file. Either this or csv_column_position must be specified.

        csv_column_position (int): A specific column position in a csv file. Either this or csv_column_name must be specified.

        column_name (str): a string column name to assign to a mapping.

        coalesce_value (Any): Default value if location is missing. Can be any type.
        
        if_missing (str): fail | ignore (default ignore). What to do if a mapping is missing.

        if_column_missing (str): fail | ignore (default fail). What to do if a named column is missing.

        delimiter (str): Delimiter to pass to csv library.

        convert_function (Callable): Function to apply on this value. This will also apply to a
            coalesce_value value.

        pass_type (Any): Value to return when using DictCruncher.get_column_types()

        Returns:
            MapperLocation object. This should be used as a 'table definition' eg:

            [
                MapperLocation(csv_column_name='CSV Column', column='id_number')
            ]
        """

        if column_name is None:
            raise ValueError('column_name must be defined.')

        if ((csv_column_name is not None) and (csv_column_position is not None)):
            raise ValueError('%s: Either csv_column_position or csv_column_name must be used. They both cannot be used at the same time.' % column_name)

        self.csv_column_name = csv_column_name
        self.csv_column_position = csv_column_position
        self.column_name = column_name
        self.coalesce_value = coalesce_value
        self.if_missing = if_missing
        self.if_column_missing = if_column_missing
        self.convert_function = convert_function
        self.pass_type = pass_type
        
        self.header_row = None

    def __str__(self):
        ident = f'"{self.csv_column_name}"' if self.csv_column_name is not None else f'csv_position: {self.csv_column_position}'
        return f"MapperLocation {ident} -> {self.column_name}"

    def _register_column_position(self, position: int):
        """Assigns a column positition to a MapperLocation mapper object.

        Args:
        
        position (int): The column position starting from 0 to get data from.

        TODO: This feels really janky, but think its better to have the 
            column position exist within the MapperLocation object for now.
        """

        self.csv_column_position = position
        
class RequiredElementMissingError(AttributeError):
    """Raised when a MapperLocation() value is missing AND if_missing is True    
    """
    pass

class CSVMapper:
    def __init__(self, filepath_or_buffer, mapper: list, has_headers=True, csv_delimiter: str=None, csv_quotechar: str=None, csv_newline=None, filepath_encoding='utf-8-sig'):
        """A library for cleaning up CSV columns without much heartache

        Args:
         filepath_or_buffer: Either a filename/path or a file handle

         mapper: A list of MapperLocation() objects defining how an exported record should look like. The order of elements in the list
            will be how they are exported.

         has_headers: Whether the csv has headers

         csv_delimiter (str): Delimiter to use on the file.

         csv_quotechar (str): Quote Character to use on file

         csv_newline (str): Newline to pass into csv module

         filepath_encoding (str): If passing in a filepath, the encoding (eg: utf-8). default is utf-8-sig
        """

        if isinstance(filepath_or_buffer, str):
            self.__in_file = open(filepath_or_buffer, 'r', encoding=filepath_encoding)

        elif hasattr(filepath_or_buffer, 'read'):
            self.__in_file = filepath_or_buffer

        else:
            raise IOError('Could not open file for reading.')

        csvfile_params = {
            'delimiter': csv_delimiter,
            'quotechar': csv_quotechar,
            'newline': csv_newline,
        }

        self.__csv_filtered_params = {k: v for k, v in csvfile_params.items() if v is not None}

        self.mapper = mapper

        self.has_headers = has_headers
        
        self._map_to_file()

    def _get_csvfile(self):
        """Get a csv.reader handler"""
        self.__in_file.seek(0)
        return csv.reader(self.__in_file, quoting = csv.QUOTE_ALL, **self.__csv_filtered_params)

    def _map_to_file(self):
        if self.has_headers:
            csvfile = self._get_csvfile()
            self.header_row = next(csvfile)
            
            for singlemapper in self.mapper:
                if singlemapper.csv_column_name is not None:
                    try:
                        mapped_position = self.header_row.index(singlemapper.csv_column_name)
                        singlemapper._register_column_position(mapped_position)

                    except ValueError:
                        if singlemapper.if_column_missing == 'ignore':
                            continue

                        raise ValueError('Unable to find the column "%s" in the input file. Found columns were %s' % (singlemapper.csv_column_name, str(self.header_row)))
        else:
            for singlemapper in self.mapper:
                if singlemapper.csv_column_name is not None:
                    raise ValueError('%s has a CSV header defined, but CSVMapper has has_header=False' % singlemapper)

    def to_records(self) -> typing.Generator:
        """Returns an iterable where each dict contains a row. Iterable is a generator
        
        Args:
            (Nothing)

        Returns:
            Iterable over each row

        Raises:
            RequriedElementMissingError - If MapperLocation's if_missing parameter is set to fail.
        """
        csvfile = self._get_csvfile()
        if self.has_headers:
            next(csvfile)

        for row in csvfile:
            out_row = {}
            
            for singlemapper in self.mapper:
                return_value = None

                if singlemapper.csv_column_position is not None:
                    return_value = row[singlemapper.csv_column_position]
                
                return_value = None if return_value == '' else return_value                    

                if return_value is None:
                    if singlemapper.if_missing == 'fail':
                        raise RequiredElementMissingError('Value is missing for column %s. row contains %s' % (singlemapper.coalesce_value, out_row))
                    elif singlemapper.coalesce_value is not None:
                        return_value = singlemapper.coalesce_value

                if singlemapper.convert_function is not None:
                    return_value = singlemapper.convert_function(return_value)

                out_row.update({singlemapper.column_name: return_value})
            yield out_row

    def to_dataframe(self):
        """Returns a pandas DataFrame with the converted data.
        
        Args:
            (Nothing)

        Returns:
            Pandas DataFrame

        Raises:
            ImportError: If pandas is not installed.
        """
        try:
            import pandas as pd
            return pd.DataFrame.from_records(self.to_records())

        except ImportError:
            raise ImportError('Must have pandas installed in order to use this function.')
        