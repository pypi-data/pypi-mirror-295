# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe78a3c6OrganizationStructure(models.Model):
    _name = "general_audit_ws_e78a3c6.organization_structure"
    _description = "Worksheet e78a3c6 - Organization Structure"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_e78a3c6",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    name = fields.Char(
        string="Unit of Organization",
        required=True,
    )
    responsibility = fields.Char(
        string="Responsiblity",
        required=True,
    )
