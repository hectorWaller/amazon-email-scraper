thonpython
class EmailFilters:
    def __init__(self, allowed_countries=None, location_keyword=None, allowed_domain=None):
        self.allowed_countries = allowed_countries or []
        self.location_keyword = location_keyword.lower() if location_keyword else None
        self.allowed_domain = allowed_domain.lower() if allowed_domain else None

    def apply(self, email: str, country: str, location: str) -> bool:
        """Return True if email passes all filters."""
        if self.allowed_countries and country not in self.allowed_countries:
            return False

        if self.location_keyword and (location is None or self.location_keyword not in location.lower()):
            return False

        if self.allowed_domain and not email.lower().endswith(self.allowed_domain):
            return False

        return True