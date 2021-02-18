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
    points = fields.Integer(required=True, error_messages={'required' : 'Points are required'})
    theme = fields.Str(required=True, error_messages={'required' : 'Theme is required'})
    text = fields.Str(required=True, error_messages={'required' : 'Text of the question is required'})
    answers = fields.Nested(answerSchema())
#    order = fields.Integer(default=0)


class gamerSchema(Schema):
    user_id = fields.Integer()
    user_score = fields.Integer()

class gameSchema(Schema):
    group_id = fields.Integer()
    game_id = fields.Str()
    gamers = fields.Nested(gamerSchema())
    current_question = fields.Str()
    current_theme = fields.Str()
    time_finish = fields.DateTime()
    game_finished = fields.Boolean(default=False)

def quest_verification(question):
    schema = questionSchema()

    try:
        result = schema.load(question)
#        pprint(result)
#        correct_question = schema.dump(result)
        return dict(success=True, data=result)
    except ValidationError as err:
        return dict(success=False, data=err.messages)


