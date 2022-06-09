"""
    Libraries
"""
from flask import Flask
from flask import jsonify
from flask_restful import reqparse
import sqlalchemy
import psycopg2
import re
import unicodedata
import operator
import pandas as pd

app = Flask(__name__)

"""
    Parser 
"""
parser = reqparse.RequestParser()
parser.add_argument("id", type=int, required=True, help="Id freelance harus diisi")

"""
    Resource 
"""
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500


@app.route('/predict', methods=['POST'])
def predict():
    def remove_url(str):
        str = re.sub(
            r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
            '', str)
        return str

    def remove_digit(str):
        str = re.sub(r'[^a-z ]*([.0-9])*\d', ' ', str)
        return str

    def remove_non_ascii(str):
        str = unicodedata.normalize('NFKD', str).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return str

    def remove_twitter_char(str):
        # mention
        str = re.sub(r'(?:@[\w_]+)', ' ', str)
        # hashtag
        str = re.sub(r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", " ", str)
        # RT/cc
        str = re.sub('RT', ' ', str)

        return str

    def remove_punctuation(str):
        str = re.sub(r'[^\s\w]', ' ', str)
        return str

    def remove_multi_space(str):
        str = re.sub('[\s]+', ' ', str)
        return str

    def casefolding(str):
        str = str.lower()
        return ' '.join(str.split())

    def remove_repeated_character(str):
        str = re.sub(r'(.)\1{2,}', r'\1', str)
        return str

    def normalize_slang_word(str):
        alay_dict = pd.read_csv('data/slang_word_list.csv', encoding='latin-1', header=None)
        alay_dict = alay_dict.rename(columns={0: 'original', 1: 'replacement'})
        alay_dict_map = dict(zip(alay_dict['original'], alay_dict['replacement']))
        return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in str.split(' ')])

    def remove_laugh(str):
        str = re.sub(r"\b(?:(h|a|e)*(?:(ha|he|hue))+h?|(?:l+o+)+l+)|(?:(w|k)*(?:wk)+(w?|k?))\b", ' ', str)

        return str

    def remove_unused_char(str):
        tmp = ""
        if len(str) < 3:
            tmp
        else:
            tmp = str

        return tmp

    def preprocessing(str):
        str = remove_url(str)
        str = remove_twitter_char(str)
        str = remove_digit(str)
        str = remove_non_ascii(str)
        str = remove_punctuation(str)
        str = remove_laugh(str)
        str = remove_multi_space(str)
        str = remove_repeated_character(str)
        str = casefolding(str)
        str = normalize_slang_word(str)
        str = remove_unused_char(str)

        return str

    args = parser.parse_args()
    # data = access_data(hostname, database, username, pwd, port_id)
    test = args["id"]
    # db_host = "ec2-52-86-115-245.compute-1.amazonaws.com"
    # db_port = "5432"
    # db_database = "d1i52s060716to"
    # db_username = "gmwwqbailduxgu"
    # db_password = "0de29981fdbc95fa090da8f93146087bfaa6c7eae6481bdf7a24c2d87a43e262"
    db_host = "kerjamin-capstone:asia-southeast2:kerjamin-db"
    db_port = "5432"
    db_database = "kerjamin-postgres"
    db_username = "postgres"
    db_password = "qaz2plm9wsxokn"
    db_socket_dir = "/cloudsql"
    instance_connection_name = "kerjamin-capstone:asia-southeast2:kerjamin-db"
    unix_socket = f'/cloudsql/{instance_connection_name}'

    conn =  psycopg2.connect(database=db_database, user=db_username, password=db_password, host=unix_socket)

    data = pd.read_sql("select id_freelance, commentary FROM order_review", conn)
    df = data[data['id_freelance'] == test]
    sentence = df["commentary"]
    sentence = sentence.apply(preprocessing)

    data2 = pd.read_csv('data/kata_sifat.csv')
    adj = data2['word']

    count_word = {}
    sentence = sentence.str.split(" ")

    for sw in sentence:
        for i in sw:
            for sw2 in adj:
                if i == sw2:
                    count = count_word.get(i, 0)
                    count += 1
                    count_word[sw2] = count

    most_words = dict(sorted(count_word.items(), key=operator.itemgetter(1), reverse=True)[:5])

    list_most_words = []
    for idx1, i in enumerate(most_words.keys()):
        for idx2, j in enumerate(most_words.values()):
            if idx1 == idx2:
                list_most_words.append(i)
                list_most_words.append(j)

    lst = []
    for idx1, pn in enumerate(list_most_words):
        for idx2, i in enumerate(list_most_words):
            d = {}
            d['sifat'] = pn
            if idx1 == idx2 - 1:
                d['value'] = i
                lst.append(d)

    listAkhir = []
    for idx1, pn in enumerate(lst):
        if idx1 % 2 == 0:
            listAkhir.append(pn)

    return {
        "data": listAkhir
    }, 200


"""
    Main 
"""
if __name__ == '__main__':
    app.run()
