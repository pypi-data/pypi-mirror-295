import datetime
import decimal

from chainalysis.util_functions.check_list_type import get_list_type
from chainalysis.util_functions.exceptions import BadRequest


class Stringify:
    """
    This class contains functions to transform python objects
    into formatted string params so they can be used to query
    Data Solutions' databases without needing to be transformed
    manually by the user.
    """

    def lists(self, _list: list) -> str:
        """
        Convert a list to a formatted string param.

        :param list: The list to be converted.
        :type list: list

        :raises Exception: Raises an exception if a list type is not submitted.
        :raises Exception: If lists do not contain the right types.
        :return: The converted list.
        :rtype: str
        """

        if not isinstance(_list, list):
            raise BadRequest(
                "Incorrect type. Supply a list.",
            )

        type = get_list_type(_list)

        if type == int or type == bool or type == float or type == decimal:
            return f"({', '.join(map(str, _list))})"

        if type == str:
            result = "("

            for i, element in enumerate(_list):
                if i > 0:
                    result += ", "
                result += f"'{element}'"

            result += ")"
            return result

    def columns(self, columns: list) -> str:
        """
        Convert a column select list to a formatted string param.

        :param list: The column select list object to be converted.
        :type list: list

        :return: The converted column select list.
        :rtype: str
        """
        type = get_list_type(columns)
        if type != str:
            raise BadRequest("Columns must be a string list")
        return ", ".join(columns)

    def datetimes(self, _datetime: datetime.datetime) -> str:
        """
        Convert a datetime object to a formatted string param.

        :param list: The datetime object to be converted.
        :type list: list

        :return: The converted datetime object.
        :rtype: str
        """

        if not isinstance(_datetime, datetime.datetime):
            raise BadRequest("Incorrect type. Supply a datetime.datetime object.")

        return f"'{_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')}'"
