def convert_step_modelling(text):
    if text == '5 минут':
        return 5
    elif text == '10 минут':
        return 10
    elif text == '15 минут':
        return 15
    elif text == '30 минут':
        return 30
    else:
        return 60