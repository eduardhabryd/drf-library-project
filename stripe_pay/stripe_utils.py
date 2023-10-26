def stripe_payment(data):
    print(data.__dict__)

    # {'_args': (),
    #  '_kwargs':{
    #      'data': < QueryDict: {
    #           'csrfmiddlewaretoken': ['bQHrErCESz9xRGlk3XKTvLAPMu2Ak03oCru9rb4pMeQT48y9bh71YmpgpPvtzY34'],
    #           'book': ['1'],
    #           'expected_return_date': ['2023-11-15']} >,
    #           'context': {
    #           'request': < rest_framework.request.Request: POST '/api/borrowings/borrowing/' >,
    #           'format': None, 'view': < borrowings.views.BorrowingViewSet object at 0x000002218CC3D110 >}},
    #           'instance': < Borrowing:
    #               Borrowed Book ID: Best Book(78),
    #               User ID: admin @ admin.com,
    #               Borrow Date: 2023 - 10 - 26,
    #               Expected Return Date: 2023 - 11 - 15,
    #               Actual Return Date: None >,
    #           'initial_data': < QueryDict: {
    #               'csrfmiddlewaretoken': ['bQHrErCESz9xRGlk3XKTvLAPMu2Ak03oCru9rb4pMeQT48y9bh71YmpgpPvtzY34'],
    #               'book': ['1'],
    #               'expected_return_date': ['2023-11-15']
    #                                     } >,
    #           'partial': False,
    #           '_context': {
    #               'request': < rest_framework.request.Request: POST '/api/borrowings/borrowing/' >,
    #               'format': None,
    #               'view': < borrowings.views.BorrowingViewSet object at 0x000002218CC3D110 >},
    #               '_creation_counter': 7,
    #               'read_only': False,
    #               'write_only': False,
    #               'required': True,
    #               'default': <class 'rest_framework.fields.empty'>,
    #               'source': None,
    #               'initial': None,
    #               'label': None,
    #               'help_text': None,
    #               'style': {},
    #               'allow_null': False,
    #               'field_name': None,
    #               'parent': None,
    #               'error_messages': {
    #                   'required': 'This field is required.',
    #                   'null': 'This field may not be null.',
    #                   'invalid': 'Invalid data. Expected a dictionary, but got {datatype}.'},
    #                   'url_field_name': 'url',
    #                   'fields': {
    #                       'id': IntegerField(label='ID', read_only=True),
    #                       'book': SlugRelatedField(
    #                           queryset=< QuerySet[
    #                               < Book: Best Book(77) >,
    #                               < Book: Another Best Book(100) >] >,
    #                               slug_field = 'id'),
    #                       'expected_return_date': DateField(),
    #                       'actual_return_date': DateField(allow_null=True, default=None, read_only=True)},
    #                       '_validators': [],
    #                       '_validated_data': OrderedDict(
    #                           [('book', < Book: Best Book (78) >),
    #                           ('expected_return_date', datetime.date(2023, 11, 15))]),
    #                           '_errors': {}}
