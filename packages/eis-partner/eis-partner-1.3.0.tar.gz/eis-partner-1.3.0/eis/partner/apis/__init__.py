
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from eis.partner.api.partner_relations_api import PartnerRelationsApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from eis.partner.api.partner_relations_api import PartnerRelationsApi
from eis.partner.api.partner_tags_api import PartnerTagsApi
from eis.partner.api.partner_types_api import PartnerTypesApi
from eis.partner.api.partner_version_api import PartnerVersionApi
from eis.partner.api.partners_api import PartnersApi
from eis.partner.api.default_api import DefaultApi
