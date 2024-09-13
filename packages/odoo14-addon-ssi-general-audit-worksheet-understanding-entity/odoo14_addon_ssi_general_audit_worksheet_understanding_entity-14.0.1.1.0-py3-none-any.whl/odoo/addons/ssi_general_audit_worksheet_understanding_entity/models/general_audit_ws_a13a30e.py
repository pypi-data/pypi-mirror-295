# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa13a30e(models.Model):
    _name = "general_audit_ws_a13a30e"
    _description = "Understanding of Relevant Regulations (a13a30e)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_a13a30e"
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_a13a30e.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
