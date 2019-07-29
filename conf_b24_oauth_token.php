<?php
return [
    'production' => [
        //идентификатор приложения https://%portal%.bitrix24.ru/marketplace/local/edit/0/
        'client_id' => '',
        //секретный код приложения https://%portal%.bitrix24.ru/marketplace/local/edit/0/
        'client_secret' => '',
        'scope' => 'user,task,tasks_extended',
        //домен третьего уровня клиентского проекта в Bitrix24
        'domain' => '%portal%.bitrix24.ru',
        //данные пользователя bitrix24
        'login' => '%email пользователя создавшего приложение%',
        'password' => '%пароль пользователя создавшего приложение$',
    ]
];
?>
