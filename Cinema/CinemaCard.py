import pandas as pd


class CinemaCard(object):
    __path_to_cards = r'C:/Users/Zlyde/PycharmProjects/PhylonemaBot/resources/Cinema/CinemaCards.csv'
    __path_to_rates = r'C:/Users/Zlyde/PycharmProjects/PhylonemaBot/resources/Cinema/Rates.csv'
    __path_to_unseen_reviews = r'C:/Users/Zlyde/PycharmProjects/PhylonemaBot/resources/Cinema/UnseenReviews.csv'
    __path_to_applied_reviews = r'C:/Users/Zlyde/PycharmProjects/PhylonemaBot/resources/Cinema/AppliedReviews.csv'
    cinema_cards_base = pd.read_csv(__path_to_cards)
    rates_base = pd.read_csv(__path_to_rates)

    def calculate_average_rating(self, category: str) -> float:
        all_rates: pd.DataFrame = self.rates_base[category].loc[(self.rates_base['Название'] == self.name) &
                                                                (self.rates_base['Автор'] == self.author)]
        sum_of_rates = sum(all_rates)
        amount_of_rates = all_rates.count()
        return sum_of_rates/amount_of_rates

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
        cls.cinema_cards_base.to_csv(cls.__path_to_cards, index=False)
        cls.cinema_cards_base = pd.read_csv(cls.__path_to_cards)
        return CinemaCard(name, author, timecodes, link)

    def __init__(self, name: str = '', author: str = '', timecodes: str = '', link: str = '', ):
        self.name = name
        self.author = author
        self.timecodes = timecodes
        self.link = link
        categories = ('Философская глубина',
                      'Острота постановки проблемы',
                      'Наличие категориального аппарата',
                      'Эстетическое удовольствие',
                      'Насколько берет за душу',
                      'Раскрытие мировоззрения автора',
                      'Художественная глубина',
                      'Общее впечатление')
        self.rating: dict = {x: self.calculate_average_rating(x) for x in categories}
        self.unseen_reviews = self.get_reviews_from_csv(self.__path_to_unseen_reviews)
        self.applied_reviews = self.get_reviews_from_csv(self.__path_to_applied_reviews)
        self.unseen_reviews_amount = len(tuple(self.unseen_reviews))
        self.applied_reviews_amount = len(tuple(self.applied_reviews))

    def get_reviews_from_csv(self, path: str):
        unseen_reviews_base = pd.DataFrame(path)
        unseen_reviews = unseen_reviews_base.loc[(unseen_reviews_base['Название фильма'] == self.name) &
                                                 (unseen_reviews_base['Режиссер'] == self.author)]
        ids = list(unseen_reviews['Автор'])
        texts = list(unseen_reviews['Текст рецензии'])
        return zip(ids, texts)

    def add_rating(self, rating=None):
        if rating is None:
            rating = [0, 0, 0, 0, 0, 0, 0, 0]
        if len(rating) == 8:
            length = len(self.rates_base)
            self.rates_base.loc[length] = rating
            self.rates_base.to_csv(self.__path_to_rates)
        else:
            raise ValueError('Not enough values for setting rating')

    @classmethod
    def get_card_from_csv(cls, name: str, author: str):
        film_info: pd.DataFrame = cls.cinema_cards_base.loc[(cls.cinema_cards_base['Название'] == name) &
                                                            (cls.cinema_cards_base['Режиссер'] == author)]
        values = film_info.values[0][2:]
        timecodes, link, reviews_amount, *rating = values
        search_result = CinemaCard(name, author, timecodes, link)
        search_result.add_rating(rating)
        return search_result

    def __str__(self):
        return str(self.cinema_cards_base.loc[(self.cinema_cards_base['Название'] == self.name) &
                                              (self.cinema_cards_base['Режиссер'] == self.author)])

    def add_review_to_csv(self, user_id: str, review_text: str, path: str):
        unseen_reviews_base = pd.DataFrame(path)
        length = len(unseen_reviews_base)
        unseen_reviews_base.loc[length] = (user_id, self.name, self.author, review_text)
        unseen_reviews_base.to_csv(path, index=False)

    def get_next_unseen_review(self):
        return next(self.unseen_reviews)

    def get_next_applied_review(self):
        return next(self.applied_reviews)

    def apply_review(self, id_: str):
        unseen_reviews_base = pd.read_csv(self.__path_to_unseen_reviews)
        review = unseen_reviews_base.loc[(unseen_reviews_base['Название'] == self.name) &
                                         (unseen_reviews_base['Режиссер'] == self.author) &
                                         (unseen_reviews_base['Автор'] == id_)]
        review_index = review.index[0]
        unseen_reviews_base.drop(review_index)
        unseen_reviews_base.to_csv(self.__path_to_unseen_reviews)
        applied_reviews_base = pd.read_csv(self.__path_to_applied_reviews)
        applied_reviews_base = pd.concat(applied_reviews_base, review)
        applied_reviews_base.to_csv(self.__path_to_applied_reviews)

    def decline_review(self, id_: str):
        unseen_reviews_base = pd.read_csv(self.__path_to_unseen_reviews)
        review = unseen_reviews_base.loc[(unseen_reviews_base['Название'] == self.name) &
                                         (unseen_reviews_base['Режиссер'] == self.author) &
                                         (unseen_reviews_base['Автор'] == id_)]
        review_index = review.index[0]
        unseen_reviews_base.drop(review_index)
        unseen_reviews_base.to_csv(self.__path_to_unseen_reviews)
