credits = [3, 2, 16.5, 4.5, 3, 3, 1.5, 0.5, 2.5, 6, 4.5, 9, 5, 7.5, 3,
              4.5, 5, 2.5, 7, 2.5, 3, 11, 1.5, 6, 3, 3, 4.5, 3.5, 16.5, 10,
              5, 3, 4.5, 6, 3, 7, 2, 9, 5, 5, 5, 1.5, 3, 3, 6, 3, 3,
              2.5, 2.5, 3, 3, 3, 3, 3, 6, 2.5, 2.5]

grades_10 = [8, 10, 10, 8, 10, 10, 9, 7, 5, 7, 6, 8, 9,
                8, 8, 10, 10, 10, 8, 7, 10, 10, 8, 7, 7,
                10, 8, 8, 9, 10, 8, 7, 6, 7, 8, 9, 10, 7,
                10, 8, 9, 7, 8, 10, 10, 7, 7,
                9, 8, 10, 9, 10, 10, 6, 7, 10, 9]

# print(sum([x*y for x, y in zip(credits, grades_10)]) / sum(credits))

grades_10_to_5 = {10 : 5, 9 : 5, 8 : 5,
                     7 : 4, 6 : 4,\
                    5 : 3}
grades_5 = [grades_10_to_5[ten] for ten in grades_10]

# print(sum([x*y for x, y in zip(credits, grades_5)]) /( sum(credits)))

from main import quest_verification




rem = dict(text='LOSING MY RELIGION')
rem_q = dict(answers=rem, points=10, text='ЭТО сленговое американское выражение, говорящее о потере терпения, '
          'принесло две премии "Грэмми" группе "R.E.M."')


quest_verification(rem_q)


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
    'theme' : 'Религиозная',
    "order": 1,
  "text": 'ЭТО сленговое американское выражение, говорящее о потере терпения, принесло две премии "Грэмми" группе "R.E.M."',
  "points": 10,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "LOSING MY RELIGION",
    "is_correct": True
  }
}

rel_question_2 = {
    "order": 2,
  "text": 'Именно ТАК звучат по-японски слова "путь богов".',
  "points": 20,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "СИНТО",
    "is_correct": True
  }
}

rel_question_3 = {
    "order": 3,
  "text": 'Вождь Терииероо, живший на ЭТОМ острове, чрезвычайно обрадовался, когда узнал от Тура Хейердала, что в Скандинавии почти все исповедуют протестантскую веру.',
  "points": 30,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "ТАИТИ",
    "is_correct": True
  }
}

rel_question_4 = {
    "order": 4,
  "text": 'Три религии: иудаизм, христианство и ислам — нередко объединяют ЭТИМ прилагательным.',
  "points": 40,
  "answers": {
    "order": 0,
    "id": 0,
    "text":  "АВРААМИЧЕСКИЕ",
    "is_correct": True
  }
}

rel_question_5 = {
    "order": 5,
  "text": 'В России исповедующие ЭТУ религию традиционно называют ее "благоверие".',
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