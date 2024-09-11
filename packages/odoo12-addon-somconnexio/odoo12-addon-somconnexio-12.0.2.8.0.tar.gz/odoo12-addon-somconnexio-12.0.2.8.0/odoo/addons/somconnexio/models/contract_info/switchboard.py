from odoo import models, fields


class SwitchboardServiceContractInfo(models.Model):
    _name = "switchboard.service.contract.info"
    _inherit = "base.service.contract.info"
    client_id = fields.Char("Client Id")
    extension = fields.Char("Extension")
    phone_number = fields.Char(default="-")
    contract_ids = fields.One2many(
        "contract.contract", "switchboard_service_contract_info_id", "Contracts"
    )
