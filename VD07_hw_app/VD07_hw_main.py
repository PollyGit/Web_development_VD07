from flask import Flask, render_template, redirect, url_for, flash
from forms import EditProfileForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Здесь вы можете обработать данные формы, например, сохранить изменения в базе данных
        flash('Ваш профиль был обновлен!', 'success')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
