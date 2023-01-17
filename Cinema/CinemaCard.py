import pandas as pd


class CinemaCard(object):
    cinema_cards_base = pd.read_csv(r'C:/Users/Zlyde/PycharmProjects/PhylonemaBot/resources/Cinema/CinemaCards.csv')

    def add_card_to_csv(self):
        length = len(self.cinema_cards_base)
        row = [self.name, self.author, self.timecodes, self.link, self.reviews_amount]
        for i in self.rating.keys():
            row.append(self.rating[i])
        self.cinema_cards_base.loc[length] = row
        self.cinema_cards_base.to_csv(r'C:/Users/Zlyde/PycharmProjects/PhylonemaBot/resources/Cinema/CinemaCards.csv',
                                      index=False)

    def __init__(self, name: str = '', author: str = '', timecodes: str = '', link: str = ''):
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
        self.add_card_to_csv()

