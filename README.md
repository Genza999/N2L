# N2L
An API that translates number/digits less than 1 billion into Uganda's main indigenous language(Luganda)

## Usage

```
GET https://n2l.herokuapp.com/convert/{the_number_to_be_translated}
```

## Examples

1.
```
GET https://n2l.herokuapp.com/convert/300

Response:
{
    "number": 300,
    "luganda_translation": "bisatu"
}
```

2.
```
GET https://n2l.herokuapp.com/convert/8950

Response:
{
    "number": 8950,
    "luganda_translation": "kanaana mu lwenda mu ataano"
}
```

3.
```
GET https://n2l.herokuapp.com/convert/300490

Response:
{
    "number": 8950,
    "luganda_translation": "mitwaalo assatu mu bina mu kyenda"
}
```

## Restrictions
At the moment, the API does not handle numbers larger than 1 billion

## Authors
[Kisekka David](https://github.com/Genza999)
