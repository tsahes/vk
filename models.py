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
    text = fields.Str(required=True, validate=answer_validation,
                      error_messages={'required': 'Answer to the question is required',
                                      'validator_failed': 'Answer cannot start with the "/" symbol'})
    id = fields.Integer(default=0)
    is_correct = fields.Boolean(default=True)
    order = fields.Integer(default=0)


class questionSchema(Schema):
    class Meta:
        unknown = INCLUDE
    points = fields.Integer(required=True, error_messages={'required': 'Points are required'})
    theme = fields.Str(required=True, error_messages={'required': 'Theme is required'})
    text = fields.Str(required=True, error_messages={'required': 'Text of the question is required'})
    answers = fields.Nested(answerSchema(), required=True, error_messages={'required': 'Answer is required'})
#    order = fields.Integer(default=0)


class gameSchema(Schema):
    group_id = fields.Integer(required=True, error_messages={'required': 'Group/chat id is required'})
    game_id = fields.Str(required=True, error_messages={'required': 'Game id is required'})
    players = fields.Dict(required=True,
                          error_messages={'required': 'Dictionary of players and their points is required'})
    players_answered = fields.List(fields.Str(), required=True,
                                   error_messages={'required': 'List of players is required'})
    current_question = fields.Str()
    current_theme = fields.Str(allow_none=True)
    time_finish = fields.DateTime()
    game_finished = fields.Boolean(default=False, required=True,
                                   error_messages={'required': 'Finished flag is required'})


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



