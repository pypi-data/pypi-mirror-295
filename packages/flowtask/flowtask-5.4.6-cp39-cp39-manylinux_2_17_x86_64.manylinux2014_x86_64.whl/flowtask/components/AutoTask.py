import math
import re
from urllib.parse import urljoin
import numpy as np
import orjson
import pandas as pd
from flowtask.components.abstract import DtComponent
from flowtask.components.interfaces.http import HTTPService
from flowtask.exceptions import ComponentError


def to_snake_case(s):
    """Converts a string to snake_case format.

    Args:
        name: The string to convert.

    Returns:
        The converted string in snake_case format.
    """
    # Remove unwanted characters
    s = re.sub(r"[^a-zA-Z0-9_\\s]", "", s)

    # Insert underscores before uppercase letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)

    # Replace remaining uppercase letters with underscores
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

class AutoTask(DtComponent, HTTPService):
    _credentials: dict = {"API_INTEGRATION_CODE": str, "USERNAME": str, "SECRET": str}

    async def start(self, **kwargs):
        self.headers = None
        self._proxies = None
        self.auth = ""
        self.auth_type = ""
        self.download = None
        self.timeout = 180
        self.accept = "application/json"
        self.query_json = self.mask_replacement_recursively(self.query_json)
        self.processing_credentials()

        self._base_url = (
            f"https://{self.zone}.autotask.net/atservicesrest/v1.0/{self.entity}/"
        )

        self.headers = {
            "Content-Type": "application/json",
            "ApiIntegrationCode": self.credentials["API_INTEGRATION_CODE"],
            "UserName": self.credentials["USERNAME"],
            "Secret": self.credentials["SECRET"],
        }

        self.ids_chunks = []
        if self.previous:
            self.data = self.input

            self.ids_chunks = self.filter_ids(
                id_field=self.id_column_name,
                items=self.data,
                chunk_size=500,
            )
        elif getattr(self, "ids", None):
            self._logger.info("Dropping specified Filters. Using ids instead.")
            self.ids_chunks = [self.ids]

        return True

    async def run(self):
        if not self.ids_chunks:
            # Use the Filter specified in the task
            df_items = await self.get_dataframe_from_entity(
                payload=orjson.dumps(self.query_json),
                id_column_name=self.id_column_name,
            )
        else:
            # Use the ids from the previous component or from the ids argument
            df_items = pd.DataFrame()
            for ids_chunk in self.ids_chunks:
                self.query_json.update(
                    {
                        "Filter": [
                            {"op": "in", "field": "id", "value": ids_chunk.tolist()}
                        ]
                    }
                )

                items = await self.get_dataframe_from_entity(
                    payload=orjson.dumps(self.query_json),
                    id_column_name=self.id_column_name,
                )

                df_items = pd.concat([df_items, items], ignore_index=True)

        if not df_items.empty and self.picklist_fields:
            df_picklist_values = await self.get_picklist_values(self.picklist_fields)

            if not getattr(df_picklist_values, "empty", True):

                for column in [to_snake_case(field) for field in self.picklist_fields]:
                    df_filtered = df_picklist_values[df_picklist_values['field'] == column]

                    # Merge the label into df_items
                    df_items = df_items.merge(
                        df_filtered[['label', 'value']],
                        how='left',
                        left_on=column,
                        right_on='value'
                    )
                    
                    # Rename the label column to reflect the original field
                    df_items.rename(columns={'label': f'{column}_label'}, inplace=True)
                    
                    # Drop the 'value' column from the merge
                    df_items.drop(columns=['value'], inplace=True)

        self._result = df_items
        return self._result

    async def close(self):
        pass

    def processing_credentials(self):
        if self.credentials:
            for value, dtype in self._credentials.items():
                try:
                    if type(self.credentials[value]) == dtype:
                        default = getattr(self, value, self.credentials[value])
                        val = self.get_env_value(
                            self.credentials[value], default=default
                        )
                        self.credentials[value] = val
                except (TypeError, KeyError) as ex:
                    self._logger.error(f"{__name__}: Wrong or missing Credentials")
                    raise ComponentError(
                        f"{__name__}: Wrong or missing Credentials"
                    ) from ex
                
    def filter_ids(self, id_field: str, items: pd.DataFrame, chunk_size):
        data = items[id_field].dropna().unique().astype(int)

        if data.size > 0:
            split_n = math.ceil(data.size / chunk_size)

            # Split into chunks of n items
            return np.array_split(data, split_n)  # Convert to NumPy array and split

        return [data]

    def get_autotask_url(self, resource):
        return urljoin(self._base_url, resource)

    async def get_dataframe_from_entity(self, payload, id_column_name):
        args = {
            "url": self.get_autotask_url("query"),
            "method": "post",
            "data": payload,
        }

        results = []
        while True:
            result, error = await self.session(**args)

            if error:
                self._logger.error(f"{__name__}: Error getting {self.entity}")
                raise ComponentError(f"{__name__}: Error getting {self.entity}") from error

            results.extend(result.get("items", []))

            args.update({"url": result["pageDetails"].get("nextPageUrl", None)})

            if not args["url"]:
                break

        df_results = await self.create_dataframe(results)

        if not df_results.empty and "userDefinedFields" in df_results.columns:
            df_results_udf = df_results["userDefinedFields"].apply(self.extract_udf)
            df_results = df_results.drop("userDefinedFields", axis=1, errors="ignore").join(df_results_udf)

        df_results = (
            df_results.rename(columns=lambda x: to_snake_case(x))
            .rename(columns={"id": id_column_name})
        )

        return df_results

    @staticmethod
    def extract_udf(row):
        """ Extracts dictionary values into columns"""
        return pd.Series({d['name']: d['value'] for d in row})

    async def get_picklist_values(self, field_names: list[str]) -> pd.DataFrame:
        result, error = await self.session(
            url=self.get_autotask_url("entityInformation/fields"),
            method="get",
        )

        if error:
            self._logger.error(f"{__name__}: Error getting {self.entity}")
            raise ComponentError(f"{__name__}: Error getting {self.entity}") from error

        picklist_data = []

        for field_name in field_names:
            for field in result["fields"]:
                if field["name"] == field_name:
                    self._logger.info(f"Extracting picking list values for {field_name}")

                    if not field["picklistValues"]:
                        df = pd.DataFrame(columns=["label", "value"])
                    else:
                        df = await self.create_dataframe(field["picklistValues"])
                        df = df[["label", "value"]]

                    df["field"] = to_snake_case(field_name)
                    picklist_data.append(df)

        # Concatenate all DataFrames and reset the index
        combined_df = pd.concat(picklist_data).reset_index(drop=True).astype({"value": "int"})
        return combined_df[["field", "label", "value"]]
