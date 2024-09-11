from querysource.exceptions import DataNotFound as QSNotFound
from ..exceptions import ComponentError, DataNotFound
from .QSBase import QSBase

class Populartimes(QSBase):
    type = "by_placeid"
    _driver = "populartimes"

    async def by_placeid(self):
        result = []
        try:
            
            for index, row in self.data.iterrows():
                self._qs.place_id = row['place_id']
                resultset = await self._qs.by_placeid()
                # Convert array into dictionary
                rts = {}
                for component in resultset["address_components"]:
                    key = component["types"][0]
                    value = component["long_name"]
                    rts[key] = value
                resultset["address_components"] = rts
                result.append(resultset)
            return result
        except QSNotFound as err:
            raise DataNotFound(f"Populartimes Not Found: {err}") from err
        except Exception as err:
            self._logger.exception(err)
            raise ComponentError(f"Populartimes ERROR: {err!s}") from err
