from marshmallow import Schema, fields, ValidationError, INCLUDE


#DATA VERIFICATION
class answerSchema(Schema):
    class Meta:
        unknown = INCLUDE
    text = fields.Str(required=True, error_messages={'required' : 'Answer to the question is required'})
    id = fields.Integer(default=0)
    is_correct = fields.Boolean(default=True)
    order = fields.Integer(default=0)


class questionSchema(Schema):
    class Meta:
        unknown = INCLUDE
    points = fields.Integer()
    theme = fields.Str(required=True, error_messages={'required' : 'Theme is required'})
    text = fields.Str(required=True, error_messages={'required' : 'Text of the question is required'})
    answers = fields.Nested(answerSchema())
#    order = fields.Integer(default=0)


def quest_verification(question):
    schema = questionSchema()

    try:
        result = schema.load(question)
#        pprint(result)
#        correct_question = schema.dump(result)
        return dict(success=True, data=result)
    except ValidationError as err:
        return dict(success=False, data=err.messages)