import pandas as pd


class CinemaCard(object):
    __path = r'C:/Users/Zlyde/PycharmProjects/PhylonemaBot/resources/Cinema/CinemaCards.csv'
    cinema_cards_base = pd.read_csv(__path)

    @classmethod
    def add_card_to_csv(cls, name: str = '', author: str = '', timecodes: str = '', link: str = ''):
        rating: dict = {'Философская глубина': 0,
                        'Острота постановки проблемы': 0,
                        'Наличие категориального аппарата': 0,
                        'Эстетическое удовольствие': 0,
                        'Насколько берет за душу': 0,
                        'Раскрытие мировоззрения автора': 0,
                        'Художественная глубина': 0,
                        'Общее впечатление': 0}
        reviews_amount: int = 0
        length = len(cls.cinema_cards_base)
        row = [name, author, timecodes, link, reviews_amount]
        for i in rating.keys():
            row.append(rating[i])
        cls.cinema_cards_base.loc[length] = row
        cls.cinema_cards_base.to_csv(cls.__path, index=False)
        return

    def __init__(self, name: str = '', author: str = '', timecodes: str = '', link: str = '', ):
        self.name = name
        self.author = author
        self.timecodes = timecodes
        self.link = link
        self.rating: dict = {'Философская глубина': 0,
                             'Острота постановки проблемы': 0,
                             'Наличие категориального аппарата': 0,
                             'Эстетическое удовольствие': 0,
                             'Насколько берет за душу': 0,
                             'Раскрытие мировоззрения автора': 0,
                             'Художественная глубина': 0,
                             'Общее впечатление': 0}
        self.reviews_amount: int = 0

    def set_rating(self, rating=None):
        if rating is None:
            rating = [0, 0, 0, 0, 0, 0, 0, 0]
        if len(rating):
            k = 0
            for i in self.rating.keys():
                self.rating[i] = rating[k]
                k += 1
        else:
            raise ValueError('Not enough values for setting rating')

    @classmethod
    def get_card_from_csv(cls, name: str, author: str):
        film_info: pd.DataFrame = cls.cinema_cards_base.loc[(cls.cinema_cards_base['Название'] == name) &
                                                            (cls.cinema_cards_base['Режиссер'] == author)]
        values = film_info.values[0][2:]
        timecodes, link, reviews_amount, *rating = values
        search_result = CinemaCard(name, author, timecodes, link)
        search_result.set_rating(rating)
        return search_result

    def __str__(self):
        return str(self.cinema_cards_base.loc[(self.cinema_cards_base['Название'] == self.name) &
                                              (self.cinema_cards_base['Режиссер'] == self.author)])

