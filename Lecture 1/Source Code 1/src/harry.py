from logic import *

rain = Symbol("rain")  # It rained
hagrid = Symbol("hagrid")  # Visited Hagrid
dumbledore = Symbol("dumbledore")  # Visited Dumbledore

knowledge = And(
    Implication(Not(rain), hagrid),
    Or(hagrid, dumbledore),
    Not(And(hagrid, dumbledore)),
    dumbledore
)
# model = {'hagrid': True, 'rain': True}
# print(model_check(knowledge, rain))
# print(And(hagrid, rain).symbols())