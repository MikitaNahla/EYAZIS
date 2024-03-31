import json
import os
import re
import string

import nltk
from nltk import Text
from server import app, conn, UPLOAD_FOLDER
from flask import request
from textDecoder import PDFReader
from textHandler import TextHandler
from nltk.stem import PorterStemmer
from operator import itemgetter


def skip_repeat_words(new_words, all_words):
    unique_words = []

    for new_word in new_words:
        count = 0
        for word in all_words:
            if word['word'].lower() == new_word['word'].lower():
                count = count + 1
                break
        if count == 0:
            new_word['word'] = new_word['word'].lower()
            unique_words.append(new_word)

    return unique_words


def get_words():
    vocabulary = []

    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('SELECT * FROM words')
        temp_vocabulary = curs.fetchall()

    for word in temp_vocabulary:
        vocabulary.append(
            {
                'id': word[0],
                'word': word[1],
                'stem': word[2],
                'part_of_speech': word[3]
            }
        )

    return vocabulary


def get_endings(cursor, word):
    with cursor as curs:
        curs.execute('SELECT * FROM endings WHERE endings.word_id = (%s)', [word['id']])
        temp_endings = curs.fetchall()

        endings = []
        for ending in temp_endings:
            endings.append({'name': ending[1], 'info': ending[2]})
    return endings


def add_endings(all_words):
    for word in all_words:
        cursor = conn.cursor()

        endings = get_endings(cursor, word)
        word['endings'] = endings


def transform_to_needed_data(words):
    words = sorted(words, key=itemgetter('word'))

    return json.dumps(words, indent=4, ensure_ascii=False)

# POST request


def add_to_db(unique_words):
    cursor = conn.cursor()
    with cursor as curs:
        for word in unique_words:
            if len(word['info']) != 0:
                curs.execute("INSERT INTO words (word, stem, part_of_speech) VALUES (%s, %s, %s) returning id",
                             [word['word'], word['info']['stem'], word['info']['part_of_speech']])
                word_id = curs.fetchone()[0]
                endings = word['info']['endings']
                for ending in endings:
                    curs.execute('INSERT INTO endings (name, info, word_id) VALUES (%s, %s, %s)',
                                 [ending[0], ending[1], word_id])
                conn.commit()


def transform_line(line):
    line = ' '.join(filter(bool, line.split()))
    line_list = list(line)
    for index, value in enumerate(line_list):
        if index + 2 <= len(line_list) - 1:
            if line_list[index + 2] in string.punctuation and line_list[index + 2] != ' ':
                line_list.pop(index + 1)

    return ''.join(line_list)


def add_context_from_left(line, text, position):
    text_copy = list(text)
    if position > 0:
        while text_copy[position - 1] != ' ':
            line = text_copy[position - 1] + line
            position -= 1

    return line


def add_context_from_right(line, text, position):
    text_copy = list(text)
    if position < len(text_copy) - 1:
        while text_copy[position] != ' ':
            line += text_copy[position]
            position += 1
            if position == len(text_copy):
                break

    return line


def handle_concordance(concordance_line, text):
    concordance_line = transform_line(concordance_line)
    substring_position = text.find(concordance_line)
    substring_length = len(list(concordance_line))
    concordance_line = add_context_from_left(concordance_line, text, substring_position)
    concordance_line = add_context_from_right(concordance_line, text, substring_position + substring_length)
    return concordance_line


def find_concordance(text, word):
    tokens = nltk.word_tokenize(text)
    text_object = Text(tokens)
    concordance = text_object.concordance(word["word"], width=20)
    concordances = []
    for concordance_line in concordance:
        concordance_line = handle_concordance(concordance_line.line, text)
        concordances.append(concordance_line)

    return concordances


def find_all_concordances(text, words):
    new_words = []
    for word in words:
        concordances = find_concordance(text, word)
        new_words.append({
            "word": word["word"],
            "info": word["info"],
            "concordances": concordances
        })
    return new_words


def create_words(text):
    stemmer = PorterStemmer()

    tH = TextHandler(text, 'en_core_web_sm', stemmer)
    tH.convert_text_to_words()

    all_words = get_words()
    new_words = tH.start_handler()
    unique_words = skip_repeat_words(new_words, all_words)
    new_words = find_all_concordances(text, new_words)
    # add_to_db(unique_words)

    return new_words


@app.route('/vocabulary/post/', methods=["POST"])
def handle_words():
    if 'file' not in request.files:
        return json.loads('No file part')

    file = request.files['file']

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    data = PDFReader(UPLOAD_FOLDER + file.filename)
    text = data.get_information()
    os.remove(file.filename)

    new_words = create_words(text)

    return json.dumps({'response': 'The dictionary has been updated'})


def handle_sentences(sentences):

    new_sentences_txt = []
    new_sentences_json = []

    for sentence in sentences:
        new_sentences_txt.append(sentence)

        new_words = create_words(sentence)
        new_sentences_json.append({"sentence": sentence, "words": new_words})

    add_sentences_to_file_txt(new_sentences_txt)
    add_sentences_to_file_json(new_sentences_json)


def add_sentences_to_file_txt(sentences):
    with open('1lab/corpus/text', 'a') as f:
        for sentence in sentences:
            f.write(sentence + '.\n')


def add_sentences_to_file_json(sentences):
    with open('1lab/corpus/corpus') as f:
        old_sentences = json.load(f)

    for sentence in sentences:
        old_sentences.append(sentence)

    with open('1lab/corpus/corpus', 'w') as f:
        json.dump(old_sentences, f)


def check_punctuation_sentences(sentences):
    new_sentences = []
    for sentence in sentences:
        sentence = sentence.replace('\n', '')
        new_sentences.append(sentence)

    return new_sentences


def check_is_lower_register(sentences):
    index = 0

    while index + 1 < len(sentences):
        if len(list(sentences[index + 1])) > 0:
            if sentences[index + 1][0].islower():
                sentences[index] = sentences[index] + '. ' + sentences[index + 1]
                sentences.pop(index + 1)
        index += 1


@app.route('/corpus/post/', methods=["POST"])
def handle_file():
    if 'file' not in request.files:
        return json.loads('No file part')

    file = request.files['file']

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    data = PDFReader(UPLOAD_FOLDER + file.filename)
    text = data.get_information()

    os.remove(file.filename)

    sentences = re.split(r'[!?.]+ *', text)
    sentences.pop()
    if '' in sentences:
        sentences.remove('')
    check_is_lower_register(sentences)
    sentences = check_punctuation_sentences(sentences)
    handle_sentences(sentences)
    print('that is all')

    return json.dumps('Nice')


@app.route('/corpus/get', methods=["GET"])
def get_corpus():
    with open('1lab/corpus/corpus', 'r') as file:
        data = json.load(file)

    return json.dumps(data)


@app.route('/vocabulary/getAll', methods=["GET"])
def get_all_words():
    all_words = get_words()
    add_endings(all_words)

    return transform_to_needed_data(all_words)


# GET chosen employee

@app.route('/vocabulary/get/<int:word_id>', methods=["GET", "POST"])
def get_one_word(word_id):
    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('SELECT * FROM words WHERE words.id = (%s)', [word_id])
        word = curs.fetchone()
    word = {'id': word[0], 'word': word[1], 'stem': word[2], 'part_of_speech': word[3]}

    add_endings([word])

    return json.dumps(word)


# PUT chosen employee

@app.route('/vocabulary/patch/<int:word_id>', methods=["PATCH"])
def update_word(word_id):
    data = request.json
    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('SELECT * FROM words WHERE words.id = (%s)', [word_id])
        word = curs.fetchone()
    cursor.close()
    word = {'id': word[0], 'word': word[1], 'stem': word[2], 'part_of_speech': word[3]}

    add_endings([word])

    for key, value in data.items():
        word[key] = value
        if key != 'endings':
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('UPDATE words SET ' + key + '=(%s) WHERE words.id = (%s)', [value, word_id])
            conn.commit()
        else:
            for ending in value:
                for ending_key, ending_value in ending:
                    cursor = conn.cursor()
                    with cursor as curs:
                        curs.execute('UPDATE endings SET ' + ending_key + '= (%s)' +
                                     ' WHERE endings.word_id = (%s)' +
                                     ' AND endings.name = (%s)',
                                     [ending_value, word_id, ending['name']])
                    conn.commit()

    return json.dumps({'word_id': word_id})


# DELETE chosen employee

@app.route('/vocabulary/delete/<int:word_id>', methods=["DELETE"])
def delete_word(word_id):
    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('DELETE FROM endings WHERE endings.word_id = (%s)', [word_id])
        curs.execute('DELETE FROM words WHERE id = (%s)', [word_id])
        conn.commit()
    return json.dumps({'word_id': word_id})
