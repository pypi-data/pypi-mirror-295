# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditRelevantRegulationItem(models.Model):
    _name = "general_audit_relevant_regulation.item"
    _description = "General Audit Relevant Regulation - Items"
    _order = "regulation_id, parent_id, sequence, id"

    regulation_id = fields.Many2one(
        string="Regulation",
        comodel_name="general_audit_relevant_regulation",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    parent_id = fields.Many2one(
        string="Parent",
        comodel_name="general_audit_relevant_regulation.item",
        ondelete="set null",
    )
    name = fields.Char(
        string="Item",
        required=True,
    )
    description = fields.Text(
        string="Description",
    )
