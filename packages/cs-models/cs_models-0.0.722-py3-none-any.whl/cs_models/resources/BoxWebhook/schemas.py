from marshmallow import (
    Schema,
    fields,
)


class BoxDriveResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    webhook_id = fields.String(required=True)
    enterprise_id = fields.String(required=True)
    updated_at = fields.DateTime(dump_only=True)
