from datetime import date, timedelta
import pandas as pd
import requests
import json
import os

api_token = '38c8119603a7760ee9a7499f57271ff5'
directory = 'data'


def call_api(page_number, dataset_name):
    api_url = f'https://onemocneni-aktualne.mzcr.cz/api/v3/{dataset_name}?page={page_number}\
                &itemsPerPage=1000&apiToken=38c8119603a7760ee9a7499f57271ff5'

    header = {'Authorization': '{0}'.format(api_token)}
    response = requests.get(api_url, headers=header)
    print(f'{response} to {dataset_name}')
    if response.status_code == 200:
        content = json.loads(response.content.decode('utf-8'))
        return content
    else:
        return None


def call_api_multiple(name, page):
    api_url = f'https://onemocneni-aktualne.mzcr.cz/api/v3/{name}?page={page}&itemsPerPage=10000\
                &apiToken=38c8119603a7760ee9a7499f57271ff5'
    print(f'api url:{api_url}')
    header = {'Authorization': '{0}'.format(api_token)}
    response = requests.get(api_url, headers=header)
    return response


def call_api_update(filename, last_date):
    date_strictly_after = last_date
    api_url = f'https://onemocneni-aktualne.mzcr.cz/api/v3/{filename}?page=1&itemsPerPage=10000\
    &datum%5Bstrictly_after%5D={date_strictly_after}&apiToken=38c8119603a7760ee9a7499f57271ff5'
    # i += 1
    print(f'api url file update:{api_url}')
    header = {'Authorization': '{0}'.format(api_token)}
    response = requests.get(api_url, headers=header)
    print(response)

    if response.status_code == 200:
        content = json.loads(response.content.decode('utf-8'))
        return content
    else:
        return None


def check_file(path):
    print(f'File {path} exists, skipping download.')
    dff = pd.read_csv(path)
    last_date = dff.iloc[-1, 0]
    print(f'last date: {last_date}')
    yesterday = date.today() - timedelta(days=1)
    print(f'today:{yesterday}')
    # file is actual
    if str(last_date) == str(yesterday):
        print(f'no update, returning whole file')
        return dff
    else:
        return None


def get_prehled():
    content = call_api(1, 'zakladni-prehled')
    if content is not None:
        data = []
        for den in content['hydra:member']:
            data.append([den['datum'],
                         den['provedene_testy_celkem'],
                         den['potvrzene_pripady_celkem'],
                         den['aktivni_pripady'],
                         den['vyleceni'],
                         den['umrti'],
                         den['aktualne_hospitalizovani'],
                         den['provedene_testy_vcerejsi_den'],
                         den['potvrzene_pripady_vcerejsi_den'],
                         den['provedene_antigenni_testy_celkem'],
                         den['provedene_antigenni_testy_vcerejsi_den'],
                         den['vykazana_ockovani_celkem'],
                         den['vykazana_ockovani_vcerejsi_den'],
                         den['potvrzene_pripady_65_celkem'],
                         den['potvrzene_pripady_65_vcerejsi_den'],
                         den['ockovane_osoby_celkem'],
                         den['ockovane_osoby_vcerejsi_den'],
                         den['potvrzene_pripady_vcerejsi_den_datum'],
                         den['potvrzene_pripady_65_vcerejsi_den_datum'],
                         den['vykazana_ockovani_vcerejsi_den_datum'],
                         den['ockovane_osoby_vcerejsi_den_datum'],
                         den['provedene_testy_vcerejsi_den_datum'],
                         den['provedene_antigenni_testy_vcerejsi_den_datum']
                         ])
        dff = pd.DataFrame(data, columns=['Datum',
                                          'Celkem provedených testů',
                                          'Celkem potvrzených případů',
                                          'Aktivní případy',
                                          'Vyléčení',
                                          'Úmrtí',
                                          'Hospitalizovaní',
                                          'Včera provedené testy',
                                          'Včera potvrzené případy',
                                          'Celkem AG testů',
                                          'Včera AG testů',
                                          'Celkem očkování',
                                          'Včera očkování',
                                          'Celkem případů 65+',
                                          'Včera případů 65+',
                                          'Celkem očkovaných',
                                          'Včera očkovaných',
                                          'Potvrzené případy datum',
                                          'Potvrzené případy 65 datum',
                                          'Vykazaná očkování datum',
                                          'Očkované osoby datum',
                                          'Provedené testy datum',
                                          'Provedené antigenní testy datum'
                                          ]
                           )
        return dff
    else:
        return None


def get_inc_kraje_new():
    file = 'incidence-7-14-kraje'
    path = directory + '/' + file + '.csv'
    if os.path.isfile(path):
        df = pd.read_csv(path)
        last_date = df.iloc[-1, 0]
        yesterday = date.today() - timedelta(days=1)
        # file is actual
        if str(last_date) == str(yesterday):
            return df
        # file needs update
        else:
            content = call_api_update(file, last_date)
            data = []
            for den in content['hydra:member']:
                data.append([den['datum'],
                             den['kraj_nazev'],
                             den['incidence_7'],
                             den['incidence_14'],
                             den['incidence_7_100000'],
                             den['incidence_14_100000']
                             ])

            dff = pd.DataFrame(data, columns=['Datum',
                                              'Kraj',
                                              'incidence 7',
                                              'incidence 14',
                                              'incidence 7 na 100 000',
                                              'incidence 14 na 100 000'
                                             ]
                              )
            old_df = pd.read_csv(path, delimiter=',')
            result = pd.concat([old_df, dff])
            result.drop_duplicates()
            # noinspection PyTypeChecker
            result.to_csv(path, index=0)

            return result
    else:
        # file does not exists
        data = []
        for i in range(0, 2):
            response = call_api_multiple(file, i)
            if response.status_code == 200:
                content = json.loads(response.content.decode('utf-8'))
                for den in content['hydra:member']:
                    data.append([den['datum'],
                                 den['kraj_nazev'],
                                 den['incidence_7'],
                                 den['incidence_14'],
                                 den['incidence_7_100000'],
                                 den['incidence_14_100000']
                                 ])

        dff = pd.DataFrame(data, columns=['Datum',
                                              'Kraj',
                                              'incidence 7',
                                              'incidence 14',
                                              'incidence 7 na 100 000',
                                              'incidence 14 na 100 000'
                                              ]
                               )
        # noinspection PyTypeChecker
        dff.to_csv(path, index=0)
        return dff


def get_ockovani_kraje():
    file = 'ockovani'
    path = directory + '/' + file + '.csv'
    if os.path.isfile(path):
        df = pd.read_csv(path)
        last_date = df.iloc[-1, 0]
        yesterday = date.today() - timedelta(days=1)
        print(f'today:{yesterday}')
        # file is actual
        if str(last_date) == str(yesterday):
            return df
        # file needs update
        else:
            content = call_api_update(file, last_date)
            data = []
            for den in content['hydra:member']:
                data.append([den['datum'],
                             den['vakcina'],
                             den['kraj_nazev'],
                             den['vekova_skupina'],
                             den['prvnich_davek'],
                             den['druhych_davek'],
                             den['celkem_davek']
                             ])

            dff = pd.DataFrame(data, columns=['Datum',
                                              'Vakcína',
                                              'Kraj',
                                              'Vekova skupina',
                                              'Prvnich dávek',
                                              'Druhych davek',
                                              'Celkem davek'
                                              ]
                               )
            old_df = pd.read_csv(path, delimiter=',')
            result = pd.concat([old_df, dff])
            result.drop_duplicates()
            # noinspection PyTypeChecker
            result.to_csv(path, index=0)

            return result
    else:
        # file does not exists
        data = []
        for i in range(0, 20):
            response = call_api_multiple('ockovani', i)
            if response.status_code == 200:
                content = json.loads(response.content.decode('utf-8'))
                for den in content['hydra:member']:
                    data.append([den['datum'],
                                 den['vakcina'],
                                 den['kraj_nazev'],
                                 den['vekova_skupina'],
                                 den['prvnich_davek'],
                                 den['druhych_davek'],
                                 den['celkem_davek']
                                 ])

        dff = pd.DataFrame(data, columns=['Datum',
                                          'Vakcína',
                                          'Kraj',
                                          'Vekova skupina',
                                          'Prvnich dávek',
                                          'Druhych davek',
                                          'Celkem davek'
                                          ]
                           )
        # noinspection PyTypeChecker
        dff.to_csv(path, index=0)

        return dff


def get_nvut():
    content = call_api(1, 'nakazeni-vyleceni-umrti-testy')
    if content is not None:
        data = []
        for den in content['hydra:member']:
            data.append([den['datum'],
                         den['prirustkovy_pocet_nakazenych'],
                         den['kumulativni_pocet_nakazenych'],
                         den['prirustkovy_pocet_vylecenych'],
                         den['kumulativni_pocet_vylecenych'],
                         den['prirustkovy_pocet_umrti'],
                         den['kumulativni_pocet_umrti'],
                         den['prirustkovy_pocet_provedenych_testu'],
                         den['kumulativni_pocet_testu'],
                         den['prirustkovy_pocet_provedenych_ag_testu'],
                         den['kumulativni_pocet_ag_testu'],
                         ])

        dff = pd.DataFrame(data, columns=['Datum',
                                          'Nakažení',
                                          'Nakažení_k',
                                          'Vyléčení',
                                          'Vyléčení_k',
                                          'Zemřelí',
                                          'Zemřelý_k',
                                          'Testovaní',
                                          'Testovaní_k',
                                          'Testovaní (AG)',
                                          'Testovaní_k (AG)'
                                          ]
                           )

        return dff
    else:
        return None


def get_hosp():
    content = call_api(1, 'hospitalizace')
    if content is not None:
        data = []
        for den in content['hydra:member']:
            data.append([den['datum'],
                         den['stav_bez_priznaku'],
                         den['stav_lehky'],
                         den['stav_stredni'],
                         den['stav_tezky']
                         ])
        dff = pd.DataFrame(data, columns=['Datum', 'bez příznaků', 'lehký stav', 'střední stav', 'těžký stav'])
        return dff
    else:
        return None


def get_hosp_ocko():
    content = call_api(1, 'ockovani-hospitalizace')
    if content is not None:
        data = []
        for den in content['hydra:member']:
            data.append([den['datum'],
                         den['hospitalizovani_bez_ockovani'],
                         den['hospitalizovani_nedokoncene_ockovani'],
                         den['hospitalizovani_dokoncene_ockovani'],
                         den['hospitalizovani_posilujici_davka'],
                         ])

        dff = pd.DataFrame(data, columns=['Datum',
                                          'bez očkování',
                                          'nedokončené očkování',
                                          'dokončené očkování',
                                          'posilující dávka'
                                          ]
                           )

        return dff
    else:
        return None


def get_incidence_cr():
    content = call_api(1, 'incidence-7-14-cr')
    if content is not None:
        data = []
        for den in content['hydra:member']:
            data.append([den['datum'],
                         den['incidence_7'],
                         den['incidence_14'],
                         ])

        dff = pd.DataFrame(data, columns=['Datum', 'incidence 7', 'incidence 14'])

        return dff
    else:
        return None


def get_ock_demo():
    file = 'ockovani-demografie'
    path = directory + '/' + file + '.csv'
    # file exist
    if os.path.isfile(path):
        df = pd.read_csv(path)
        last_date = df.iloc[-1, 0]
        yesterday = date.today() - timedelta(days=1)
        # file is actual
        if str(last_date) == str(yesterday):
            return df
        # file needs update
        else:
            content = call_api_update(file, last_date)
            data = []
            for den in content['hydra:member']:
                data.append([den['datum'],
                             den['vakcina'],
                             den['vekova_skupina'],
                             den['pohlavi'],
                             den['pocet_davek']
                             ])

            dff = pd.DataFrame(data, columns=['Datum',
                                              'vakcína',
                                              'věková skupina',
                                              'pohlaví',
                                              'počet dávek'
                                              ]
                               )
            old_df = pd.read_csv(path, delimiter=',')
            result = pd.concat([old_df, dff])
            result.drop_duplicates()
            # noinspection PyTypeChecker
            result.to_csv(path, index=0)

            return result
    else:
        # file does not exists
        data = []
        for i in range(1, 15):
            response = call_api_multiple(file, i)
            if response.status_code == 200:
                content = json.loads(response.content.decode('utf-8'))

                for den in content['hydra:member']:
                    data.append([den['datum'],
                                 den['vakcina'],
                                 den['vekova_skupina'],
                                 den['pohlavi'],
                                 den['pocet_davek']
                                 ])

        dff = pd.DataFrame(data, columns=['Datum',
                                          'vakcína',
                                          'věková skupina',
                                          'pohlaví',
                                          'počet dávek'
                                          ]
                           )
        # noinspection PyTypeChecker
        dff.to_csv(path, index=0)
        return dff


def get_inc_kraje():
    data = []
    for i in range(0, 3):
        api_url = f'https://onemocneni-aktualne.mzcr.cz/api/v3/incidence-7-14-kraje?page={i}&itemsPerPage=10000\
                    &apiToken=38c8119603a7760ee9a7499f57271ff5'

        print(f'api url:{api_url}')
        header = {'Authorization': '{0}'.format(api_token)}
        response = requests.get(api_url, headers=header)
        print(response)

        if response.status_code == 200:
            content = json.loads(response.content.decode('utf-8'))

            for den in content['hydra:member']:
                data.append([den['datum'],
                             den['kraj_nazev'],
                             den['incidence_7'],
                             den['incidence_14'],
                             den['incidence_7_100000'],
                             den['incidence_14_100000']
                             ])

    dff = pd.DataFrame(data, columns=['Datum',
                                      'Kraj',
                                      'incidence 7',
                                      'incidence 14',
                                      'incidence 7 na 100 000',
                                      'incidence 14 na 100 000'
                                      ]
                       )
    return dff


def get_ockovani():
    file = directory + '/ockovani.csv'
    # file exist
    print(f'get_ockovani start')
    if os.path.isfile(file):
        print(f'File {file} exists, skipping download.')
        dff = pd.read_csv(file)
        last_date = dff.iloc[-1, 0]
        print(f'last date in ockovani: {last_date}')
        yesterday = date.today() - timedelta(days=1)
        print(f'today:{yesterday}')
        # file is actual
        if str(last_date) == str(yesterday):
            print(f'no update, returning whole file')
            return dff
        # file needs update
        else:
            data = []
            date_strictly_after = date.today() - timedelta(days=2)
            api_url = f'https://onemocneni-aktualne.mzcr.cz/api/v3/ockovani?page=1&itemsPerPage=10000\
            &datum%5Bstrictly_after%5D={date_strictly_after}&apiToken=38c8119603a7760ee9a7499f57271ff5'
            # i += 1
            print(f'api url file update:{api_url}')
            header = {'Authorization': '{0}'.format(api_token)}
            response = requests.get(api_url, headers=header)
            print(response)

            if response.status_code == 200:
                content = json.loads(response.content.decode('utf-8'))

                for den in content['hydra:member']:
                    data.append([den['datum'],
                                 den['vakcina'],
                                 den['kraj_nazev'],
                                 den['vekova_skupina'],
                                 den['prvnich_davek'],
                                 den['druhych_davek'],
                                 den['celkem_davek']
                                 ])

                dff = pd.DataFrame(data, columns=['Datum',
                                                  'Vakcína',
                                                  'Kraj',
                                                  'Vekova skupina',
                                                  'Prvnich dávek',
                                                  'Druhych davek',
                                                  'Celkem davek'
                                                  ]
                                   )
                print(dff)
                old_df = pd.read_csv(file, delimiter=',')
                print(f'old df: {old_df}')

                print(f'new df: {dff}')
                # noinspection PyTypeChecker
                result = pd.concat([old_df, dff])
                result.drop_duplicates()
                # noinspection PyTypeChecker
                result.to_csv(file, index=0)

                return result
    else:
        # file does not exists
        data = []
        for i in range(0, 20):
            api_url = f'https://onemocneni-aktualne.mzcr.cz/api/v3/ockovani?page={i}&itemsPerPage=10000\
                        &apiToken=38c8119603a7760ee9a7499f57271ff5'
            print(f'api url:{api_url}')
            header = {'Authorization': '{0}'.format(api_token)}
            response = requests.get(api_url, headers=header)
            print(response)
            # print(content['hydra:member'][3]['datum'])

            if response.status_code == 200:
                content = json.loads(response.content.decode('utf-8'))

                for den in content['hydra:member']:
                    data.append([den['datum'],
                                 den['vakcina'],
                                 den['kraj_nazev'],
                                 den['vekova_skupina'],
                                 den['prvnich_davek'],
                                 den['druhych_davek'],
                                 den['celkem_davek']
                                 ])

        dff = pd.DataFrame(data, columns=['Datum',
                                          'Vakcína',
                                          'Kraj',
                                          'Vekova skupina',
                                          'Prvnich dávek',
                                          'Druhych davek',
                                          'Celkem davek'
                                          ]
                           )
        # noinspection PyTypeChecker
        dff.to_csv(file, index=0)

        return dff



