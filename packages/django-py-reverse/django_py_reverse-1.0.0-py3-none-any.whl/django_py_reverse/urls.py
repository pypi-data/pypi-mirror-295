import re


class Urls:
    def __init__(self, data, url_prefix="", include_js_style=False):
        # type: (dict[str, list[list[str]]], str, bool) -> None
        """
        Initializes the Urls class with the provided data.

        Args:
            data (dict): Dictionary containing 'urls' and 'prefix' keys.
                         'urls' should be a list of URL patterns, and 'prefix'
                         is the common prefix for all URLs.
        """
        self.url_patterns = data["urls"]
        self.url_prefix = url_prefix or data["prefix"]
        if not self.url_prefix.endswith("/"):
            self.url_prefix += "/"
        self.self_url_patterns = {}
        self.urls = {}
        self.include_js_style = include_js_style

    def _get_url(self, url_pattern: str) -> callable:
        """
        Generates a function that can construct URLs based on the given URL pattern.

        Args:
            url_pattern (str): Name of the URL pattern.

        Returns:
            function: A function that accepts keyword arguments corresponding to URL pattern parameters
                      and returns the constructed URL.
        """

        def url_function(**kwargs: dict[str, str]) -> str or None:
            """
            Constructs a URL based on the provided keyword arguments.

            Args:
                **kwargs: Keyword arguments corresponding to URL pattern parameters.

            Returns:
                str: The constructed URL.
            """
            ref_list = self.self_url_patterns[url_pattern]

            for ref in ref_list:
                # Check if the number and names of provided keys match the URL pattern
                if len(ref[1]) == len(kwargs) and all(arg in kwargs for arg in ref[1]):
                    url = ref[0]
                    for url_arg, url_arg_value in kwargs.items():
                        if url_arg_value is None or url_arg_value is None:
                            url_arg_value = ""
                        else:
                            url_arg_value = str(url_arg_value)
                        url = url.replace("%(" + url_arg + ")s", url_arg_value)

                    return f"{self.url_prefix}{url}"

            # Can't find a match
            return None

        return url_function

    def factory(self) -> dict[str, callable]:
        """
        Creates URL functions for each URL pattern and populates the Urls dictionary.
        """
        for name, pattern in self.url_patterns:
            self.self_url_patterns[name] = pattern
            url_function = self._get_url(name)

            # Add URL function to the Urls dictionary with different keys
            if self.include_js_style:
                self.urls[
                    re.sub(r"[-_]+(.)", lambda m: m.group(1).upper(), name)
                ] = url_function
            self.urls[name.replace("-", "_")] = url_function
            self.urls[name] = url_function

        return self.urls
