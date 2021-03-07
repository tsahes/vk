from marshmallow import Schema, fields, ValidationError, INCLUDE

def answer_validation(text):
    if text[0] == '/':
        return False
    else:
        return True

#DATA VERIFICATION
class answerSchema(Schema):
    class Meta:
        unknown = INCLUDE
    text = fields.Str(required=True, validate=answer_validation(),
                      error_messages={'required': 'Answer to the question is required',
                                      'validator_failed': 'Answer cannot start with the "/" symbol'})
    id = fields.Integer(default=0)
    is_correct = fields.Boolean(default=True)
    order = fields.Integer(default=0)


class questionSchema(Schema):
    class Meta:
        unknown = INCLUDE
    points = fields.Integer(required=True, error_messages={'required' : 'Points are required'})
    theme = fields.Str(required=True, error_messages={'required' : 'Theme is required'})
    text = fields.Str(required=True, error_messages={'required' : 'Text of the question is required'})
    answers = fields.Nested(answerSchema())
#    order = fields.Integer(default=0)


class gameSchema(Schema):
    group_id = fields.Integer()
    game_id = fields.Str()
    players = fields.Dict()
    players_answered = fields.List()
    current_question = fields.Str()
    current_theme = fields.Str(allow_none=True)
    time_finish = fields.DateTime()
    game_finished = fields.Boolean(default=False)


def data_verification(data: dict, type: str) -> dict:
    if type == 'game':
        schema = gameSchema()
    elif type == 'question':
        schema = questionSchema()

    try:
        result = schema.load(data)
#        pprint(result)
#        correct_question = schema.dump(result)
        return dict(success=True, data=result)
    except ValidationError as err:
        return dict(success=False, data=err.messages)



