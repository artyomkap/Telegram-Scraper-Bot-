from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


klein_categories_kb = [
    [
        InlineKeyboardButton(text="🚘 Транспортные средства", callback_data='klein_category|transport'),
        InlineKeyboardButton(text="🤿 Услуги", callback_data='klein_category|services')
    ],
    [
        InlineKeyboardButton(text="🎟 Билеты", callback_data='klein_category|tickets'),
        InlineKeyboardButton(text="🖥 Электронника", callback_data='klein_category|electric')
    ],
    [
        InlineKeyboardButton(text="🍼 Семья и дети", callback_data='klein_category|kids'),
        InlineKeyboardButton(text="🎨 Хобби", callback_data='klein_category|hobby')
    ],
    [
        InlineKeyboardButton(text="🏡 Дом и Сад", callback_data='klein_category|garden'),
        InlineKeyboardButton(text="🦮 Домашние питомцы", callback_data='klein_category|pets')
    ],
    [
        InlineKeyboardButton(text="🔑 Недвижимость", callback_data='klein_category|property'),
        InlineKeyboardButton(text="📈 Работа", callback_data='klein_category|job')
    ],
    [
        InlineKeyboardButton(text="💅🏻 Мода и красота", callback_data='klein_category|beauty'),
        InlineKeyboardButton(text="🎵 Музыка, фильмы и книги", callback_data='klein_category|music')
    ],
    [
        InlineKeyboardButton(text="🛠 Помощь поблизости", callback_data='klein_category|help'),
        InlineKeyboardButton(text="🎒 Уроки и курсы", callback_data='klein_category|courses')
    ],
    [
        InlineKeyboardButton(text="💱 Обмен", callback_data='klein_category|trade'),
        InlineKeyboardButton(text="♾ Все категории", callback_data='klein_category|all')
    ]
]


klein_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_categories_kb)

klein_transport_categories_kb = [
    [
        InlineKeyboardButton(text="🚗 Автомобили", callback_data='klein_transport|auto'),
        InlineKeyboardButton(text="🔧 Автозапчасти и шины", callback_data='klein_transport|tires')
    ],
    [
        InlineKeyboardButton(text="⛵ Боуты и аксессуары", callback_data='klein_transport|boats'),
        InlineKeyboardButton(text="🚲 Велосипеды и аксессуары", callback_data='klein_transport|bicycles')
    ],
    [
        InlineKeyboardButton(text="🏍️ Мотоциклы и скутеры", callback_data='klein_transport|motorcycles'),
        InlineKeyboardButton(text="🔩 Запчасти для мотоциклов и аксессуары", callback_data='klein_transport|motorcycle_parts')
    ],
    [
        InlineKeyboardButton(text="🚚 Грузовики и прицепы", callback_data='klein_transport|trucks_and_trailers'),
        InlineKeyboardButton(text="🔧 Ремонт и обслуживание", callback_data='klein_transport|repairs_and_services')
    ],
    [
        InlineKeyboardButton(text="🚐 Дома на колесах", callback_data='klein_transport|motorhomes'),
        InlineKeyboardButton(text="🛠️ Прочие авто, вело и лодочные товары", callback_data='klein_transport|other_auto_bike_boat')
    ],
    [
        InlineKeyboardButton(text="Общие транспортные средства", callback_data="klein_transport|transport")
    ]
]

klein_services_categories_kb = [
    [
        InlineKeyboardButton(text="👴 Помощь пожилым", callback_data='klein_services|senior_care'),
        InlineKeyboardButton(text="🚗 Авто, вело и лодочные товары", callback_data='klein_services|auto_bike_boat')
    ],
    [
        InlineKeyboardButton(text="👶 Няня и детский уход", callback_data='klein_services|babysitter_childcare'),
        InlineKeyboardButton(text="🔌 Электроника", callback_data='klein_services|electronics')
    ],
    [
        InlineKeyboardButton(text="🏡 Дом и сад", callback_data='klein_services|home_and_garden'),
        InlineKeyboardButton(text="🎨 Художники и музыканты", callback_data='klein_services|artists_musicians')
    ],
    [
        InlineKeyboardButton(text="✈️ Путешествия и события", callback_data='klein_services|travel_and_events'),
        InlineKeyboardButton(text="🐾 Уход за животными и обучение", callback_data='klein_services|pet_care_training')
    ],
    [
        InlineKeyboardButton(text="🚚 Переезд и транспорт", callback_data='klein_services|moving_and_transport'),
        InlineKeyboardButton(text="💼 Другие услуги", callback_data='klein_services|other_services')
    ],
    [
        InlineKeyboardButton(text="Общие услуги", callback_data="klein_services|services")
    ]
]


klein_tickets_categories_kb = [
    [
        InlineKeyboardButton(text="🚆 Поезда и общественный транспорт", callback_data="klein_tickets|trains_public_transport"),
        InlineKeyboardButton(text="😄 Комедия и кабаре", callback_data="klein_tickets|comedy_kabarett")
    ],
    [
        InlineKeyboardButton(text="🎫 Скидочные купоны", callback_data="klein_tickets|vouchers"),
        InlineKeyboardButton(text="👶 Дети", callback_data="klein_tickets|kids")
    ],
    [
        InlineKeyboardButton(text="🎤 Концерты", callback_data="klein_tickets|concerts"),
        InlineKeyboardButton(text="🏟️ Спорт", callback_data="klein_tickets|sports")
    ],
    [
        InlineKeyboardButton(text="🎭 Театр и мюзиклы", callback_data="klein_tickets|theater_musicals"),
        InlineKeyboardButton(text="🎟️ Другие билеты", callback_data="klein_tickets|other_tickets")
    ],
    [
        InlineKeyboardButton(text="Общие билеты", callback_data="klein_tickets|tickets")
    ]
]


klein_electric_categories_kb = [
    [
        InlineKeyboardButton(text="🔊 Аудио и Hi-Fi", callback_data='klein_electric|audio_hifi'),
        InlineKeyboardButton(text="🔧 Услуги в сфере электроники", callback_data='klein_electric|electronic_services')
    ],
    [
        InlineKeyboardButton(text="📷 Фото", callback_data='klein_electric|photo'),
        InlineKeyboardButton(text="📱 Телефоны", callback_data='klein_electric|phones')
    ],
    [
        InlineKeyboardButton(text="🏠 Бытовая техника", callback_data='klein_electric|appliances'),
        InlineKeyboardButton(text="🎮 Консоли", callback_data='klein_electric|consoles')
    ],
    [
        InlineKeyboardButton(text="💻 Ноутбуки", callback_data='klein_electric|laptops'),
        InlineKeyboardButton(text="🖥️ ПК", callback_data='klein_electric|pcs')
    ],
    [
        InlineKeyboardButton(text="🖱️ ПК-аксессуары и софт", callback_data='klein_electric|pc_accessories_software'),
        InlineKeyboardButton(text="📱 Планшеты и ридеры", callback_data='klein_electric|tablets_readers')
    ],
    [
        InlineKeyboardButton(text="📺 ТВ и видео", callback_data='klein_electric|tv_video'),
        InlineKeyboardButton(text="🎮 Видеоигры", callback_data='klein_electric|video_games')
    ],
    [
        InlineKeyboardButton(text="🔌 Другая электроника", callback_data='klein_electric|other_electronics')
    ],
    [
        InlineKeyboardButton(text="Общая электроника", callback_data='klein_electric|electric')
    ]
]


klein_family_categories_kb = [
    [
        InlineKeyboardButton(text="👵 Уход за пожилыми", callback_data="klein_family|elderly_care"),
        InlineKeyboardButton(text="👶 Детская одежда", callback_data="klein_family|childrens_clothing")
    ],
    [
        InlineKeyboardButton(text="👟 Детская обувь", callback_data="klein_family|childrens_shoes"),
        InlineKeyboardButton(text="🍼 Товары для младенцев", callback_data="klein_family|baby_products")
    ],
    [
        InlineKeyboardButton(text="🚗 Детские автокресла и сиденья", callback_data="klein_family|child_car_seats"),
        InlineKeyboardButton(text="👩‍👧 Няня и уход за детьми", callback_data="klein_family|babysitter_and_childcare")
    ],
    [
        InlineKeyboardButton(text="🛴 Детские коляски и бугги", callback_data="klein_family|strollers_and_buggies"),
        InlineKeyboardButton(text="🛏️ Мебель для детской комнаты", callback_data="klein_family|childrens_furniture")
    ],
    [
        InlineKeyboardButton(text="🎲 Игрушки", callback_data="klein_family|toys"),
        InlineKeyboardButton(text="👪 Прочие товары для семьи и детей", callback_data="klein_family|other_family_and_children_products")
    ],
    [
        InlineKeyboardButton(text="Общее в Семья", callback_data="klein_family|family")
    ]
]


klein_hobbies_categories_kb = [
    [
        InlineKeyboardButton(text="🔮 Эзотерика и духовное", callback_data='klein_hobbies|esoteric_spiritual'),
        InlineKeyboardButton(text="🍲 Еда и напитки", callback_data='klein_hobbies|food_and_drinks')
    ],
    [
        InlineKeyboardButton(text="🎉 Времяпровождение", callback_data='klein_hobbies|free_time_activities'),
        InlineKeyboardButton(text="🎨 Рукоделие, творчество и искусство", callback_data='klein_hobbies|handcraft_crafts')
    ],
    [
        InlineKeyboardButton(text="🖼️ Искусство и антиквариат", callback_data='klein_hobbies|art_antiques'),
        InlineKeyboardButton(text="🎭 Художники и музыканты", callback_data='klein_hobbies|artist_musician')
    ],
    [
        InlineKeyboardButton(text="🛠️ Моделирование", callback_data='klein_hobbies|modelling'),
        InlineKeyboardButton(text="✈️ Путешествия и услуги по организации событий", callback_data='klein_hobbies|travel_event_services')
    ],
    [
        InlineKeyboardButton(text="🧑‍🤝‍🧑 Сборы", callback_data='klein_hobbies|collect'),
        InlineKeyboardButton(text="⚽ Спорт и кемпинг", callback_data='klein_hobbies|sport_camping')
    ],
    [
        InlineKeyboardButton(text="🎪 Барахолка", callback_data='klein_hobbies|junk'),
        InlineKeyboardButton(text="🔍 Потеряно и найдено", callback_data='klein_hobbies|found_lost')
    ],
    [
        InlineKeyboardButton(text="🎮 Прочее о досуге, хобби и соседстве", callback_data='klein_hobbies|another_hobbies'),
        InlineKeyboardButton(text="Общие хобби", callback_data="klein_hobbies|hobbies"),
    ]
]

klein_garden_categories_kb = [
    [
        InlineKeyboardButton(text="🚿 Ванная", callback_data='klein_garden|bathroom'),
        InlineKeyboardButton(text="💼 Офис", callback_data='klein_garden|office')
    ],
    [
        InlineKeyboardButton(text="🎨 Декор", callback_data='klein_garden|decoration'),
        InlineKeyboardButton(text="🔧 Услуги по дому и саду", callback_data='klein_garden|services')
    ],
    [
        InlineKeyboardButton(text="🌳 Садовые принадлежности и растения", callback_data='klein_garden|garden_accessories'),
        InlineKeyboardButton(text="🛋️ Текстиль для дома", callback_data='klein_garden|home_textiles')
    ],
    [
        InlineKeyboardButton(text="🔨 Ремонт и строительство", callback_data='klein_garden|home_improvement'),
        InlineKeyboardButton(text="🍽️ Кухня и столовая", callback_data='klein_garden|kitchen_dining')
    ],
    [
        InlineKeyboardButton(text="💡 Лампы и освещение", callback_data='klein_garden|lamps_lighting'),
        InlineKeyboardButton(text="🛏️ Спальня", callback_data='klein_garden|bedroom')
    ],
    [
        InlineKeyboardButton(text="🛋️ Гостиная", callback_data='klein_garden|living_room'),
        InlineKeyboardButton(text="🏡 Прочее для дома и сада", callback_data='klein_garden|other_home_garden')
    ],
    [
        InlineKeyboardButton(text="Общее в Дом и Сад", callback_data="klein_garden|garden")
    ]
]


klein_pets_categories_kb = [
    [
        InlineKeyboardButton(text="🐟 Рыбы", callback_data='klein_pets|fish'),
        InlineKeyboardButton(text="🐶 Собаки", callback_data='klein_pets|dogs')
    ],
    [
        InlineKeyboardButton(text="🐱 Кошки", callback_data='klein_pets|cats'),
        InlineKeyboardButton(text="🐭 Мелкие домашние животные", callback_data='klein_pets|small_animals')
    ],
    [
        InlineKeyboardButton(text="🐮 Домашние животные", callback_data='klein_pets|livestock'),
        InlineKeyboardButton(text="🐴 Лошади", callback_data='klein_pets|horses')
    ],
    [
        InlineKeyboardButton(text="🐾 Уход за животными и тренировка", callback_data='klein_pets|pet_care_and_training'),
        InlineKeyboardButton(text="🔍 Пропавшие животные", callback_data='klein_pets|lost_pets')
    ],
    [
        InlineKeyboardButton(text="🐦 Птицы", callback_data='klein_pets|birds'),
        InlineKeyboardButton(text="🛒 Аксессуары", callback_data='klein_pets|accessories')
    ],
    [
        InlineKeyboardButton(text="Общиее в Домашние животные", callback_data="klein_pets|pets")
    ]
]


klein_property_categories_kb = [
    [
        InlineKeyboardButton(text="🏠 На время и в Германии", callback_data='klein_property|temporary_and_wg'),
        InlineKeyboardButton(text="🏢 Квартиры в собственность", callback_data='klein_property|condos')
    ],
    [
        InlineKeyboardButton(text="🌴 Курортные и за границей", callback_data='klein_property|holiday_and_foreign_properties'),
        InlineKeyboardButton(text="🚗 Гаражи и стояночные места", callback_data='klein_property|garages_and_parking_spaces')
    ],
    [
        InlineKeyboardButton(text="🏢 Коммерческая недвижимость", callback_data='klein_property|commercial_properties'),
        InlineKeyboardButton(text="🏡 Участки и сады", callback_data='klein_property|plots_and_gardens')
    ],
    [
        InlineKeyboardButton(text="🏡 Дома на продажу", callback_data='klein_property|houses_for_sale'),
        InlineKeyboardButton(text="🏠 Дома в аренду", callback_data='klein_property|houses_for_rent')
    ],
    [
        InlineKeyboardButton(text="🏢 Аренда квартир", callback_data='klein_property|apartments_for_rent'),
        InlineKeyboardButton(text="🚚 Переезд и транспорт", callback_data='klein_property|moving_and_transport')
    ],
    [
        InlineKeyboardButton(text="🏠 Другая недвижимость", callback_data='klein_property|other_properties'),
        InlineKeyboardButton(text="Общая недвижимость", callback_data='klein_property|property')
    ]
]


klein_job_categories_kb = [
    [
        InlineKeyboardButton(text="📚 Обучение", callback_data='klein_job|training'),
        InlineKeyboardButton(text="👷 Строительство, ремонт и производство", callback_data='klein_job|construction')
    ],
    [
        InlineKeyboardButton(text="💼 Офисная работа и администрирование", callback_data='klein_job|office_administration'),
        InlineKeyboardButton(text="🍽️ Рестораны, кафе и туризм", callback_data='klein_job|gastronomy_tourism')
    ],
    [
        InlineKeyboardButton(text="📞 Обслуживание клиентов и колл-центр", callback_data='klein_job|customer_service'),
        InlineKeyboardButton(text="💼 Мини- и подработки", callback_data='klein_job|mini_jobs')
    ],
    [
        InlineKeyboardButton(text="🔄 Практика", callback_data='klein_job|internships'),
        InlineKeyboardButton(text="👩‍⚕️ Социальная сфера и уход", callback_data='klein_job|social_care')
    ],
    [
        InlineKeyboardButton(text="🚚 Транспорт, логистика и дорожное движение", callback_data='klein_job|transport_logistics'),
        InlineKeyboardButton(text="🤝 Продажи и закупки", callback_data='klein_job|sales_purchases')
    ],
    [
        InlineKeyboardButton(text="👨‍💼 Другие вакансии", callback_data='klein_job|other_jobs'),
        InlineKeyboardButton(text="Общее в работа", callback_data='klein_job|job')
    ]
]



klein_beauty_categories_kb = [
    [
        InlineKeyboardButton(text="💍 Аксессуары и украшения", callback_data="klein_beauty|accessories_jewelry"),
        InlineKeyboardButton(text="💄 Красота и здоровье", callback_data="klein_beauty|beauty_health")
    ],
    [
        InlineKeyboardButton(text="👗 Женская одежда", callback_data="klein_beauty|women_clothing"),
        InlineKeyboardButton(text="👠 Женская обувь", callback_data="klein_beauty|women_shoes")
    ],
    [
        InlineKeyboardButton(text="👔 Мужская одежда", callback_data="klein_beauty|men_clothing"),
        InlineKeyboardButton(text="👞 Мужская обувь", callback_data="klein_beauty|men_shoes")
    ],
    [
        InlineKeyboardButton(text="⌚ Часы и ювелирные изделия", callback_data="klein_beauty|watches_jewelry"),
        InlineKeyboardButton(text="👚 Прочая мода и красота", callback_data="klein_beauty|other_fashion_beauty")
    ],
    [
        InlineKeyboardButton(text="Общее в Красоте ", callback_data="klein_beauty|beauty")
    ]
]



klein_music_categories_kb = [
    [
        InlineKeyboardButton(text="📚 Книги и журналы", callback_data="klein_music|books_and_magazines"),
        InlineKeyboardButton(text="📝 Офис и канцелярские товары", callback_data="klein_music|office_and_stationery")
    ],
    [
        InlineKeyboardButton(text="🎭 Комиксы", callback_data="klein_music|comics"),
        InlineKeyboardButton(text="🎓 Учебная литература", callback_data="klein_music|textbooks_school_study")
    ],
    [
        InlineKeyboardButton(text="🎬 Фильмы и DVD", callback_data="klein_music|movies_and_dvd"),
        InlineKeyboardButton(text="🎵 Музыка и CD", callback_data="klein_music|music_and_cds")
    ],
    [
        InlineKeyboardButton(text="🎸 Музыкальные инструменты", callback_data="klein_music|musical_instruments"),
        InlineKeyboardButton(text="📀 Прочая музыка, фильмы и книги", callback_data="klein_music|other_music_movies_books")
    ],
    [
        InlineKeyboardButton(text="Общее в Музыка и Фильмы", callback_data="klein_music|music")
    ]
]


klein_help_categories_kb = [
    [
        InlineKeyboardButton(text="🤝 Помощь соседям", callback_data="klein_help|neighborhood_assistance"),
        InlineKeyboardButton(text="Общее в помощь", callback_data="klein_help|help")
    ]
]


klein_courses_categories_kb = [
    [
        InlineKeyboardButton(text="💄 Красота и здоровье", callback_data='klein_courses|beauty_health'),
        InlineKeyboardButton(text="💻 Курсы по компьютерам", callback_data='klein_courses|computer_courses')
    ],
    [
        InlineKeyboardButton(text="🔮 Эзотерика и духовное развитие", callback_data='klein_courses|esoteric_spiritual'),
        InlineKeyboardButton(text="🍳 Кулинария и выпечка", callback_data='klein_courses|cooking_baking')
    ],
    [
        InlineKeyboardButton(text="🎨 Искусство и дизайн", callback_data='klein_courses|art_design'),
        InlineKeyboardButton(text="🎵 Музыка и пение", callback_data='klein_courses|music_singing')
    ],
    [
        InlineKeyboardButton(text="📚 Репетиторство", callback_data='klein_courses|tutoring'),
        InlineKeyboardButton(text="⚽ Спортивные курсы", callback_data='klein_courses|sports_courses')
    ],
    [
        InlineKeyboardButton(text="🗣️ Языковые курсы", callback_data='klein_courses|language_courses'),
        InlineKeyboardButton(text="💃 Танцевальные курсы", callback_data='klein_courses|dance_courses')
    ],
    [
        InlineKeyboardButton(text="📖 Дополнительное образование", callback_data='klein_courses|further_education'),
        InlineKeyboardButton(text="🎓 Другие уроки и курсы", callback_data='klein_courses|other_lessons_courses')
    ],
    [
        InlineKeyboardButton(text="Общее в курсах", callback_data='klein_courses|lessons')
    ]
]

klein_trade_categories_kb = [
    [
        InlineKeyboardButton(text="🔄 Обмен", callback_data="klein_trade|exchange"),
        InlineKeyboardButton(text="🔄 Займы", callback_data="klein_trade|loans")
    ],
    [
        InlineKeyboardButton(text="🔄 Благотворительность", callback_data="klein_trade|giveaway"),
        InlineKeyboardButton(text="🔄 Общее в обмен", callback_data="klein_trade|trade")
    ]
]



klein_transport_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_transport_categories_kb)
klein_services_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_services_categories_kb)
klein_tickets_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_tickets_categories_kb)
klein_electric_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_electric_categories_kb)
klein_family_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_family_categories_kb)
klein_hobbies_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_hobbies_categories_kb)
klein_garden_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_garden_categories_kb)
klein_pets_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_pets_categories_kb)
klein_property_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_property_categories_kb)
klein_job_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_job_categories_kb)
klein_beauty_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_beauty_categories_kb)
klein_music_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_music_categories_kb)
klein_help_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_help_categories_kb)
klein_courses_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_courses_categories_kb)
klein_trade_categories = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_trade_categories_kb)


klein_preset_save_kb = [
    [
        InlineKeyboardButton(text="Сохранить пресет", callback_data="save_klein_preset"),
        InlineKeyboardButton(text="Не сохранять", callback_data="not_save_klein_preset")
    ]
]

klein_preset_save = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_preset_save_kb)


klein_parse_preset_kb = [
    [
        InlineKeyboardButton(text="Выполнить парсинг", callback_data="klein_preset_parsing"),
        InlineKeyboardButton(text="Удалить пресет", callback_data="klein_delete_preset")
    ]
]


klein_parse_preset = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_parse_preset_kb)

