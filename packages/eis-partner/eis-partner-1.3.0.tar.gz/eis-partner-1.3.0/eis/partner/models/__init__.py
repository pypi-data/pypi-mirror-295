# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from eis.partner.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from eis.partner.model.create_partner_relation_request_dto_rest import CreatePartnerRelationRequestDtoRest
from eis.partner.model.create_partner_relation_response_class import CreatePartnerRelationResponseClass
from eis.partner.model.create_partner_request_dto import CreatePartnerRequestDto
from eis.partner.model.create_partner_response_class import CreatePartnerResponseClass
from eis.partner.model.create_partner_type_request_dto import CreatePartnerTypeRequestDto
from eis.partner.model.create_partner_type_response_class import CreatePartnerTypeResponseClass
from eis.partner.model.create_tag_request_dto import CreateTagRequestDto
from eis.partner.model.create_tag_response_class import CreateTagResponseClass
from eis.partner.model.delete_response_class import DeleteResponseClass
from eis.partner.model.get_partner_relation_class import GetPartnerRelationClass
from eis.partner.model.get_partner_relation_type_class import GetPartnerRelationTypeClass
from eis.partner.model.get_partner_response_class import GetPartnerResponseClass
from eis.partner.model.get_partner_type_response_class import GetPartnerTypeResponseClass
from eis.partner.model.get_partner_version_response_class import GetPartnerVersionResponseClass
from eis.partner.model.get_tag_response_class import GetTagResponseClass
from eis.partner.model.inline_response200 import InlineResponse200
from eis.partner.model.inline_response503 import InlineResponse503
from eis.partner.model.list_partner_relation_class import ListPartnerRelationClass
from eis.partner.model.list_partner_relation_types_class import ListPartnerRelationTypesClass
from eis.partner.model.list_partner_types_response_class import ListPartnerTypesResponseClass
from eis.partner.model.list_partner_versions_response_class import ListPartnerVersionsResponseClass
from eis.partner.model.list_partners_response_class import ListPartnersResponseClass
from eis.partner.model.list_tags_response_class import ListTagsResponseClass
from eis.partner.model.partner_class import PartnerClass
from eis.partner.model.partner_relation_class import PartnerRelationClass
from eis.partner.model.partner_relation_type_class import PartnerRelationTypeClass
from eis.partner.model.partner_type_class import PartnerTypeClass
from eis.partner.model.relation_type_slug import RelationTypeSlug
from eis.partner.model.tag_class import TagClass
from eis.partner.model.tag_partner_request_dto_rest import TagPartnerRequestDtoRest
from eis.partner.model.update_partner_relation_request_dto_rest import UpdatePartnerRelationRequestDtoRest
from eis.partner.model.update_partner_request_dto import UpdatePartnerRequestDto
from eis.partner.model.update_partner_response_class import UpdatePartnerResponseClass
from eis.partner.model.update_partner_type_request_dto import UpdatePartnerTypeRequestDto
from eis.partner.model.update_partner_type_response_class import UpdatePartnerTypeResponseClass
from eis.partner.model.update_tag_response_class import UpdateTagResponseClass
