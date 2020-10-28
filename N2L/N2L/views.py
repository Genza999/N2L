from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from N2L.N2L.utilities import (
    ones_dict, tens_dict, hundreds_dict, thousands_dict, ten_thousands_dict,
    hundred_thousands_dict, millions_dict, billion_dict
)

numbers_list = [
    ones_dict, tens_dict, hundreds_dict, thousands_dict, ten_thousands_dict,
    hundred_thousands_dict, millions_dict, billion_dict
]

class Convert(APIView):
    def value(self, number):
        for dictionary in numbers_list:
            if int(number) in dictionary:
                return dictionary[int(number)]

    def tens_range(self, number):
        append_string = 'kkumi na'
        digit_word = ones_dict[int(number)]
        return f'{append_string} {digit_word}'

    def first_check(self, number):
        return self.value(number)

    def validate(self, number):
        error = []

        # raise error if number isnt integer
        if not isinstance(number, int):
            error.append('Number is not an integer')

        if not str(number).isnumeric():
            error.append('Alphabet characters not allowed')
        
        # remove leading zeros
        if str(number)[0] == '0':
            number = str(number).lstrip('0')
            number = int(number)

        # raise error if number is bigger than 1000000000(1 billion)
        if number > 1000000000:
           error.append('Number bigger than 1 billion wont be translated')
        
        return error, number


    def get(self, request, req_number):
        # valiate the users number
        error, number = self.validate(req_number)
        if error:
            return Response(
                {
                    'error(s)': ', '.join(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # check if number is basic translation
        result = self.first_check(number)
        if result:
            return Response(
                {
                    'number': req_number,
                    'luganda_translation': result
                },
                status=status.HTTP_200_OK
            )
        
        # again checking if number is basic translation
        if number in range(11, 20):
            second_digit = str(number)[1]
            result = self.tens_range(second_digit)
            if result:
                return Response(
                    {
                        'number': req_number,
                        'luganda_translation': result
                    },
                    status=status.HTTP_200_OK
                )
        
        # if not in basic translation, time for magic
        length = len(str(number))
        dec_length = length - 1
        word_list = []

        # if number is greater than 999,999 and complex i.e. not basic
        if length > 7:                                                                                                                                                                                                                                                                                                                                                                                                                                          
            this_number = str(number)[0:-6]
            this_length = len(this_number) - 1
            if len(this_number) == 2 and this_number[0] == '1' and not this_number[1] == '0':
                word = self.tens_range(int(this_number[-1]))
                the_word = 'bukadde ' + word
                word_list.append(the_word)
            else:
                for i in this_number:
                    if i == '0':
                        this_length = this_length - 1
                        continue
                    new_number = i + (this_length * '0')
                    word = self.value(new_number)
                    word_list.append(word)
                    this_length = this_length - 1

                word_list[0] = 'bukadde ' + word_list[0]

            number = str(number)[-6:]
            newlength = len(str(number))
            dec_length = newlength - 1

        # if number is less than 1,000,000 and complex i.e. not basic
        for i in str(number):
            if i == '0':
                dec_length = dec_length - 1
                continue

            if dec_length == 1:
                if str(number)[-1] == '0':
                    word = self.value(i + '0')
                    word_list.append(word)
                    break

                if i == '1':
                    word = self.tens_range(str(number)[-1])
                    word_list.append(word)
                    break

            new_number = i + (dec_length * '0')
            word = self.value(new_number)
            word_list.append(word)
            dec_length = dec_length - 1

        # final construct of luganda translation
        final_word = ' mu '.join(word_list)
        return Response(
            {
                'number': req_number,
                'luganda_translation': final_word
            },
            status=status.HTTP_200_OK
        )


