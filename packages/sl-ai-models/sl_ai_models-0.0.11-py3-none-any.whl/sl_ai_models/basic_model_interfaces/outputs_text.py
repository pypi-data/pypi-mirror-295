from typing import Any, get_args, get_origin
import logging
logger = logging.getLogger(__name__)
from abc import ABC
from sl_ai_models.basic_model_interfaces.ai_model import AiModel
import json
from sl_ai_models.utils.ai_misc import try_function_till_tries_run_out, validate_complex_type, strip_code_block_markdown
from typing import TypeVar
from pydantic import BaseModel
import ast
import re
T = TypeVar('T')


class OutputsText(AiModel, ABC):

    async def invoke_and_return_verified_type(self, input: Any, normal_complex_or_pydantic_type: type[T], allowed_invoke_tries_for_failed_output: int = 3) -> T:
        """
        Input should ask for the type of resulting object you want with no other words around it
        Retries if an invalid format is given

        ## Handles
        - normal types (e.g. str, int, list, dict, bool, union)
        - complex types (e.g. list[str], dict[str, int], list[tuple[dict,int]], etc.)
        - Pydantic model or list of models (e.g. MyPydanticModel, list[MyPydanticModel], but not list[tuple[MyPydanticModel,int]])

        ## Example
        Prompt: Give me a list of recipe ideas as a list of string

        Type asked for: list[str]

        AI Returns:


            [
            "recipe idea 1",
            "recipe idea 2"
            ]


        Function Returns: list[str] containing ["recipe idea 1", "recipe idea 2"]
        """
        return await try_function_till_tries_run_out(allowed_invoke_tries_for_failed_output, self.__invoke_and_transform_to_type, input, normal_complex_or_pydantic_type)



    async def invoke_and_unsafely_run_and_return_generated_code(self, input: Any, expected_output_type: type[T], allowed_invoke_tries_for_failed_output: int) -> tuple[T,str]:
        """
        Input should ask for a code block with no other words around it
        The code block should assign the return value to a variable called 'final_result'
        Returns the code output as a string and the final result as the expected output type
        """
        return await try_function_till_tries_run_out(allowed_invoke_tries_for_failed_output, self.__invoke_and_unsafely_run_generated_code, input, expected_output_type)


    async def __invoke_and_transform_to_type(self, input: Any, normal_complex_or_pydantic_type: type[T]) -> T:
        response: str = await self.invoke(input)
        cleaned_response = strip_code_block_markdown(response.strip())
        try:
            transformed_response = self.transform_response_to_type(cleaned_response, normal_complex_or_pydantic_type)
        except Exception as e:
            raise ValueError(f"Error transorming response to type {normal_complex_or_pydantic_type}: {e}. Response was: {cleaned_response}")
        if not validate_complex_type(transformed_response, normal_complex_or_pydantic_type):
            raise TypeError(f"Model did not return {normal_complex_or_pydantic_type}. Output was: {cleaned_response}")
        return transformed_response




    @classmethod
    def transform_response_to_type(cls, response: str, normal_complex_or_pydantic_type: type[T]) -> T:
        outer_type = get_origin(normal_complex_or_pydantic_type)
        inner_types = get_args(normal_complex_or_pydantic_type)

        try:
            is_list = (outer_type == list)
            is_list_of_pydantic_models = is_list and issubclass(inner_types[0], BaseModel)
        except TypeError:
            is_list_of_pydantic_models = False

        try:
            is_pydantic_model = issubclass(normal_complex_or_pydantic_type, BaseModel)
        except TypeError:
            is_pydantic_model = False

        if is_list_of_pydantic_models:
            pydantic_model_type: type[BaseModel] = inner_types[0]
            list_of_validated_objects: list[BaseModel] = []
            list_of_dicts_from_response = json.loads(response)
            for item in list_of_dicts_from_response:
                pydantic_object = pydantic_model_type.model_validate(item)
                list_of_validated_objects.append(pydantic_object)
            final_response = list_of_validated_objects
        elif is_pydantic_model:
            assert issubclass(normal_complex_or_pydantic_type, BaseModel)
            model_as_json = json.loads(response)
            response_as_model = normal_complex_or_pydantic_type.model_validate(model_as_json)
            final_response = response_as_model
        else:
            final_response = cls.__turn_string_into_non_pydantic_python_data_structure(response)

        assert validate_complex_type(final_response, normal_complex_or_pydantic_type)
        return final_response # type: ignore <- validate_complex_type checks this, but mypy doesn't pick it up


    async def __invoke_and_unsafely_run_generated_code(self, input: Any, expected_output_type: type[T]) -> tuple[T,str]:
        model_response = await self.invoke(input)
        code = strip_code_block_markdown(model_response)

        global_vars = {
            '__builtins__': __builtins__  # Allow access to standard libraries
        }
        local_vars = {}

        try:
            exec(code, global_vars, local_vars)
        except Exception as e:
            raise RuntimeError(f"Error executing code: {e}. Code was {code}")

        evaluated_answer = local_vars.get('final_result')
        if evaluated_answer is None:
            raise ValueError(f"Code did not assign anything to final_result. Code was {code}")

        if not validate_complex_type(evaluated_answer, expected_output_type):
            raise TypeError(f"Code run did not return {expected_output_type}. Output was: {evaluated_answer}")

        return evaluated_answer, code


    @classmethod
    def __turn_string_into_non_pydantic_python_data_structure(cls, response: str) -> Any:
        if response == "[]" or response == "" or response == "[\"\"]" or response == "['']":
            return []

        try:
            response_loaded_as_string = json.loads(response)
        except json.JSONDecodeError as e1:
            try:
                response_loaded_as_string = ast.literal_eval(response)
            except Exception as e2:
                try:
                    response_loaded_as_string = cls.__extract_json_from_text(response)
                except Exception as e3:
                    raise ValueError(f"Model did not return a parsable value. Error1: {e1}, Error2: {e2}, Error3: {e3}, response: {response}")

        return response_loaded_as_string


    @staticmethod
    def __extract_json_from_text(text: str) -> dict | list:
        json_match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            json_loaded = json.loads(json_string)
            return json_loaded
        else:
            raise ValueError(f"No JSON found in the text")


    @staticmethod
    def get_schema_format_instructions_for_pydantic_type(pydantic_type: type[BaseModel]) -> str:
        # Copy schema to avoid altering original Pydantic schema.
        schema = {k: v for k, v in pydantic_type.model_json_schema().items()}

        reduced_schema = schema
        if "title" in reduced_schema:
            del reduced_schema["title"]
        if "type" in reduced_schema:
            del reduced_schema["type"]
        schema_str = json.dumps(reduced_schema)

        return _PYDANTIC_FORMAT_INSTRUCTIONS.format(schema=schema_str)



_PYDANTIC_FORMAT_INSTRUCTIONS = """
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

Here is the output schema:
```
{schema}
```

Make sure to return an instance of the JSON (no other words, preface, or conclusion). Do not return the schema itself.
"""