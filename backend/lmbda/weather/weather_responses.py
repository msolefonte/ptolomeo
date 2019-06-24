
LIST_YES = [
    'Mejor llevarlo encima, por si acaso.',
    'Nunca está de más estar preparado.',
    'Es mejor tenerlo y no necesitarlo que necesitarlo y no tenerlo.',
    'Teniendo en cuenta el pronóstico, yo diría que sí.'
]

LIST_NO = [
    'No, deberías de estar bien sin eso.',
    'No creo que sea necesario.',
    'Dudo que te haga falta.',
    'Puedes traerlo si quieres, pero dudo que lo necesites.',
    'Me parece bastante improbable que vayas a necesitarlo.'
]

LIST_COLD = [
    'Hace bastante frío allí.',
    'Hace bastante frío, diría.',
    'Yo no me olvidaría de mis guantes.'
]

LIST_CHILLY = [
    'Hace algo de frío.',
    'Necesitarás una chaqueta seguro.',
    'Lleva chaqueta por si acaso.'
]

LIST_WARM = [
    'La temperatura está bien.',
    'Se está bien.',
    'Se puede estar.'
]

LIST_HOT = [
    'Hace bastante calor.',
    'Me parece que necesitarás protector solar.'
]

WEATHER_CURRENT = [
    'El tiempo en {place} ahora mismo es de {temperature} con {condition}.',
    'Ahora mismo hace {temperature} con {condition} en {place}.',
    'Está haciendo {temperature} con {condition} en {place}.',
    'Hace {temperature} en {place} con {condition}.'
]

WEATHER_DATE = [
    '{day} en {place} hará sobre {temperature} con {condition}',
    '{day} en {place} puedes esperar estar sobre los {temperature} con {condition}',
    '{day} en {place} puedes esperar {condition}, con una media de {temperature}',
    '{day} en {place} va a haber {condition}, con temperaturas sobre {temperature}',
]

WEATHER_WEEKDAY = [
    'El {date} en {place} hará {temperature} con {condition}.',
    'El {date} en {place} se espera un ambiente de {temperature} con {condition}.',
    'La predicción para el {date} en {place} es de {condition}, {temperature}.',
    'El {date} en {place} se espera un ambiente de {condition}, con temperaturas sobre {temperature}.'
]

WEATHER_DATE_TIME = [
    '{day} en {place} a las {time} el ambiente será de {temperature} con {condition}.',
    '{day} en {place} a las {time} puedes esperar estar sobre los {temperature} con {condition}.',
    '{day} en {place} a las {time} puedes esperar {condition}, con una temperatura media de unos {temperature}.',
    '{day} a las {time} en {place} va a hacer {temperature} con {condition}.'
]

WEATHER_TIME_PERIOD = [
    'El clima en {city} será de {condition} con una media de {temp} en el periodo desde {time_start} hasta {time_end}.'
]

WEATHER_TIME_PERIOD_DEFINED = [
    'Este {time_period} en {place} habrá una temperatura media de {temperature} con {condition}.',
    'Este {time_period} en {place} puedes esperar {condition}, con temperaturas sobre {temperature}.',
    'Espera un ambiente de {condition} en {time_period} en {place}, con temperaturas sobre {temperature}.',
    'It will be {condition} in {place} and around {temperature} este {time_period}.',
]

WEATHER_DATE_PERIOD_WEEKEND = [
    'El sábado en {city} va a estar {condition_sat}, '
    'con temperaturas desde {sat_temp_min} hasta {sat_temp_max}. '
    'Y el domingo va a estar {condition_sun}, '
    'con mínimas de {sun_temp_min} y máximas de {sun_temp_max}.'
]

WEATHER_DATE_PERIOD = [
    'Desde {date_start} hasta {date_end}'
    ' en {city}, puedes esperar {condition}, '
    'con mínimas de {degree_list_min} y máximas de {degree_list_max}.'
]

WEATHER_ACTIVITY_YES = [
    '¡Sí! Hace buen tiempo para eso.',
    '¡Sí! La verdad es que apetece.'
]

WEATHER_ACTIVITY_NO = [
    'No creo que sea el mejor momento para hacer eso.',
    'No. La verdad es que no apetece mucho.'
]

RESPONSE_WEATHER_CONDITION = [
    'La probabilidad de que {condition_original} es del {condition}%.'
]

RESPONSE_WEATHER_OUTFIT = [
    'La probabilidad de que {condition_original} es del {condition}%. {answer}'
]