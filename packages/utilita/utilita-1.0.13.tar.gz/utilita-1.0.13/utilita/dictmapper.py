import json
# Expect: list of json objects.
import re
import typing

class MapperLocation:
    def __init__(self, location, column_name, coalesce_value=None, if_missing='ignore', attempt_json_serializing=True, delimiter='::',  convert_function=None, pass_type=None):
        """
        if_missing = str: fail | ignore | drop (default ignore)
        """
        self.location = location
        self.column_name = column_name
        self.coalesce_value=coalesce_value
        self.if_missing=if_missing
        self.attempt_json_serializing=True
        self.delimiter=delimiter
        self.convert_function=convert_function
        self.pass_type = pass_type
        
class RequiredElementMissingError(AttributeError):
    pass

class DictMapper:
    def __init__(self, in_dict_list: list, mapper: dict) -> None:
        """Creates a DictMapper instance. Use get_records() to get mapped records.

        Args:
         in_dict_list: A list of dicts to iterate over

         mapper: A dict of MapperLocation() objects defining how an exported record should look like. dict name should be the 'table_name'
            eg: {'output_table': [MapperLocation().....]}
        """
        self.in_dict_list = [d for d in in_dict_list]
        self.mapper = mapper
        self.table_names = [key for key in mapper]
        self.total_records = len(self.in_dict_list)

        self.__re_check_list_base_location = r"^.+(?=\[\])"
        self.__re_check_list_specific_element = r"[a-zA-Z]+\[[0-9]+\]"
        self.__re_check_list_unlimited_element = r"[a-zA-Z]+(?=\[\])"
        self.__re_list_location_name = r"[a-zA-Z]+(?=\[)"
        self.__re_list_location_index = r"(?<=\[)[0-9]+(?=\])"


    def get_records(self, table_name: str=None, extra_data=None) -> list:
        """ Gets the transformed flattened records.

        Args:
         table_name: 

         extra_data:

         Returns:
          A list of records that were flattened from the original json data.
        
        """
        if extra_data is None:
            extra_data = {}

        if table_name in self.table_names:
            return self._dump_to_records(in_rows=self.in_dict_list, mapper_set=self.mapper.get(table_name), extra_data=extra_data)
        else:
            raise ValueError(f'{table_name} is not defined in mapper. We got {self.table_names}')
        
    def get_column_types(self, table_name: str=None) -> dict:

        if table_name in self.table_names:
            mapper_list = self.mapper.get(table_name)
            
            mapper_return = {}
            for mapper in mapper_list:
                if mapper.pass_type is not None:
                    mapper_return.update({mapper.column_name: mapper.pass_type})

            return mapper_return
        else:
            raise ValueError(f'{table_name} is not defined in mapper. We got {self.table_names}')

    def auto_flatten_records(self, prefix: str=str(), stringify_list=False, force_lowercase=False) -> typing.Generator:
        for in_dict in self.in_dict_list:
            yield self._flatten_single_dict(root_dict=in_dict, prefix=prefix, stringify_list=stringify_list, force_lowercase=force_lowercase)

    def _flatten_single_dict(self, root_dict: dict, prefix: str=str(), stringify_list=False, force_lowercase=False) -> dict:
        """Takes a nested dictionary and "flattens" it into a single level key:value set. Object children in elements will have a prefix

        Eg: flatten_dict({"a": {"b": {"c": 1}}) == {"a_b_c": 1}
        
        root_dict: input dict

        prefix: str = name to append to returned elements    

        stringify_list: bool = False = If we encounter a list object, do we stringify it or leave it be?

        force_lowercase: bool = False = Force keys to lowercase (including prefix)

        Returns:
        dict = flattened object
        """

        root_dict = root_dict.copy()
        flattened = {}

        for k, v in root_dict.items():
            new_key = f"{prefix}{k}"
            new_key = new_key.lower() if force_lowercase else new_key
            
            # Take in any types that are not nested dictionaries.
            if type(v) not in [dict, list]:
                flattened.update({new_key: v})
            elif type(v) == dict:
                flattened.update(self._flatten_single_dict(root_dict=v, prefix=new_key + '_', force_lowercase=force_lowercase))
            # Only list should exist here.
            elif type(v) == list:
                # warnings.warn(f'{new_key} is a list')
                if stringify_list == True:
                    flattened.update({new_key: json.dumps(v)})
                else:
                    flattened.update({new_key: v})

        return flattened
    
    def _expand_dict(self, in_dict):
        flat_list = []
        row_was_expanded = False
        for k, v in in_dict.items():
            if type(v) == list:
                for row in v:
                    subroot = in_dict.copy()
                    subdata = self._flatten_single_dict(row, prefix=f'{k}_')
                    subroot.update(subdata)
                    # in_dict = subroot.copy()
                    del subroot[k]
                    flat_list.append(subroot)
                    row_was_expanded = True

        if not row_was_expanded:
            flat_list.append(in_dict)

    def _dump_single_row(self, in_row: list, mapper_set: list, extra_data: dict=None, extra_data_in_front:bool=False, ignore_location_str: str=None):
        extra_data = {} if extra_data is None else extra_data
        
        output_row = {}
        
        if len(mapper_set) == 0:
            # In the event we only are expecting to loop through subrows
            return output_row
        
        # Supposed to be a parent attribute eg {"id": "foo", "tags": ["tag_name": "bar"]}
        if extra_data_in_front:
            output_row.update(extra_data)
        
        first_column = next(iter(mapper_set)).column_name

        # for column, location in column_set.items():
        for mapperlocation in mapper_set:
            column = mapperlocation.column_name
            location = mapperlocation.location
            delimiter = mapperlocation.delimiter
            convert_function = mapperlocation.convert_function
            coalesce_value = mapperlocation.coalesce_value

            if convert_function is not None:
                coalesce_value = convert_function(coalesce_value)

            # Hack to remove unneeded location string as we now have no reference to it.
            if ignore_location_str is not None:
                # ignore_location_str = ignore_location_str #+ f'[]{mapperlocation.delimiter}'
                location = location.replace(ignore_location_str, '')

            # If we only need to pull a single element.
            try:
                location_elements = location.split(delimiter)

                if location_elements[0] == 'root' and len(location_elements) == 1:
                    if convert_function is not None:
                        in_row = convert_function(in_row)

                    output_row.update({column: in_row})

                current_object = in_row
                
                for single_location in location_elements:
                    # Ignore the root element
                    if single_location == 'root':
                        continue

                    # If we specify we want just the first element in a list eg: payments[0].get('key')
                    if re.match(self.__re_check_list_specific_element, single_location):
                        location_name = re.search(self.__re_list_location_name, single_location).group()
                        location_index = int(re.search(self.__re_list_location_index, single_location).group())
                        try:
                            current_object = current_object.get(location_name)[location_index]
                        except IndexError:
                            # print(f'Warning: indexerror {location_name}[{location_index}] does not exist in {location}. First column is {first_column}, data is {output_row.get(first_column)}')
                            if mapperlocation.if_missing == 'fail':
                                raise RequiredElementMissingError(f'Required element {location_name}[{location_index}] does not exist in {location}. First column is {first_column}, data is {output_row.get(first_column)}')
                            if mapperlocation.if_missing == 'drop':
                                # print('dropping row')
                                return None
                            else:
                                output_row.update({column: mapperlocation.coalesce_value})
                                break
                        
                    else:
                        if not hasattr(current_object, 'get') and isinstance(current_object, str) and mapperlocation.attempt_json_serializing:
                            try:
                                current_object = json.loads(current_object)
                            except json.decoder.JSONDecodeError:
                                if isinstance(current_object, str):
                                    output_row.update({column: current_object})
                                    break
                            
                        current_object = current_object.get(single_location)
                        if current_object is None:
                            # print(f'Warning: elementnotfound {single_location} does not exist in {location}. First column is {first_column}, data is {output_row.get(first_column)}')
                            if mapperlocation.if_missing == 'fail':
                                raise RequiredElementMissingError(f'Required element {single_location} does not exist in {location}. First column is {first_column}, data is {output_row.get(first_column)}')
                            elif mapperlocation.if_missing == 'drop':
                                # print(f'dropping row')
                                return None
                            else:
                                output_row.update({column: mapperlocation.coalesce_value})
                                break
                        
                    output_row.update({column: current_object})
                
                if convert_function is not None:
                    output_row[column] = convert_function(output_row[column])

            except AttributeError:
                # print(f'Warning: attributeerror {single_location} does not exist in {location}. First column is {first_column}, data is {output_row.get(first_column)}')
                if mapperlocation.if_missing == 'fail':
                    raise RequiredElementMissingError(f'Required element {single_location} does not exist in {location}. First column is {first_column}, data is {output_row.get(first_column)}')
                
                elif mapperlocation.if_missing == 'drop':
                    # print('dropping row')
                    return None

                else:
                    output_row.update({column: mapperlocation.coalesce_value})
                    continue

        if not extra_data_in_front:
            output_row.update(extra_data)
        
        return output_row

    def _dump_to_records(self, in_rows, mapper_set, extra_data=None):
        if extra_data == None:
            extra_data = {}

        out_rows = []
        
        nested_list_mapper_set = []
        nested_list_base_location = set()

        single_mapper_set = []

        for mapper in mapper_set:
            if re.search(self.__re_check_list_unlimited_element, mapper.location):
                nested_list_mapper_set.append(mapper)
                nested_list_base_location.add(re.match(self.__re_check_list_base_location, mapper.location).group())
                nested_list_base_location_delimiter = mapper.delimiter
            else:
                single_mapper_set.append(mapper)

        if len(nested_list_base_location) > 1:
            raise AttributeError(f"This library does not currently supported multiple listed mappers in a single instance. Sorry. We found {nested_list_base_location}")

        if len(nested_list_base_location) > 0:
            nested_list_base_location = next(iter(nested_list_base_location))
            nested_list_base_location_elements = nested_list_base_location.split(nested_list_base_location_delimiter)
            nested_list_base_location = nested_list_base_location + f'[]{nested_list_base_location_delimiter}'

        # feeds in the raw JSON row, and outputs a flattened record
        for row in in_rows:
            output_row = self._dump_single_row(in_row=row, mapper_set=single_mapper_set, extra_data=extra_data)

            if len(nested_list_base_location) > 0:
                output_nested_rows = []
                nested_rows = row.copy()
                for element in nested_list_base_location_elements:
                    if element == 'root':
                        continue
                    else:
                        nested_rows = nested_rows.get(element, {})
                        nested_rows = nested_rows if nested_rows is not None else {}

                if len(nested_rows) == 0:
                    nested_row = self._dump_single_row(in_row={}, mapper_set=nested_list_mapper_set, extra_data=output_row, extra_data_in_front=True, ignore_location_str=nested_list_base_location)
                    if nested_row is None:
                        continue
                    
                    output_nested_rows.append(nested_row)

                else:
                    for nested_row in nested_rows:
                        if nested_row is None:
                            continue
                        output_nested_rows.append(self._dump_single_row(in_row=nested_row, mapper_set=nested_list_mapper_set, extra_data=output_row, extra_data_in_front=True, ignore_location_str=nested_list_base_location))
                
                for r in output_nested_rows:
                    # These are bad hacks, but i want to go home.
                    if r is None:
                        continue
                    out_rows.append(r)

                if len(output_nested_rows) == 0 and output_row is not None and len(output_row) != 0:
                    out_rows.append(output_row)

            else:
                if output_row is not None and len(output_row) != 0:
                    out_rows.append(output_row)

        return out_rows