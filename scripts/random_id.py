import random


ids = [
    '0a8a0072-fc0d-11e8-9b56-4a0006dd1f80',
    'a519e37e-fc0c-11e8-9b56-4a0006dd1f80',
    '39a0b586-fc0d-11e8-9b56-4a0006dd1f80',
    '534b0608-fc0d-11e8-9b56-4a0006dd1f80',
    '3d2a72e6-fc0d-11e8-9b56-4a0006dd1f80',
    'b30c872a-fc0c-11e8-9b56-4a0006dd1f80',
    'c9255c30-fc0c-11e8-9b56-4a0006dd1f80',
    'bf108d96-fc0c-11e8-9b56-4a0006dd1f80',
    '22cdd668-fc0d-11e8-9b56-4a0006dd1f80',
    '1f736974-fc0d-11e8-9b56-4a0006dd1f80',
    '5699b2c8-fc0d-11e8-9b56-4a0006dd1f80',
    '52bd975a-fc0d-11e8-9b56-4a0006dd1f80',
    'cdc66388-fc0c-11e8-9b56-4a0006dd1f80',
    'c44a7bbe-fc0c-11e8-9b56-4a0006dd1f80',
    '29a03e36-fc0d-11e8-9b56-4a0006dd1f80',
    '38008a26-fc0d-11e8-9b56-4a0006dd1f80',
    '1f523394-fc0d-11e8-9b56-4a0006dd1f80',
    '0c5c6dcc-fc0d-11e8-9b56-4a0006dd1f80',
    '36cf478c-fc0d-11e8-9b56-4a0006dd1f80',
    'db51eacc-fc0c-11e8-9b56-4a0006dd1f80',
    'a9bff800-fc0c-11e8-9b56-4a0006dd1f80',
    '563f9180-fc0d-11e8-9b56-4a0006dd1f80',
    '15dc3166-fc0d-11e8-9b56-4a0006dd1f80',
    '38e39ec4-fc0d-11e8-9b56-4a0006dd1f80',
    '07d239ee-fc0d-11e8-9b56-4a0006dd1f80',
    'ecef5e9a-fc0c-11e8-9b56-4a0006dd1f80',
    'c27d4f28-fc0c-11e8-9b56-4a0006dd1f80',
    'af102e74-fc0c-11e8-9b56-4a0006dd1f80',
    '526f74b2-fc0d-11e8-9b56-4a0006dd1f80'
]


def getRandomId():
    return random.sample(ids, 3)[1]