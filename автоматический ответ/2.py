from flask import Flask, render_template

app = Flask(__name__)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    profil = {}
    profil['title'] = 'Анкета'
    profil['surname'] = 'Watny'
    profil['name'] = 'Mark'
    profil['education'] = 'выше среднего'
    profil['profession'] = 'штурман марсохода'
    profil['sex'] = 'male'
    profil['motivation'] = 'Всегда мечтал застрять на Марсе!'
    profil['ready'] = 'True'
    return render_template('auto_answer.html', **profil)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
