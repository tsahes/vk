#from main import quest_verification

rem = dict(text='LOSING MY RELIGION')
rem_q = dict(answers=rem, points=10, text='ЭТО сленговое американское выражение, говорящее о потере терпения, '
          'принесло две премии "Грэмми" группе "R.E.M."')


#quest_verification(rem_q)


# FILLING UP THE DB
#print(find_document(db.questions))
#insert_document(db.questions, {'status' : 'not_ok'})

empty_question = {
  "order": 0,
  "text": "string",
  "points": 0,
  "answers": {
    "order": 0,
    "id": 0,
    "text": "string",
    "is_correct": True
  }
}
#insert_document(db.questions, empty_question)
#db.questions.delete_many({'status' : 'not_ok'})

#ADDING A PACKAGE OF QUESTIONS
rel_question_1 = {
    "theme" : "Религиозная",
  "text": "ЭТО сленговое американское выражение, говорящее о потере терпения, принесло две премии 'Грэмми' группе 'R.E.M.'",
  "points": 10,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "LOSING MY RELIGION",
    "is_correct": True
  }
}

rel_question_2 = {
    "theme" : "Религиозная",
  "text": "Именно ТАК звучат по-японски слова 'путь богов'.",
  "points": 20,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "СИНТО",
    "is_correct": True
  }
}

rel_question_3 = {
    "theme" : "Религиозная",
  "text": "Вождь Терииероо, живший на ЭТОМ острове, чрезвычайно обрадовался, когда узнал от Тура Хейердала, что в Скандинавии почти все исповедуют протестантскую веру.",
  "points": 30,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "ТАИТИ",
    "is_correct": True
  }
}

rel_question_4 = {
    "theme" : "Религиозная",
  "text": "Три религии: иудаизм, христианство и ислам — нередко объединяют ЭТИМ прилагательным.",
  "points": 40,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "АВРААМИЧЕСКИЕ",
    "is_correct": True
  }
}

rel_question_5 = {
    "theme" : "Религиозная",
  "text": "В России исповедующие ЭТУ религию традиционно называют ее 'благоверие'.",
  "points": 50,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "ЗОРОАСТРИЗМ",
    "is_correct": True
  }
}

rel_package = [rel_question_1, rel_question_2,
               rel_question_3, rel_question_4,
               rel_question_5]

#for quest in rel_package:
#    insert_document(db.questions, quest)

#pprint(find_document(db.questions, multiple=True))

a = dict(b=2, c=3)