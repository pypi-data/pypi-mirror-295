# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe78a3c6(models.Model):
    _name = "general_audit_ws_e78a3c6"
    _description = "Structure Organization and Responsibilities (e78a3c6)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_e78a3c6"
    )

    organtization_structure_ids = fields.One2many(
        string="Organization Structures",
        comodel_name="general_audit_ws_e78a3c6.organization_structure",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
