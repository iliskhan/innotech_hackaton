const sexAr = ['Не уточняет', 'Женщина', 'Мужчина']
const politicalAr = ['Не указано', 'Коммунистические', 'Социалистические',
'Умеренные', 'Либеральные', 'Консервативные', 'Монархические', 'Ультраконсервативные',
'Индифферентные', 'Либертарианские']
const badHabitChoicesAr = ['Не указано', 'Резко негативное', 'Негативное',
'Компромиссное', 'Нейтральное', 'Положительное']

interface IPersonal {
        id?: number;
        langs?: string;
        religion?: string;
        inspired_by?: string;
        smoking?: any;
        alcohol?: any;
        political?: any;
}

function isNumber(value: any) {
    return typeof value === 'number';
}

class Person {
    constructor(input?: any) {
        Object.assign(this, input);
        const newObject: any = {};

        const {avatar, bdate, city, contacts, country, education,
        first_name, interests, last_name, nickname, occupation, personal, sex, vk_user_id} = this;

        if (bdate) newObject['День рождения'] = bdate;
        if (city) newObject['Город'] = city;
        if (contacts) newObject['Контакты'] = contacts;
        if (country) newObject['Страна'] = country;
        if (first_name) newObject['Имя'] = first_name;
        if (interests) newObject['Интересы'] = interests;
        if (last_name) newObject['Фамилия'] = last_name;
        if (nickname) newObject['Отчество'] = nickname;

        if (isNumber(sex)) newObject['Пол'] = sexAr[sex];


        if (personal) {
            const {
             inspired_by, religion, smoking, alcohol, political, langs,
            } = personal;
            if (isNumber(smoking)) newObject['Курение'] = badHabitChoicesAr[smoking];
            if (isNumber(alcohol))  newObject['Алкоголь'] = badHabitChoicesAr[alcohol];
            if (isNumber(political)) newObject['Полит. предпочтения'] = politicalAr[political];
            if (inspired_by) newObject['Вдохновение'] = inspired_by;
            if (religion) newObject['Религия'] = religion;
            if (langs) newObject['Языки'] = langs;
        }

        if (occupation) {
            const {name} = occupation;
            if (name) newObject['Карьера'] = name;
        }

        if (education) {
            const {university} = education;
            if (university) newObject['Образование'] = university;
        }

        return newObject;
    }

    id?: number;
    avatar?: string;
    personal?: IPersonal
    occupation?: {
        id?: number;
        type?: string;
        name?: string;
    };
    vk_user_id?: string;
    first_name?: string;
    last_name?: string;
    bdate?: string;
    city?: string;
    contacts?: string;
    country?: string;
    interests?: string;
    sex?: any;
    nickname?: string;
    education?: {
        id?: number;
        university?: string;
        faculty?: string;
        graduation?: number;
    };
}

export {Person};